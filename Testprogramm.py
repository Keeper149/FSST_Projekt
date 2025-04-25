def ArtistData(dateipfad):
    erste_woerter = []
    try:
        with open(dateipfad, 'r', encoding='utf-8') as datei:
            for zeile in datei:
                woerter = zeile.strip().split()
                if woerter:
                    erste_woerter.append(woerter[0])
    except FileNotFoundError:
        print(f"Datei nicht gefunden: {dateipfad}")
    return erste_woerter

# Beispielnutzung
dateipfad = 'beispiel.txt'
liste = ArtistData(dateipfad)
print(liste)