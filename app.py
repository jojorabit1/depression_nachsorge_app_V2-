import streamlit as st
import datenbank
from utils import datum_anzeige
import auswertung
from design import design_system_laden



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




