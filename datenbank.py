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
            datum       TEXT,
            stimmung    INTEGER,
            energie     INTEGER,
            schlaf      INTEGER
        )
    """)
    verbindung.commit()
    print("Tabelle bereit")

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

def eintrag_heute_vorhanden(verbindung, datum):
    cursor = verbindung.cursor()
    cursor.execute("SELECT * FROM eintraege WHERE datum = ?", (datum,))
    ergebnis = cursor.fetchone()
    return bool(ergebnis)

