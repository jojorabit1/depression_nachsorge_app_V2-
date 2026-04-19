def main():
    name = input("Wie heißt du? ")
    stimmung = int(input("Stimmung heute (1-10): "))
    energie =int(input("Energie heute (1-10): "))
    schlaf = int(input("Wie lange hast du geschlafen (in Stunden): "))

    print(f"Hallo {name}. Stimmung: {stimmung}/10, Energie: {energie}/10, Schlaf: {schlaf}h.")

if __name__ == "__main__":
    main()
