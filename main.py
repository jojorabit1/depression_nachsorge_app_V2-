def main():
    name = input("Wie heißt du? ")
    stimmung = int(input("Stimmung heute (1-10): "))
    energie =int(input("Energie heute (1-10): "))
    schlaf = int(input("Wie lange hast du geschlafen (in Stunden): "))

    print(f"Hallo {name}. Stimmung: {stimmung}/10, Energie: {energie}/10, Schlaf: {schlaf}h.")

    if stimmung < 4 and energie < 4:
        if schlaf < 5:
            print(f"⚠️ Achtung {name}: Deine Werte sind heute kritisch niedrig — "
                  f"und du hast wenig geschlafen. Bitte melde dich bei jemandem.")
        else:
            print(f"⚠️ Achtung {name}: Deine Werte sind heute kritisch niedrig. "
                  f"Bitte melde dich bei jemandem.")
    elif stimmung < 4 or energie < 4 or schlaf < 5:
        print(f"Heute scheint es dir nicht ganz leicht zu fallen, {name}. Achte auf dich.")
    else:
        print(f"Gut gemacht, {name}. Deine Werte sind heute solide.")


def auswertung_woche(werte):
    durchschnitt = round(sum(werte) / len(werte),1)

    kritische_tage = 0
    for wert in werte:
        if wert < 4:
            kritische_tage = kritische_tage + 1

    print(f"Durchschnitt: {durchschnitt}")
    print(f"Kritische Tage: {kritische_tage}")
    if kritische_tage > 3:
        print("Diese Woche war belastend, bitte sprich mit jemandem.")
    elif kritische_tage >= 3:
        print("Diese Woche war gemischt. Ach te auf dich")
    else:
        print("Gute Woche! Deine Werte waren stabil")


def eingabe_woche():
    werte = []
    for tag in range(7):
        wert = int(input(f"Stimmung Tag {tag + 1} (1-10): "))
        werte.append(wert)
    return werte

def dictornary_test():
    woche= [
        {"Stimmung": 6, "Energie": 4, "Schlaf": 7},
        {"Stimmung": 3, "Energie": 2, "Schlaf": 9},
        {"Stimmung": 8, "Energie": 7, "Schlaf": 9}]

    for tag in woche:
        for schluessel, wert in tag.items():
            print(f"{schluessel}: {wert}")


def bewertung_erstellen(stimmung, energie):
    """Logik für das Frühwarnsystem (aus L02/L05)."""
    if stimmung < 4 and energie < 4:
        return "⚠️ Achtung: Deine Werte sind im kritischen Bereich."
    elif stimmung < 4 or energie < 4:
        return "💡 Heute scheint ein schwieriger Tag zu sein. Achte auf dich."
    else:
        return "✅ Deine Werte sehen heute stabil aus."


def berechne_schlaf_bilanz(stunden):
    """Logik für die Schlafauswertung."""
    if stunden < 6:
        return "zu wenig Schlaf"
    elif 6 <= stunden <= 9:
        return "ausreichend Schlaf"
    else:
        return "sehr viel Schlaf"


def main():
    print("--- Tägliches Tracking ---")

    # Eingabe (L01)
    name = input("Name: ").strip()
    stimmung = int(input("Stimmung (1-10): "))
    energie = int(input("Energie (1-10): "))
    schlaf_stunden = float(input("Wie viele Stunden hast du geschlafen? "))

    # Verarbeitung (L05 - Nutzung der Return-Werte)
    feedback_befinden = bewertung_erstellen(stimmung, energie)
    feedback_schlaf = berechne_schlaf_bilanz(schlaf_stunden)

    # Ausgabe (f-Strings aus L01)
    print(f"\nHallo {name}!")
    print(f"Status: {feedback_befinden}")
    print(f"Schlaf-Analyse: Du hattest {feedback_schlaf}.")



if __name__ == "__main__":
     main()
    # stimmung_woche = [6, 4, 7, 3, 8, 2, 6]
    # auswertung_woche(stimmung_woche)
    # wochenwerte = eingabe_woche()
    # auswertung_woche(wochenwerte)
    # dictornary_test()