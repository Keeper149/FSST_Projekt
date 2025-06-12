from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

app = Flask(__name__)

# Spotify-Zugangsdaten
client_id = '203863a432824c938d40cbc2bafba8eb'
client_secret = '07e4f916fbb8447c80b48b0d38c75a4c'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))

# Datenbank-Setup
Base = declarative_base()
engine = create_engine("sqlite:///spotify.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

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

Base.metadata.create_all(bind=engine)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    q = request.form["artist"].strip()
    mode = request.form["search_mode"]

    # Offline-Modus: nur lokale DB abfragen
    if mode == "offline":
        a = session.query(Artist).filter_by(Name=q).first()
        data = None
        if a:
            data = {
                "name": a.Name,
                "genres": a.genres.split(", "),
                "followers": f"{a.followers:,}".replace(",", "."),
                "popularity": a.popularity,
                "image": a.Img,
                "spotify_url": a.external_urls
            }
        return render_template("result.html",
                               data=data,
                               artist_input=q,
                               top_tracks=[],
                               latest_albums=[])

    # Online-Modus: Spotify-API ansprechen
    res = sp.search(q=q, type="artist", limit=1)["artists"]["items"]
    if not res:
        return render_template("result.html",
                               data=None,
                               artist_input=q + " (online)",
                               top_tracks=[],
                               latest_albums=[])

    ent = res[0]
    artist_id = ent["id"]
    name = ent["name"]
    pop = ent["popularity"]
    foll = ent["followers"]["total"]
    genres = ", ".join(ent["genres"]) if ent["genres"] else "Unbekannt"
    img = ent["images"][0]["url"] if ent["images"] else None
    url = ent["external_urls"]["spotify"]

    # In DB speichern, falls neu
    if not session.query(Artist).filter_by(Name=name).first():
        session.add(Artist(name, genres, foll, pop, img, url))
        session.commit()

    # Top 10 Songs (Cover, Preview, Popularity)
    tracks = sp.artist_top_tracks(artist_id, country="DE")["tracks"][:10]
    top_tracks = []
    for t in tracks:
        top_tracks.append({
            "name": t["name"],
            "popularity": t["popularity"],
            "preview_url": t["preview_url"],
            "cover": t["album"]["images"][-1]["url"] if t["album"]["images"] else None
        })

    # Neueste 3 Alben nebeneinander
    albums = sp.artist_albums(artist_id, album_type="album", limit=10)["items"]
    seen = set()
    latest_albums = []
    for alb in albums:
        title = alb["name"]
        if title not in seen:
            latest_albums.append({
                "name": title,
                "release_date": alb["release_date"],
                "url": alb["external_urls"]["spotify"],
                "image": alb["images"][0]["url"] if alb["images"] else None
            })
            seen.add(title)
        if len(latest_albums) == 3:
            break

    data = {
        "name": name,
        "genres": genres.split(", "),
        "followers": f"{foll:,}".replace(",", "."),
        "popularity": pop,
        "image": img,
        "spotify_url": url
    }

    return render_template("result.html",
                           data=data,
                           artist_input=name,
                           top_tracks=top_tracks,
                           latest_albums=latest_albums)

if __name__ == "__main__":
    app.run(debug=True)
