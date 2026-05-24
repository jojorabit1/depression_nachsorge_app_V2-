import sqlite3
from difflib import get_close_matches


def verbindung_herstellen():
    verbindung = sqlite3.connect("nachsorge.db")
    print("Verbindung hergestellt.")
    return verbindung


def erstelle_tabelle(verbindung):
    cursor = verbindung.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eintraege(
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            datum       TEXT UNIQUE,
            stimmung    INTEGER,
            energie     INTEGER,
            schlaf      INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS woerter (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        datum TEXT UNIQUE,
        wort  TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS words (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        wort  TEXT NOT NULL UNIQUE
        )
    """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_words (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            wort        TEXT NOT NULL UNIQUE,
            use_count   INTEGER NOT NULL DEFAULT 1
            )
        """)
    verbindung.commit()
    print("Tabelle bereit")

def wort_speichern(verbindung, datum, wort):
    cursor = verbindung.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO woerter (datum, wort) VALUES (?, ?)",
        (datum, wort)
    )
    verbindung.commit()

def eintrag_speichern(verbindung, datum, stimmung, energie, schlaf):
    cursor = verbindung.cursor()
    cursor.execute("""
        INSERT INTO eintraege (datum, stimmung, energie, schlaf)
        VALUES (?, ?, ?, ?)
    """, (datum, stimmung, energie, schlaf))
    verbindung.commit()
    print(f"Eintrag gespeichert: {datum}, Stimmung {stimmung}, Energie {energie}, Schlaf {schlaf}")


GLOBALE_WOERTER = [
    "erschöpft", "müde", "leer", "schwer", "bleiern",
    "hoffnungsvoll", "ruhig", "stabil", "ausgeglichen", "leicht",
    "ängstlich", "unruhig", "angespannt", "nervös", "gereizt",
    "traurig", "niedergeschlagen", "antriebslos", "apathisch", "taub",
    "dankbar", "zufrieden", "freudig", "lebendig", "kraftvoll",
    "überfordert", "hilflos", "verzweifelt", "einsam", "isoliert",
    "verbunden", "getragen", "sicher", "geborgen", "akzeptiert",
    "unsicher", "schuldig", "schamvoll", "wertlos", "orientierungslos",
    "neugierig", "offen", "motiviert", "fokussiert", "präsent",
    "abwesend", "benebelt", "konfus", "zerstreut", "distanziert"
]

def befuelle_words():
    with verbindung_herstellen() as conn:
        cursor = conn.cursor()
        for wort in GLOBALE_WOERTER:
            cursor.execute(
                "INSERT OR IGNORE INTO words (wort) VALUES (?)",
                (wort,)
            )
        conn.commit()

def user_word_speichern(wort):
    with verbindung_herstellen() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_words (wort, use_count)
            VALUES (?, 1) 
            ON CONFLICT(wort) DO UPDATE SET use_count = use_count + 1
        """, (wort,))
        conn.commit()



def eintrag_laden(verbindung):
    verbindung.row_factory = sqlite3.Row
    cursor = verbindung.cursor()
    cursor.execute("SELECT * FROM eintraege")
    return [dict(zeile) for zeile in cursor.fetchall()]


def wort_laden(verbindung, datum):
    verbindung.row_factory = sqlite3.Row
    cursor = verbindung.cursor()
    cursor.execute(
        "SELECT wort FROM woerter WHERE datum = ?",
        (datum,)
        )
    ergebnis = cursor.fetchone()
    if ergebnis:
        return ergebnis["wort"]
    return None


def fuzzy_suche(eingabe):
    if len(eingabe) <2:
        return []
    with verbindung_herstellen() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT wort FROM words")
        words = [zeile[0] for zeile in cursor.fetchall()]
        cursor.execute("SELECT wort FROM user_words")
        user_words = [zeile[0] for zeile in cursor.fetchall()]
    alle_woerter = list(set(words + user_words))
    return get_close_matches(eingabe, alle_woerter, n=5, cutoff=0.3)
