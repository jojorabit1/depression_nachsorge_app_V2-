import streamlit as st
import datenbank
from utils import datum_heute, datum_anzeige
import auswertung
import pandas as pd
from datetime import date
import altair as alt


verbindung = datenbank.verbindung_herstellen()
datenbank.erstelle_tabelle(verbindung)
datenbank.befuelle_words()


if "neu_laden" not in st.session_state:
    st.session_state.neu_laden = True

if st.session_state.neu_laden:
    st.session_state.eintraege = datenbank.eintrag_laden(verbindung)
    st.session_state.neu_laden = False

with st.sidebar:
    st.title("Nachsorge-App")
    st.write("dein täglicher check-in nach dem Klinikaufenthalt.")
    st.divider()
    st.write(f"Heute: {datum_anzeige()}")
    st.write(f"einträge gesamt: {len(st.session_state.eintraege)}")

tab_checkin, tab_verlauf, tab_auswertung = st.tabs(["check-in", "verlauf", "auswertung"])

with tab_checkin:
    st.subheader("Tages-Check-in")

    stimmung = st.slider("Stimmung", min_value=1, max_value=10, value=5)
    energie = st.slider("Energie", min_value=1, max_value=10, value=5)
    schlaf = st.slider("Schlaf", min_value=1, max_value=10, value=5)

    wort_vorhanden = datenbank.wort_laden(verbindung, datum_heute())

    eingabe = st.text_input(
        "Wie lautet dein Wort für heute?",
        value=wort_vorhanden or "",
        placeholder="z.B. erschöpft, ruhig, angespannt ...",
        max_chars=40
    )

    vorschlaege = datenbank.fuzzy_suche(verbindung, eingabe)

    if vorschlaege:
        wort = st.selectbox("Meinst du...?", vorschlaege)
    else:
        wort = eingabe


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
                st.warning (f"Wort konnte nicht gespeichert werden: {e}")


        st.session_state.neu_laden = True
        st.rerun()


with tab_auswertung:


    st.subheader("Auswertung")

    if len(st.session_state.eintraege) == 0:
        st.info("Noch keine Einträge")
    else:
        durchschnitt_stimmung = auswertung.berechne_durchschnitt(st.session_state.eintraege, "stimmung")
        durchschnitt_energie = auswertung.berechne_durchschnitt(st.session_state.eintraege, "energie")
        durchschnitt_schlaf = auswertung.berechne_durchschnitt(st.session_state.eintraege, "schlaf")

        if len(st.session_state.eintraege) >= 2:
            delta_stimmung = round(st.session_state.eintraege[-1]["stimmung"] - st.session_state.eintraege[-2]["stimmung"], 1)
            delta_energie = round(st.session_state.eintraege[-1]["energie"] - st.session_state.eintraege[-2]["energie"], 1)
            delta_schlaf = round(st.session_state.eintraege[-1]["schlaf"] - st.session_state.eintraege[-2]["schlaf"], 1)
        else:
            delta_stimmung = None
            delta_energie = None
            delta_schlaf = None

        col1, col2, col3 = st.columns(3)
        col1.metric(label="Stimmung:", value=durchschnitt_stimmung, delta=delta_stimmung)
        col2.metric(label="Energie:", value=durchschnitt_energie, delta=delta_energie)
        col3.metric(label="Schlaf:", value=durchschnitt_schlaf, delta=delta_schlaf)

        with st.expander ("gespeicherte Einträge anzeigen"):
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
with tab_verlauf:
    st.subheader("Verlauf")

    if len(st.session_state.eintraege) == 0:
        st.info("Noch keine Einträge für den Verlauf.")
    else:
        df = pd.DataFrame(st.session_state.eintraege)
        df["datum"] = pd.to_datetime(df["datum"])
        df["datum"] = df["datum"].dt.strftime("%d.%m.")
        df = df.set_index("datum")
        st.line_chart(df[["stimmung", "energie", "schlaf"]])


