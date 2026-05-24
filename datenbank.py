import sqlite3

import streamlit


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
    verbindung.commit()
    print("Tabelle bereit")

def wort_speichern(verbindung, datum, wort):
    cursor = verbindung.cursor()
    cursor.execute(
        "INSERT INTO woerter (datum, wort) VALUES (?, ?)",
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