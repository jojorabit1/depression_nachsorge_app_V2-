import streamlit as st

def design_system_laden():
    # Google Fonts laden
    st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
        /* ===== DESIGN SYSTEM · NACHSORGE-APP ===== */

        /* CSS Variablen */
        :root {
            --bg:          #F4F1ED;
            --bg-warm:     #EDE9E3;
            --primary:     #2A4D5C;
            --primary-lt:  #3B6475;
            --accent:      #6D9AAE;
            --accent-soft: #C9DDE6;
            --text-main:   #1C2E38;
            --text-mid:    #4A6270;
            --text-muted:  #7A9BAA;
            --serif:       'Lora', Georgia, serif;
            --sans:        'DM Sans', sans-serif;
        }

        /* Streamlit Header verstecken */
        header[data-testid="stHeader"] {
            display: none !important;
        }

        /* Hintergrund */
        .stApp {
            background-color: var(--bg);
        }

        /* Globale Schrift */
        html, body, [class*="css"] {
            font-family: var(--sans);
            font-size: 15px;
            color: var(--text-main);
        }

        /* Content-Bereich */
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 80px !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        /* Karten */
        .karte {
            background-color: #FFFFFF;
            border-radius: 16px;
            padding: 20px 24px;
            margin-bottom: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        }

        /* Akzentfarbe */
        .teal {
            color: var(--primary);
            font-weight: 600;
        }

        /* Karten-Überschrift */
        .kartentitel {
            font-family: var(--serif);
            color: var(--primary);
            font-size: 17px;
            font-weight: 500;
        }

        /* Fließtext klein */
        .klein {
            font-size: 13px;
            color: var(--text-mid);
        }

        /* Buttons */
        .stButton > button {
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 10px 20px;
            font-size: 15px;
            width: 100%;
            font-family: var(--sans);
            font-weight: 500;
            height: 54px;
        }
        
        [data-testid="stElementContainer"]:has([data-testid="stBaseButton-secondary"]) {
            display: flex;
            justify-content: flex-end;
        }
        
        [data-testid="stBaseButton-secondary"] {
            width: auto !important;
            min-width: 120px !important;
        }

        .stButton > button:hover {
            background-color: var(--primary-lt);
        }

        /* Badges */
        .badge-gruen {
            background-color: #d4edda;
            color: #155724;
            border-radius: 8px;
            padding: 0.6rem 1rem;
            margin-bottom: 0.5rem;
        }

        .badge-blau {
            background-color: var(--accent-soft);
            color: var(--primary);
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

        /* ── Bottom Navigation ── */
        div[role="radiogroup"] input[type="radio"],
        div[role="radiogroup"] input,
        div[role="radiogroup"] > label > div:first-child,
        div[role="radiogroup"] span[data-testid="stRadioOption"] > div {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            height: 0 !important;
        }

        div[role="radiogroup"]:has(label:nth-child(4)) {
            position: fixed !important;
            bottom: 0 !important;
            left: 0 !important;
            right: 0 !important;
            z-index: 999 !important;
            display: flex;
            background: #ffffff;
            border-radius: 0 !important;
            border-top: 1px solid var(--accent-soft) !important;
            padding: 8px 16px !important;
            gap: 4px;
            margin: 0 !important;
        }
        
        div[role="radiogroup"] label {
            flex: 1;
            width: 25%;
            max-width: 25%;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 10px 4px;
            border-radius: 12px;
            cursor: pointer;
            transition: background 0.2s;
            font-size: 22px;
            line-height: 1;
            font-family: var(--sans);
            color: var(--text-mid);
        }

        div[role="radiogroup"] label:has(input:checked) {
            background: var(--primary);
            color: white;
            flex: 1;
            width: 25%;
            max-width: 25%;
            box-sizing: border-box;
        }
        .stSlider {
            padding-top: 0.3rem !important;
            padding-bottom: 0.3rem !important;
        }
        
        div[data-testid="stVerticalBlock"] > div {
            gap: 0.3rem !important;
        }
        
        .onboarding-screen {
            text-align: center;
            padding: 48px 24px
        }
        
        .onboarding-headline {
            font-family: var(--serif);
            font-size: 32px;
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 16px;
        }
        
        .onboarding-body {
            font-size: 17px;
            color: var(--text-mid);
            line-height: 1.6;
            margin-bottom: 40px
        }    
         
        .onboarding-weiter-btn {
            position: fixed;
            bottom: 24px;
            left: 16px;
            right: 16px;
        }
         
         .splash-screen {
            margin: -1rem -1rem 0 -1rem;
        }
        
        .splash-top {
            background-color: var(--primary);
            height: 30vh;
        }
        
        .splash-wave {
            background-color: var(--bg);
            margin-top: -2px;
        }
        
        .splash-wave svg {
            display: block;
            width: 100%;
        }
        
        .splash-bottom {
            padding: 24px 24px 100px 24px;
            text-align: center;
        }       
        
        .splash-bottom .stButton > button {
            width: auto;
            min-width: 120px;
            float: right;
        }
    </style>
    """, unsafe_allow_html=True)
