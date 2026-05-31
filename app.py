import streamlit as st
import datenbank
from utils import datum_heute, datum_anzeige
import auswertung
import pandas as pd
from datetime import date
import altair as alt

def design_system_laden():
    st.markdown("""
    <style>
        /* ===== DESIGN SYSTEM · NACHSORGE-APP ===== */

        /* Hintergrundfarbe */
        .stApp {
            background-color: #F7F5F0;
        }

        /* Globale Schrift */
        html, body, [class*="css"] {
            font-family: 'Inter', 'Helvetica Neue', sans-serif;
            font-size: 15px;
            color: #1A1A1A;
        }

        /* Sidebar Hintergrund */
        section[data-testid="stSidebar"] {
            background-color: #EEE9E0;
        }

        /* Karten-Stil */
        .karte {
            background-color: #FFFFFF;
            border-radius: 16px;
            padding: 20px 24px;
            margin-bottom: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        }

        /* Akzentfarbe als Textklasse */
        .teal {
            color: #2A5C68;
            font-weight: 600;
        }
        
        /* karten Überschrift */
        .kartentitel {
            color: #224A54;
            font-size: 17px;
            font-weight: 700;
        }

        /* Fließtext klein */
        .klein {
            font-size: 13px;
            color: #555555;
        }

        /* Button-Stil überschreiben */
        .stButton > button {
            background-color: #2A5C68;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 10px 20px;
            font-size: 15px;
            width: 100%;
        }

        .stButton > button:hover {
            background-color: #1E4450;
        }
        
        .badge-gruen {
            background-color: #d4edda;
            color: #155724;
            border-radius: 8px;
            padding: 0.6rem 1rem;
            margin-bottom: 0.5rem;
        }
        
        .badge-blau {
            background-color: #d0e8f2;
            color: #0c4a6e;
            border-radius: 8px;
            padding: 0.6rem 1rem;
            margin-bottom: 0.5rem;
        }
        
        .badge-gelb {
            background-color: #fff3cd;
            color: #856404;
            border-radius: 8px;
            padding: 0.6rem 1rem;
            margin-bottom: 0.5rem;
        }
        
        .badge-rot {
            background-color: #f8d7da;
            color: #721c24;
            border-radius: 8px;
            padding: 0.6rem 1rem;
            margin-bottom: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)


design_system_laden()
verbindung = datenbank.verbindung_herstellen()
datenbank.erstelle_tabelle(verbindung)
datenbank.befuelle_words(verbindung)


if "neu_laden" not in st.session_state:
    st.session_state.neu_laden = True

if st.session_state.neu_laden:
    st.session_state.eintraege = datenbank.alle_eintraege_laden(verbindung)
    st.session_state.neu_laden = False

with st.sidebar:
    st.title("Nachsorge-App")
    st.write("dein täglicher check-in nach dem Klinikaufenthalt.")
    st.divider()
    st.write(f"Heute: {datum_anzeige()}")
    st.write(f"einträge gesamt: {len(st.session_state.eintraege)}")

tab_checkin, tab_verlauf, tab_auswertung = st.tabs(["check-in", "verlauf", "auswertung"])


letzter_eintrag = datenbank.eintrag_laden(verbindung)

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
            datenbank.alle_eintraege_laden(verbindung, datum, stimmung, energie, schlaf)
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


