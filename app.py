import dateutil.utils
import streamlit as st
import datenbank
from utils import datum_heute


verbindung = datenbank.verbindung_herstellen()
datenbank.erstelle_tabelle(verbindung)

st.title("Nachsorge-App")
st.subheader("Tages-Check-in")

stimmung = st.slider("Stimmung", min_value=1, max_value=10, value=5)
energie = st.slider("Energie", min_value=1, max_value=10, value=5)
schlaf = st.slider("Schlaf", min_value=1, max_value=10, value=5)


if st.button("Speichern"):
    datum = datum_heute()
    if datenbank.eintrag_heute_vorhanden(verbindung, datum):
        st.warning("Du hast heute bereits eingecheckt")
    else:
        datenbank.eintrag_speichern(verbindung, datum, stimmung, energie, schlaf)
        st.success("Eintrag gespeichert!")

st.subheader("Gespeicherte Einträge")
eintraege = datenbank.eintrag_laden(verbindung)

tabelle = []
for zeile in eintraege:
    tabelle.append({
        "ID": zeile[0],
        "Datum": zeile[1],
        "Stimmung": zeile[2],
        "Energie": zeile[3],
        "Schlaf": zeile[4]
    })

st.table(tabelle)