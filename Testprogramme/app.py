from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    artist_query = request.form.get("artist").strip().lower()

    with open("artist_data.json", encoding="utf-8") as f:
        data = json.load(f)

    found_artist = None

    # Daten ist jetzt eine Liste – wir müssen über jeden Eintrag iterieren
    for entry in data:
        for artist in entry["artists"]["items"]:
            if artist["name"].lower() == artist_query:
                found_artist = {
                    "name": artist["name"],
                    "popularity": artist["popularity"],
                    "followers": f"{artist['followers']['total']:,}".replace(",", "."),
                    "genres": artist["genres"],
                    "image": artist["images"][0]["url"] if artist["images"] else None,
                    "spotify_url": artist["external_urls"]["spotify"]
                }
                break
        if found_artist:
            break

    return render_template("result.html", data=found_artist, artist_input=artist_query)

if __name__ == "__main__":
    app.run(debug=True)
