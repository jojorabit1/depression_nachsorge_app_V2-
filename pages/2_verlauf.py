import pandas as pd
import streamlit as st
import design
import datenbank


verbindung = datenbank.verbindung_herstellen()
design.design_system_laden()

if "neu_laden" not in st.session_state:
    st.session_state.neu_laden = True

if st.session_state.neu_laden:
    st.session_state.eintraege = datenbank.alle_eintraege_laden(verbindung)
    st.session_state.neu_laden = False

st.subheader("Verlauf")

if len(st.session_state.eintraege) == 0:
    st.info("Noch keine Einträge für den Verlauf.")
else:
    df = pd.DataFrame(st.session_state.eintraege)
    df["datum"] = pd.to_datetime(df["datum"])
    df["datum"] = df["datum"].dt.strftime("%d.%m.")
    df = df.set_index("datum")
    st.line_chart(df[["stimmung", "energie", "schlaf"]])