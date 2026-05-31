import streamlit as st
import auswertung
import design
import datenbank
from datetime import date
from utils import datum_heute
import pandas as pd
import altair as alt

verbindung = datenbank.verbindung_herstellen()
design.design_system_laden()

if "neu_laden" not in st.session_state:
    st.session_state.neu_laden = True

if st.session_state.neu_laden:
    st.session_state.eintraege = datenbank.alle_eintraege_laden(verbindung)
    st.session_state.neu_laden = False


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