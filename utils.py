def sicher_teilen(a, b):
    if not isinstance(a, (float, int)):
        return None
    if not isinstance(b, (float, int)):
        return None
    if b == 0:
        return None
    return (a/ b)