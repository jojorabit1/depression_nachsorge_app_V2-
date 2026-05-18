def stimmung_check(wert):
    """Bewertet die Stimmung isoliert."""
    if wert is None or not isinstance(wert, int):
        return None
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


