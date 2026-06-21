import streamlit as st
import datenbank
import re
import sqlite3


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
        registrierung_name(verbindung)
    elif screen == 5:
        registrierung_kontakt(verbindung)
    elif screen == 6:
        bestaetigung()


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

def registrierung_name(verbindung):
    st.markdown(f"""
            <div class="splash-screen">
            <div class="splash-top"></div>
            <div class="splash-wave">
                <svg viewBox="0 0 390 60" xmlns="http://www.w3.org/2000/svg">
                    <path d="M0,30 Q97,60 195,30 Q293,0 390,30 L390,0 L0,0 Z" fill="#2A4D5C"/>
                </svg>
            </div>
        </div>
    """, unsafe_allow_html=True)
    nachname                = st.text_input("Nachname")
    vorname                 = st.text_input("Vorname")
    ansprache               = st.text_input("Wie willst du angesprochen werden?")
    if st.button("weiter"):
        if not nachname or not vorname:
            st.error("Bitte alle Pflichfelder ausfüllen")
        else:
            st.session_state["nachname"] = nachname
            st.session_state["vorname"] = vorname
            st.session_state["ansprache"] = ansprache
            st.session_state["onboarding_screen"] += 1
            st.rerun()
def registrierung_kontakt (verbindung):
    st.markdown(f"""
                <div class="splash-screen">
                <div class="splash-top"></div>
                <div class="splash-wave">
                    <svg viewBox="0 0 390 60" xmlns="http://www.w3.org/2000/svg">
                        <path d="M0,30 Q97,60 195,30 Q293,0 390,30 L390,0 L0,0 Z" fill="#2A4D5C"/>
                    </svg>
                </div>
            </div>
        """, unsafe_allow_html=True)
    email = st.text_input("Wie lautet dein E-mail Adresse?")
    if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.error("Bitte eine gültige Email eingeben")
    passwort = st.text_input("Passwort", type="password")
    if passwort:
        checks = [
            (len(passwort) >= 8, "Mindestens 8 Zeichen"),
            (any(c.isupper() for c in passwort), "Mindestens ein Großbuchstabe"),
            (any(c.isdigit() for c in passwort), "Mindestens eine Zahl"),
            (any(c in "!@#$%^&*;" for c in passwort), "Mindestens ein Sonderzeichen"),
        ]
        for erfuellt, text in checks:
            farbe = "green" if erfuellt else "red"
            symbol = "✓" if erfuellt else "✗"
            st.markdown(f'<p style="color:{farbe}; font-size:13px;">{symbol} {text}</p>', unsafe_allow_html=True)
    passwort_wiederholen = st.text_input("Passwort wiederholen", type="password")
    if passwort_wiederholen:
        if passwort != passwort_wiederholen:
            st.error("Passwörter sind nicht identisch")
    if st.button("Konto erstellen"):
        if not email or not passwort or not passwort_wiederholen:
            st.error("Bitte alle Pflichfelder ausfüllen")
        else:
            try:
                datenbank.registriere_user(
                    verbindung,
                    st.session_state["nachname"],
                    st.session_state["vorname"],
                    st.session_state["ansprache"],
                    email,
                    passwort
                )
                st.session_state["onboarding_screen"] += 1
                st.rerun()
            except sqlite3.IntegrityError:
                st.warning("Dise E-Mail-Adresse ist bereits registriert.")
            except Exception as e:
                st.error("Ein unbekannter Fehler ist aufgetreten. Bitte versuche es erneut.")
                print(f"DEBUG: {e}")

def bestaetigung():
    ansprache = st.session_state["ansprache"] or st.session_state.get("vorname", "")
    st.markdown(f"""
            <div class="splash-screen">
            <div class="splash-top"></div>
            <div class="splash-wave">
                <svg viewBox="0 0 390 60" xmlns="http://www.w3.org/2000/svg">
                    <path d="M0,30 Q97,60 195,30 Q293,0 390,30 L390,0 L0,0 Z" fill="#2A4D5C"/>
                </svg>
            </div>
            <div class="splash-bottom">
                <p class="onboarding-headline">Hallo {ansprache}</p>
                <p class="onboarding-body">Dein Konto ist bereit. In den nächsten Schritten richten wir gemeinsam deine persönliche App ein.</p>
                <p class="onboarding-body">Beantworte bitte zuerst ein paar kurze Fragen zu deiner aktuellen Situation - das dauert ca. 5 Minuten. </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    if st.button("Jetzt starten"):
        st.session_state["onboarding_screen"] += 1
        st.rerun()

