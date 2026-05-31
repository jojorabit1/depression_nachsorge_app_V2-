import streamlit as st
import design
import datenbank
from utils import datum_heute



design.design_system_laden()
verbindung = datenbank.verbindung_herstellen()

if "neu_laden" not in st.session_state:
    st.session_state.neu_laden = True

if st.session_state.neu_laden:
    st.session_state.eintraege = datenbank.alle_eintraege_laden(verbindung)
    st.session_state.neu_laden = False

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

