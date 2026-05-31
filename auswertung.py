from utils import sicher_teilen

AKTIONSKATALOG = {
    "schlaf": [
        {"aktion": "Heute Abend Handy ab 21 Uhr weglegen", "energie_min": 1, "ikone": "🌙"},
        {"aktion": "Kurzes Entspannungsritual vor dem Schlafen einplanen", "energie_min": 1, "ikone": "🕯️"},
        {"aktion": "Zimmer vor dem Schlafen kurz lüften", "energie_min": 1, "ikone": "🪟"},
        {"aktion": "Morgen zur gleichen Zeit aufstehen wie heute", "energie_min": 1, "ikone": "⏰"},
        {"aktion": "Heute Abend keinen Kaffee mehr nach 14 Uhr", "energie_min": 1, "ikone": "☕"},
        {"aktion": "10 Minuten ruhige Musik hören vor dem Schlafen", "energie_min": 1, "ikone": "🎵"},
    ],
    "bewegung_leicht": [
        {"aktion": "5 Minuten strecken oder dehnen", "energie_min": 1, "ikone": "🧘"},
        {"aktion": "10 Minuten spazieren gehen", "energie_min": 1, "ikone": "🚶"},
        {"aktion": "Einmal die Treppe statt den Aufzug nehmen", "energie_min": 1, "ikone": "🪜"},
        {"aktion": "Drei Minuten frische Luft auf dem Balkon oder vor der Tür", "energie_min": 1, "ikone": "🌬️"},
        {"aktion": "Beim nächsten Telefonat aufstehen und dabei bewegen", "energie_min": 1, "ikone": "📱"},
        {"aktion": "Kurz die Schultern rollen und tief durchatmen", "energie_min": 1, "ikone": "💨"},
    ],
    "bewegung_mittel": [
        {"aktion": "20 Minuten zügig spazieren gehen", "energie_min": 3, "ikone": "🌿"},
        {"aktion": "Kurze Runde um den Block drehen", "energie_min": 3, "ikone": "🏙️"},
        {"aktion": "30 Minuten Fahrrad fahren", "energie_min": 4, "ikone": "🚴"},
        {"aktion": "15 Minuten Joggen im eigenen Tempo", "energie_min": 4, "ikone": "🏃"},
        {"aktion": "Kurzes Körpergewichtstraining: 3 Übungen, je 10 Wiederholungen", "energie_min": 3, "ikone": "💪"},
        {"aktion": "Schwimmen gehen oder ins Wasser", "energie_min": 4, "ikone": "🏊"},
    ],
    "kognition": [
        {"aktion": "Drei Dinge aufschreiben, die heute gut waren", "energie_min": 1, "ikone": "✏️"},
        {"aktion": "10 Minuten lesen — egal was", "energie_min": 2, "ikone": "📖"},
        {"aktion": "Einen kleinen Plan für morgen früh aufschreiben", "energie_min": 1, "ikone": "📋"},
        {"aktion": "Einen Gedanken, der belastet, kurz aufschreiben und weglegen", "energie_min": 1, "ikone": "🗒️"},
        {"aktion": "Eine Sache benennen, auf die du heute stolz sein kannst", "energie_min": 1, "ikone": "🌟"},
        {"aktion": "5 Minuten bewusstes Atemübung: 4 Sekunden ein, 6 Sekunden aus", "energie_min": 1, "ikone": "🫁"},
        {"aktion": "Einen kleinen Erfolg von heute laut aussprechen", "energie_min": 1, "ikone": "🗣️"},
    ],
    "soziales": [
        {"aktion": "Eine Person kurz anschreiben", "energie_min": 1, "ikone": "💬"},
        {"aktion": "Jemanden anrufen, den du magst", "energie_min": 2, "ikone": "📞"},
        {"aktion": "Einer Person heute ein echtes Kompliment machen", "energie_min": 1, "ikone": "🤝"},
        {"aktion": "Jemandem schreiben, den du lange nicht gehört hast", "energie_min": 2, "ikone": "✉️"},
        {"aktion": "Mit einer Person zusammen etwas essen oder Kaffee trinken", "energie_min": 3, "ikone": "☕"},
        {"aktion": "Einem Menschen in deiner Nähe kurz zuhören", "energie_min": 2, "ikone": "👂"},
    ],
    "ernaehrung": [
        {"aktion": "Ein Glas Wasser trinken — jetzt, sofort", "energie_min": 1, "ikone": "💧"},
        {"aktion": "Heute eine Mahlzeit mit Gemüse einplanen", "energie_min": 1, "ikone": "🥦"},
        {"aktion": "Frühstück nicht überspringen, auch wenn klein", "energie_min": 1, "ikone": "🍳"},
        {"aktion": "Heute bewusst und ohne Bildschirm essen", "energie_min": 1, "ikone": "🍽️"},
        {"aktion": "Einen Snack vorbereiten, der morgen früh bereitliegt", "energie_min": 1, "ikone": "🍎"},
    ],
}
def tagesimpuls_generieren(stimmung, energie, schlaf):
    if schlaf < 5:
        kategorie = "schlaf"
    elif energie <= 2 and stimmung <= 3:
        kategorie = "ernaehrung"
    elif energie <= 2:
        kategorie = "bewegung_leicht"
    elif stimmung <= 3:
        kategorie = "soziales"
    else:
        kategorie = "bewegung_mittel"

    aktion = AKTIONSKATALOG[kategorie][0]

    return {
        "aktion": aktion["aktion"],
        "kategorie": kategorie,
        "ikone": aktion["ikone"],
        "begruendung": begruendung_erstellen(kategorie)
    }

