
# FSST_Projekt – Künstler‑Info mit Spotify API

Dieses Projekt stellt eine kleine Webanwendung bereit, mit der sich Informationen über Musikkünstler abrufen lassen. Die Anwendung kann wahlweise online (direkt über die Spotify API) oder offline (aus der lokalen Datenbank) suchen.

---

## 🎵 Funktionsumfang

- 🔍 Suche nach Künstlern über die Spotify API
- 💾 Zwischenspeichern der Ergebnisse in einer lokalen SQLite‑Datenbank (`spotify.db`)
- 📡 **Online-Suche**: Holt aktuelle Daten direkt von Spotify und speichert sie
- 📁 **Offline-Suche**: Greift nur auf lokal gespeicherte Daten zu – keine Internetverbindung nötig
- 💻 Schlichte Weboberfläche mit zwei Seiten: `index.html` (Suche) und `result.html` (Ergebnisse)

Die Hauptlogik befindet sich in `FSST_Projekt/app.py`. Im Verzeichnis `Testprogramme/` liegen zusätzliche Testskripte und Beispieldateien, die zur Entwicklung genutzt wurden.

---

## ⚙️ Voraussetzungen

- Python **3.8** oder neuer
- Die Python‑Pakete:
  - `Flask`
  - `Spotipy`
  - `SQLAlchemy`

**Optional:**
- Ein eigenes Spotify‑Konto mit Entwicklerzugang (für eigene `client_id` und `client_secret`)

---

## 🛠️ Installation

### 1. Repository klonen

```bash
git clone https://github.com/Keeper149/FSST_Projekt.git
cd FSST_Projekt
```

### 2. Virtuelle Umgebung erstellen (empfohlen)

```bash
python3 -m venv venv
source venv/bin/activate      # Unter Windows: venv\Scripts\activate
```

### 3. Abhängigkeiten installieren

```bash
pip install flask spotipy sqlalchemy
```

---

## 🔐 Spotify API konfigurieren (optional)

In `FSST_Projekt/app.py` sind standardmäßig Beispiel-Zugangsdaten hinterlegt.  
Wenn du eigene API-Schlüssel nutzen möchtest:

1. Erstelle ein kostenloses Spotify Entwicklerkonto unter: https://developer.spotify.com/dashboard  
2. Trage deine `client_id` und `client_secret` in `app.py` ein oder nutze Umgebungsvariablen.

---

## 🚀 Anwendung starten

```bash
python FSST_Projekt/app.py
```

Die Web-App ist danach erreichbar unter: [http://localhost:5000](http://localhost:5000)

- **Künstlername eingeben**
- Zwischen **Online-Suche** oder **Offline-Suche** wählen

---

## 🗂️ Projektstruktur (Auszug)

```
FSST_Projekt/
├── FSST_Projekt/
│   ├── app.py              # Hauptprogramm – enthält Webserver und API-Logik
│   ├── spotify.db          # SQLite-Datenbank (wird automatisch erstellt)
│   └── templates/
│       ├── index.html      # Startseite mit Suchmaske
│       └── result.html     # Ergebnisseite mit Künstlerinfos
├── Testprogramme/          # Testskripte und Beispiele
├── templates/              # (Alt) Weitere HTML-Dateien
└── README.md               # Diese Projektbeschreibung
```

---

## 📬 Kontakt & Feedback

Fragen, Ideen oder Bugs?  
Gerne ein [Issue](https://github.com/Keeper149/FSST_Projekt/issues) eröffnen oder direkt einen Pull Request einreichen!

---

## 🪪 Lizenz

Dieses Projekt wurde im Rahmen eines Schulprojekts erstellt. Lizenzhinweise findest du ggf. in einer späteren Version des Repositories.
