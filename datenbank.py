import sqlite3

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
    cursor = verbindung.cursor()
    cursor.execute("SELECT * FROM eintraege")
    zeilen = cursor.fetchall()
    for zeile in zeilen:
       print(f"ID {zeile[0]} | {zeile[1]} | Stimmung {zeile[2]} | Energie {zeile[3]} | Schlaf {zeile[4]}")
    return zeilen
def main():
    with sqlite3.connect("nachsorge.db") as verbindung:
        erstelle_tabelle(verbindung)
        eintrag_laden(verbindung)
    print("Verbindung geschlossen.")

if __name__ == "__main__":
    main()

