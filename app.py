import streamlit as st
import states
import auswertung

st.title("Nachsorge-App")
st.subheader("Tages-Check-in")

woche = []

for tag_nummer in range(3):
    st.subheader(f"Tag {tag_nummer +1}")
    stimmung = st.slider("Stimmung (1-10)", min_value=1, max_value=10, key=f"stimmung_{tag_nummer}")
    energie = st.slider("Energie (1-10)", min_value=1, max_value=10, key=f"energie_{tag_nummer}")
    schlaf = st.slider("Schlaf (1-10)", min_value=1, max_value=10, key=f"schlaf_{tag_nummer}")

    tag = {
        "stimmung": stimmung,
        "energie": energie,
        "schlaf": schlaf

    }
    woche.append(tag)

if st.button("Auswerten"):
    for i, tag in enumerate(woche):
        st.write(f"Stimmung Tag {i + 1}: {tag['stimmung']}")

    durchschnitt_stimmung = auswertung.berechne_durchschnitt(woche, "stimmung")
    st.write(f"Durchschnitt Stimmung: {durchschnitt_stimmung}")

    durchschnitt_energie = auswertung.berechne_durchschnitt(woche, "energie")
    st.write(f"Durchschnitt Energie: {durchschnitt_energie}")

    durchschnitt_schlaf = auswertung.berechne_durchschnitt(woche, "schlaf")
    st.write(f"Durchschnitt Schlaf: {durchschnitt_schlaf}")

    schlechtester = auswertung.finde_schlechtesten_tag(woche, "stimmung")
    st.write(f"Schlechtester Tag: Tag {schlechtester['tag']} (Stimmung {schlechtester["wert"]})")
    bewertung = states.stimmung_check(schlechtester["wert"])
    st.write(f"Bewertung: {bewertung}")

    kritische_tage = auswertung.zaehle_kritische_tage(woche, "energie", 4)
    st.write(f"Tage mit niedriger Energie: {kritische_tage}")

    if kritische_tage > 3:
        st.write("⚠️ Diese Woche war belastend. Bitte sprich mit jemandem.")
    elif kritische_tage >= 1:
        st.write("Diese Woche war gemischt. Achte auf dich.")
    else:
        st.write("Gute Woche! Deine Energie war stabil.")

