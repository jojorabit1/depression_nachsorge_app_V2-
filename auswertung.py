def berechne_durchschnitt(woche, schluessel):
    werte = []
    for tag in woche:
        werte.append(tag[schluessel])
    return round(sum(werte) / len(werte), 1)

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