def begruendung_erstellen(kategorie):
    begruendungen = {
        "schlaf": "Dein Schlaf war heute Nacht kurz. Eine kleine Schlafhygiene-Gewohnheit kann viel bewirken.",
        "bewegung_leicht": "Auch minimale Bewegung aktiviert den Kreislauf und hebt die Stimmung messbar.",
        "bewegung_mittel": "Regelmäßige Bewegung ist eine der wirksamsten Maßnahmen gegen depressive Verstimmung.",
        "kognition": "Ein kleiner kognitiver Anker hilft, aus dem Gedankenkarussell herauszukommen.",
        "soziales": "Sozialer Kontakt — auch kurz — wirkt nachweislich stimmungsaufhellend.",
        "ernaehrung": "Kleine Ernährungsgewohnheiten stabilisieren Energie und Stimmung über den Tag.",
    }
    return begruendungen[kategorie]
def berechne_durchschnitt(woche, schluessel):
    try:
        werte = []
        for tag in woche:
            werte.append(tag[schluessel])
        return round(sum(werte) / len(werte), 1)
    except ZeroDivisionError:
        return None
    except KeyError:
        return None

def finde_schlechtesten_tag(woche, schluessel):
    schlechtester_wert = 10
    schlechtester_tag = 1
    for i, tag in enumerate(woche):
        if tag[schluessel] < schlechtester_wert:
            schlechtester_wert = tag[schluessel]
            schlechtester_tag = i + 1
    return {"tag": schlechtester_tag, "wert": schlechtester_wert}

def zaehle_kritische_tage(woche, schluessel, schwellenwert):
    kritisch = 0
    for tag in woche:
        if tag[schluessel] < schwellenwert:
            kritisch = kritisch + 1
    return kritisch

def wort_stimmung_korrelation(wort_stimmung_liste):
    sammlung = {}

    for eintrag in wort_stimmung_liste:
        wort = eintrag["wort"]
        stimmung = eintrag["stimmung"]

        if wort not in sammlung:
            sammlung[wort] = []
            sammlung[wort].append(stimmung)

    ergebnis = {}
    for wort, werte in sammlung.items():
        ergebnis[wort] = round(sum(werte) / len(werte), 1)

    return ergebnis

def eskalationsstufe(warnzeichen):
    anzahl = len(warnzeichen)
    woerter = [w["wort"] for w in warnzeichen]

    if anzahl == 0:
        return {
            "stufe": 0,
            "titel": "alles ist stabil",
            "nachricht": "Bei dir gibt es keine auffallenden Wörter",
            "woerter": []
        }
    elif anzahl == 1:
        return {
            "stufe": 1,
            "titel": "es entsteht ein Muster",
            "nachricht": "Ein Wort taucht häufig in schwierigen Momenten auf.",
            "woerter": woerter
        }
    elif anzahl == 2:
        return {
            "stufe": 2,
            "titel": "erhöhte aufmerksamkeit",
            "nachricht": "zwei wörter sind mit niedrigen stimmungswerten verbunden. "
                         "Es könnte hilfreich sein, das mit jemandem zu besprechen",
            "woerter": woerter
        }
    else:
        return {
            "stufe": 3,
            "titel": "bitte sprich mit jemandem",
            "nachricht": "mehrere zeichen gleichzeitig" 
                         " — ein gespräch mit deiner therapeutin oder deinem therapeuten wäre jetzt sinnvoll",
            "woerter": woerter
        }

