from datetime import date

def sicher_teilen(a, b):
    if not isinstance(a, (float, int)):
        return None
    if not isinstance(b, (float, int)):
        return None
    if b == 0:
        return None
    return (a/ b)

def datum_heute():
    return date.today().isoformat()

def datum_anzeige():
    return date.today().strftime("%d.%m.%Y")
