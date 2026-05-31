import streamlit as st
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