import sqlite3
from difflib import get_close_matches
from datetime import datetime


def verbindung_herstellen():
    verbindung = sqlite3.connect("nachsorge.db")
    verbindung.row_factory = sqlite3.Row
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
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id                      INTEGER PRIMARY KEY AUTOINCREMENT,
            name                    TEXT NOT NULL,
            ansprache               TEXT,
            passwort                TEXT NOT NULL,
            onboarding_complete     INTEGER DEFAULT 0,
            created_at              TEXT
            )
        """)
    verbindung.commit()
    print("Tabelle bereit")


def registriere_user(verbindung, name, ansprache, passwort):
    created_at = datetime.now().isoformat()
    cursor = verbindung.cursor()
    cursor.execute(
        "INSERT INTO users (name, ansprache, passwort, created_at) VALUES (?, ?, ?, ?)",
        (name, ansprache, passwort, created_at)
    )
    verbindung.commit()
    return cursor.lastrowid

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


def befuelle_words(verbindung):
        cursor = verbindung.cursor()
        for wort in GLOBALE_WOERTER:
            cursor.execute(
                "INSERT OR IGNORE INTO words (wort) VALUES (?)",
                (wort,)
            )
        verbindung.commit()

def user_word_speichern(verbindung, wort):
    cursor = verbindung.cursor()
    cursor.execute("""
        INSERT INTO user_words (wort, use_count)
        VALUES (?, 1) 
        ON CONFLICT(wort) DO UPDATE SET use_count = use_count + 1
    """, (wort,))
    verbindung.commit()

def get_user(verbindung):
    cursor = verbindung.cursor()
    cursor.execute("SELECT * FROM users LIMIT 1")
    ergebnis = cursor.fetchone()
    if ergebnis:
        return dict(ergebnis)
    return None

def eintrag_laden(verbindung):
    cursor = verbindung.cursor()
    cursor.execute("SELECT * FROM eintraege ORDER BY datum DESC LIMIT 1")
    ergebnis = cursor.fetchone()
    if ergebnis:
        return dict(ergebnis)
    return None

def alle_eintraege_laden(verbindung):
    cursor = verbindung.cursor()
    cursor.execute("SELECT * FROM eintraege ORDER BY datum ASC")
    ergebnisse = cursor.fetchall()
    return [dict(zeile) for zeile in ergebnisse]

def wort_laden(verbindung, datum):
    cursor = verbindung.cursor()
    cursor.execute(
        "SELECT wort FROM woerter WHERE datum = ?",
        (datum,)
        )
    ergebnis = cursor.fetchone()
    if ergebnis:
        return ergebnis["wort"]
    return None


def fuzzy_suche(verbindung, eingabe):
    if len(eingabe) <2:
        return []
    cursor = verbindung.cursor()
    cursor.execute("SELECT wort FROM words")
    words = [zeile[0] for zeile in cursor.fetchall()]
    cursor.execute("SELECT wort FROM user_words")
    user_words = [zeile[0] for zeile in cursor.fetchall()]
    alle_woerter = list(set(words + user_words))
    return get_close_matches(eingabe, alle_woerter, n=5, cutoff=0.3)

def haufigste_woerter(verbindung, anzahl=5):
    cursor = verbindung.cursor()
    cursor.execute("""
        SELECT wort, use_count 
        FROM user_words 
        ORDER BY use_count DESC 
        LIMIT ?"""
        , (anzahl,)
    )
    ergebnisse = cursor.fetchall()
    return [dict(zeile) for zeile in ergebnisse]

def wort_stimmung_laden(verbindung):
    cursor = verbindung.cursor()
    cursor.execute("""
        SELECT woerter.wort, eintraege.stimmung
        From woerter
        JOIN eintraege ON woerter.datum = eintraege.datum
    """)
    ergebnisse = cursor.fetchall()
    return [dict(zeile) for zeile in ergebnisse]

def fruehwarnzeichen_laden(verbindung, min_anzahl=3, schwellenwert=5.0):
    cursor = verbindung.cursor()
    cursor.execute("""
        SELECT w.wort, AVG(e.stimmung) AS avg_stimmung, COUNT(*) AS anzahl
        FROM eintraege e
        JOIN woerter w ON e.datum = w.datum
        GROUP BY w.wort
        HAVING anzahl >= ? AND avg_stimmung < ?
        ORDER BY avg_stimmung ASC
    """, (min_anzahl, schwellenwert)
    )
    ergebnisse = cursor.fetchall()
    return [dict(zeile) for zeile in ergebnisse]