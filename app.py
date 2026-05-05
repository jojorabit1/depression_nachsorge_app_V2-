import streamlit as st

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

    stimmungswerte = []
    for tag in woche:
        stimmungswerte.append(tag["stimmung"])

    durchschnitt = round(sum(stimmungswerte) / len(stimmungswerte), 1)
    st.write(f"Durchschnitt Stimmung: {durchschnitt}")

    schlechtester_wert = 10
    schlechtester_tag = 1
    for i, tag in enumerate(woche):
        if tag["stimmung"] < schlechtester_wert:
            schlechtester_wert = tag["stimmung"]
            schlechtester_tag = i + 1

    st.write(f"Schlechtester Tag: Tag {schlechtester_tag} (Stimmung {schlechtester_wert})")

    kritische_tage = 0
    for tag in woche:
        if tag["energie"] < 4:
            kritische_tage = kritische_tage + 1

    st.write(f"Tage mit niedriger Energie: {kritische_tage}")

    if kritische_tage > 3:
        st.write("⚠️ Diese Woche war belastend. Bitte sprich mit jemandem.")
    elif kritische_tage >= 1:
        st.write("Diese Woche war gemischt. Achte auf dich.")
    else:
        st.write("Gute Woche! Deine Energie war stabil.")

