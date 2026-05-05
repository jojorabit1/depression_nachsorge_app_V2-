def stimmung_check(wert):
    """Bewertet die Stimmung isoliert."""
    if wert < 4:
        return "niedrig"
    elif wert < 7:
        return "stabil"
    else:
        return "gut"

def schlaf_check(stunden):
    """Bewertet die Schlafqualität."""
    if stunden < 6:
        return "zu wenig"
    return "ausreichend"


