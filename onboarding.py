import streamlit as st

def zeige_onboarding(verbindung):
    screen = st.session_state["onboarding_screen"]

    if screen == 0:
        herzlich_willkommen()
    elif screen == 1:
        so_funktionierts()
    elif screen == 2:
        deine_sicherheit()
    elif screen == 3:
        sichere_daten()
    elif screen == 4:
        starten()

def herzlich_willkommen():
    st.markdown("""
    <div class="splash-screen">
        <div class="splash-top"></div>
        <div class="splash-wave">
            <svg viewBox="0 0 390 60" xmlns="http://www.w3.org/2000/svg">
                <path d="M0,30 Q97,60 195,30 Q293,0 390,30 L390,0 L0,0 Z" fill="#2A4D5C"/>
            </svg>
        </div>
        <div class="splash-bottom">
            <p class="onboarding-headline">Herzlich Willkommen</p>
            <p class="onboarding-body">Diese App unterstützt dich in der Zeit nach deiner Entlassung aus der Klinik. Sie hilft dir, deinen Alltag zu strukturieren und deine eigenen Frühwarnzeichen zu erkennen.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Weiter"):
        st.session_state["onboarding_screen"] += 1
        st.rerun()

def so_funktionierts():
    st.markdown(f"""
        <div class="splash-screen">
        <div class="splash-top"></div>
        <div class="splash-wave">
            <svg viewBox="0 0 390 60" xmlns="http://www.w3.org/2000/svg">
                <path d="M0,30 Q97,60 195,30 Q293,0 390,30 L390,0 L0,0 Z" fill="#2A4D5C"/>
            </svg>
        </div>
        <div class="splash-bottom">
            <p class="onboarding-headline">So funktioniert's</p>
            <p class="onboarding-body">Du machst regelmäßig einen Check-in und teilst, wie es dir gerade geht.</p>
            <p class="onboarding-body">Die App unterstützt dich dabei, deinen Tag zu planen und zu strukturieren. 
                    Du siehst deinen Verlauf und erkennst Muster in deinem Befinden.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Weiter"):
        st.session_state["onboarding_screen"] += 1
        st.rerun()

def deine_sicherheit():
    st.markdown(f"""
        <div class="splash-screen">
        <div class="splash-top"></div>
        <div class="splash-wave">
            <svg viewBox="0 0 390 60" xmlns="http://www.w3.org/2000/svg">
                <path d="M0,30 Q97,60 195,30 Q293,0 390,30 L390,0 L0,0 Z" fill="#2A4D5C"/>
            </svg>
        </div>
        <div class="splash-bottom">
            <p class="onboarding-headline">Deine Sicherheit</p>
            <p class="onboarding-body">falls es dir mal sehr schlecht geht, hat diese App einen Krisenplan für dich.</p>
            <p class="onboarding-body">Du hinterlegst deine wichtigsten Kontakte und Hilfsressourcen — damit du sie immer zur Hand hast.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


    if st.button("Weiter"):
        st.session_state["onboarding_screen"] += 1
        st.rerun()

def sichere_daten():
    st.markdown(f"""
        <div class="splash-screen">
        <div class="splash-top"></div>
        <div class="splash-wave">
            <svg viewBox="0 0 390 60" xmlns="http://www.w3.org/2000/svg">
                <path d="M0,30 Q97,60 195,30 Q293,0 390,30 L390,0 L0,0 Z" fill="#2A4D5C"/>
            </svg>
        </div>
        <div class="splash-bottom">
            <p class="onboarding-headline">Deine Daten sind sicher</p>
            <p class="onboarding-body">Deine persönlichen Daten bleiben privat und gehören dir.</p>
            <p class="onboarding-body">Du kannst jederzeit sehen, welche Daten die App speichert, und du kannst sie jederzeit löschen.
            Wenn du die App nutzen möchtest, akzeptiere bitte unsere Datenschutzerklärung.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    akzeptiert = st.checkbox("Ich akzeptiere die Datenschutzerklärung und Nutzerbedingungen")

    if akzeptiert:
        if st.button("Weiter"):
            st.session_state["onboarding_screen"] += 1
            st.rerun()
    else:
        st.button("Weiter", disabled=True)

def starten():
    st.markdown(f"""
        <div class="splash-screen">
        <div class="splash-top"></div>
        <div class="splash-wave">
            <svg viewBox="0 0 390 60" xmlns="http://www.w3.org/2000/svg">
                <path d="M0,30 Q97,60 195,30 Q293,0 390,30 L390,0 L0,0 Z" fill="#2A4D5C"/>
            </svg>
        </div>
            <div class="splash-bottom">
                <p class="onboarding-headline">Lass uns starten</p>
                <p class="onboarding-body">Im nächsten Schritt beantwortest du ein paar kurze Fragen zu deiner aktuellen Situation — etwa 5 Minuten. </p>
                <p class="onboarding-body">Dann erstellen wir gemeinsam deinen persönlichen Krisenplan.</p>
            </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Jetzt starten"):
        st.session_state["onboarding_screen"] += 1
        st.rerun()

