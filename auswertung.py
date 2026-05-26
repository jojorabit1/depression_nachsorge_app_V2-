from utils import sicher_teilen

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