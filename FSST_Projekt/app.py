from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

# Flask-App
app = Flask(__name__)

# Spotify API Setup
client_id = '203863a432824c938d40cbc2bafba8eb'
client_secret = '07e4f916fbb8447c80b48b0d38c75a4c'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))

# SQLAlchemy Setup
Base = declarative_base()
db_path = "sqlite:///spotify.db"
engine = create_engine(db_path, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# ORM-Modell
class Artist(Base):
    __tablename__ = "artists"
    Name = Column(String, primary_key=True)
    genres = Column(String)
    followers = Column(Integer)
    popularity = Column(Integer)
    Img = Column(String)
    external_urls = Column(String)

    def __init__(self, Name, genres, followers, popularity, Img, external_urls):
        self.Name = Name
        self.genres = genres
        self.followers = followers
        self.popularity = popularity
        self.Img = Img
        self.external_urls = external_urls

# Tabelle erzeugen
Base.metadata.create_all(bind=engine)

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    artist_query = request.form.get("artist").strip()
    search_mode = request.form.get("search_mode")  # "online" oder "offline"

    # Immer zuerst lokale DB prüfen
    artist_from_db = session.query(Artist).filter_by(Name=artist_query).first()

    if search_mode == "offline":
        if artist_from_db:
            data = {
                "name": artist_from_db.Name,
                "genres": artist_from_db.genres.split(", "),
                "followers": f"{artist_from_db.followers:,}".replace(",", "."),
                "popularity": artist_from_db.popularity,
                "image": artist_from_db.Img,
                "spotify_url": artist_from_db.external_urls
            }
            return render_template("result.html", data=data, artist_input=artist_query)
        else:
            return render_template("result.html", data=None, artist_input=artist_query + " (offline)")

    # Online-Suche via Spotify API
    results = sp.search(q=artist_query, type='artist', limit=1)
    items = results["artists"]["items"]

    if not items:
        return render_template("result.html", data=None, artist_input=artist_query + " (online)")

    entry = items[0]
    name = entry["name"]
    popularity = entry["popularity"]
    followers = entry["followers"]["total"]
    genres = ", ".join(entry["genres"]) if entry["genres"] else "Unbekannt"
    img = entry["images"][0]["url"] if entry["images"] else None
    url = entry["external_urls"]["spotify"]

    # Nur speichern, wenn noch nicht in DB
    existing = session.query(Artist).filter_by(Name=name).first()
    if not existing:
        artist_obj = Artist(name, genres, followers, popularity, img, url)
        session.add(artist_obj)
        session.commit()

    # Daten aus DB anzeigen
    artist_from_db = session.query(Artist).filter_by(Name=name).first()
    data = {
        "name": artist_from_db.Name,
        "genres": artist_from_db.genres.split(", "),
        "followers": f"{artist_from_db.followers:,}".replace(",", "."),
        "popularity": artist_from_db.popularity,
        "image": artist_from_db.Img,
        "spotify_url": artist_from_db.external_urls
    }

    return render_template("result.html", data=data, artist_input=name)

if __name__ == "__main__":
    app.run(debug=True)
