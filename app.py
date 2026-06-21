import streamlit as st
import datenbank
from utils import datum_anzeige, datum_heute
import auswertung
from design import design_system_laden
import pandas as pd
import altair as alt
from datetime import date
import onboarding


design_system_laden()
verbindung = datenbank.verbindung_herstellen()
datenbank.erstelle_tabelle(verbindung)
datenbank.befuelle_words(verbindung)

if "onboarding_screen" not in st.session_state:
    st.session_state["onboarding_screen"] = 4

user = datenbank.get_user(verbindung)

if user is None or user["onboarding_complete"] == 0:
    onboarding.zeige_onboarding(verbindung)
else:
    if "neu_laden" not in st.session_state:
        st.session_state.neu_laden = True

    if st.session_state.neu_laden:
        st.session_state.eintraege = datenbank.alle_eintraege_laden(verbindung)
        st.session_state.neu_laden = False

    # Navigation
    seite = st.radio(
        label="Navigation",
        options=["📋", "📈", "📊", "⚠️"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if seite == "📋":
        letzter_eintrag = datenbank.eintrag_laden(verbindung)

        if "checkin_bestaetigung" not in st.session_state:
            st.session_state.checkin_bestaetigung = None

        if st.session_state.checkin_bestaetigung:
            st.success(st.session_state.checkin_bestaetigung)

        if letzter_eintrag:
            impuls = auswertung.tagesimpuls_generieren(
                stimmung=letzter_eintrag["stimmung"],
                energie=letzter_eintrag["energie"],
                schlaf=letzter_eintrag["schlaf"]
            )

            st.markdown(f"""
            <div class="karte">
                <p class="kartentitel">Dein Tagesimpuls</p>
                <p class="teal">{impuls['ikone']} {impuls['aktion']}</p>
                <p class="klein">{impuls['begruendung']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("📋 Noch kein Check-in vorhanden — trag heute deinen ersten ein.")


        st.subheader("Tages-Check-in")

        stimmung = st.slider("Stimmung", min_value=1, max_value=10, value=5)
        energie = st.slider("Energie", min_value=1, max_value=10, value=5)
        schlaf = st.slider("Schlaf", min_value=1, max_value=10, value=5)

        wort_vorhanden = datenbank.wort_laden(verbindung, datum_heute())

        if "wort_eingabe" not in st.session_state:
            st.session_state.wort_eingabe = wort_vorhanden or ""

        eingabe = st.text_input(
            "Wie lautet dein Wort für heute?",
            value=st.session_state.wort_eingabe,
            placeholder="z.B. erschöpft, ruhig, angespannt ...",
            max_chars=40,
            on_change=None
        )

        vorschlaege = datenbank.fuzzy_suche(verbindung, eingabe)

        if vorschlaege:
            if eingabe not in vorschlaege:
                optionen = [eingabe] + vorschlaege
            else:
                optionen = vorschlaege
            auswahl = st.pills(
                "Vorschläge",
                optionen,
                default=None,
                selection_mode="single",
                key="wort_auswahl",
                label_visibility="collapsed"
            )
            if auswahl:
                st.session_state.wort_eingabe = auswahl
                st.rerun()

        wort = st.session_state.wort_eingabe or eingabe


        if st.button("Speichern"):
            datum = datum_heute()

            try:
                datenbank.eintrag_speichern(verbindung, datum, stimmung, energie, schlaf)
                st.success("Eintrag gespeichert!")
            except Exception:
                st.warning("Du hast heute bereits eingecheckt")

            if wort:
                try:
                    datenbank.wort_speichern(verbindung, datum, wort)
                    datenbank.user_word_speichern(verbindung, wort)
                    st.success("Wort gespeichert!")
                except Exception as e:
                    st.warning(f"Wort konnte nicht gespeichert werden: {e}")

            st.session_state.checkin_bestaetigung = f"✓ Check-in gespeichert — dein Wort heute: **{wort}**"
            st.session_state.neu_laden = True
            st.rerun()



    elif seite == "📈":
        st.subheader("Verlauf")

        if len(st.session_state.eintraege) == 0:
            st.info("Noch keine Einträge für den Verlauf.")
        else:
            df = pd.DataFrame(st.session_state.eintraege)
            df["datum"] = pd.to_datetime(df["datum"])
            df = df.sort_values("datum")

            df_long = df.melt(
                id_vars="datum",
                value_vars=["stimmung", "energie", "schlaf"],
                var_name="kategorie",
                value_name="wert"
            )

            chart = alt.Chart(df_long).mark_line(point=True).encode(
                x=alt.X("datum:T", axis=alt.Axis(format="%d.%m", title="")),
                y=alt.Y("wert:Q", scale=alt.Scale(domain=[0, 10]), title=""),
                color="kategorie:N"
            )
            st.altair_chart(chart, use_container_width=True)

    elif seite == "📊":
        st.subheader("Auswertung")

        if len(st.session_state.eintraege) == 0:
            st.info("Noch keine Einträge")
        else:
            durchschnitt_stimmung = auswertung.berechne_durchschnitt(st.session_state.eintraege, "stimmung")
            durchschnitt_energie = auswertung.berechne_durchschnitt(st.session_state.eintraege, "energie")
            durchschnitt_schlaf = auswertung.berechne_durchschnitt(st.session_state.eintraege, "schlaf")

            if len(st.session_state.eintraege) >= 2:
                delta_stimmung = round(
                    st.session_state.eintraege[-1]["stimmung"] - st.session_state.eintraege[-2]["stimmung"], 1)
                delta_energie = round(st.session_state.eintraege[-1]["energie"] - st.session_state.eintraege[-2]["energie"],
                                      1)
                delta_schlaf = round(st.session_state.eintraege[-1]["schlaf"] - st.session_state.eintraege[-2]["schlaf"], 1)
            else:
                delta_stimmung = None
                delta_energie = None
                delta_schlaf = None

            col1, col2, col3 = st.columns(3)
            col1.metric(label="Stimmung:", value=durchschnitt_stimmung, delta=delta_stimmung)
            col2.metric(label="Energie:", value=durchschnitt_energie, delta=delta_energie)
            col3.metric(label="Schlaf:", value=durchschnitt_schlaf, delta=delta_schlaf)

            with st.expander("gespeicherte Einträge anzeigen"):
                tabelle = []
                for zeile in st.session_state.eintraege:
                    tabelle.append({
                        "Datum": date.fromisoformat(zeile["datum"]).strftime("%d.%m.%Y"),
                        "Stimmung": zeile["stimmung"],
                        "Energie": zeile["energie"],
                        "Schlaf": zeile["schlaf"]
                    })

                st.table(tabelle)

            wort_heute = datenbank.wort_laden(verbindung, datum_heute())
            if wort_heute:
                st.write(f"Dein wort für heute: **{wort_heute}**")
            else:
                st.write("Heute noch kein Wort eingegeben")

        st.subheader("Häufigste Wörter")
        woerter = datenbank.haufigste_woerter(verbindung, anzahl=5)

        if not woerter:
            st.info("Noch keine Wörter gespeichert")
        else:
            df_woerter = pd.DataFrame(woerter)
            chart = alt.Chart(df_woerter).mark_bar().encode(
                x="wort",
                y=alt.Y(
                    "use_count:Q",
                    scale=alt.Scale(domainMin=0),
                    axis=alt.Axis(tickMinStep=1, format="d", tickCount=max(df_woerter["use_count"]))
                )
            )
            st.altair_chart(chart, use_container_width=True)

        st.subheader("Wörter im verlauf")
        wort_stimmung = datenbank.wort_stimmung_laden(verbindung)

        if not wort_stimmung:
            st.info("Noch keine Daten für Wortmuster")
        else:
            df_muster = pd.DataFrame(wort_stimmung)
            st.dataframe(df_muster)

        st.subheader("wort ↔ stimmung")
        korrelation = auswertung.wort_stimmung_korrelation(wort_stimmung)

        if not korrelation:
            st.info("noch keine Daten")
        else:
            df_korrelation = pd.DataFrame(
                korrelation.items(),
                columns=["wort", "ø stimmung"]
            )
            st.dataframe(df_korrelation)

        st.subheader("Frühwarnzeichen")
        warnzeichen = datenbank.fruehwarnzeichen_laden(verbindung)
        ergebnis = auswertung.eskalationsstufe(warnzeichen)

        woerter_text = ", ".join(ergebnis["woerter"]) if ergebnis["woerter"] else ""

        stufen_mapping = {
            0: ("gruen", "👌"),
            1: ("blau", "ℹ️"),
            2: ("gelb", "⚠️"),
            3: ("rot", "🛑"),
        }
        stufe_css, icon = stufen_mapping[ergebnis["stufe"]]

        st.markdown(f"""
            <div class="badge-{stufe_css}">
                <p class="kartentitel">{icon} {ergebnis['titel']}</p>
                <p class="klein">{ergebnis['nachricht']} {woerter_text}</p>
            </div>
        """, unsafe_allow_html=True)
    elif seite == "⚠️":
        st.write("Krisenplan")



