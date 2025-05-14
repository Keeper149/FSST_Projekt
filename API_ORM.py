import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#Vorherige Datenbank löschen
file_path=r"C:\Users\Max\Documents\Schule\4CHEL\FSST\Spotify_Website_Projekt\ORM\selftest.db"
if os.path.exists(file_path):
    # Datei existiert, also löschen
    os.remove(file_path)
Base=declarative_base()
#Einloggen in die Spotify API
#Hier muss der eigene Client ID und Client Secret rein
client_id = '203863a432824c938d40cbc2bafba8eb'
client_secret = '07e4f916fbb8447c80b48b0d38c75a4c'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


user_choice = input("Gib den Namen des Künstlers ein: ")
results = sp.search(q=user_choice, type='artist', limit=1)

#print(results)
for entry in results['artists']['items']:
    ArtistN=entry['name']
    ArtistP=entry['popularity'] 
    ArtistF=entry['followers']['total']
    ArtistG=entry['genres']
    ArtistG=ArtistG[0]
    ArtistI=entry['images'][0]['url'] if entry['images'] else None
    ArtistU=entry['external_urls']['spotify']
    #Hier wird die Datenbank mit den Werten gefüllt
    print(entry['name'])
    print(entry['popularity'])
    print(entry['followers']['total'])
    print(entry['genres'])
    print(entry['images'][0]['url'] if entry['images'] else None)
    print(entry['external_urls']['spotify'])
    
class Artist(Base):#Klasse fungiert als Datenbank eintrag
    __tablename__ ="people"#Datenbank Einträge Klassifizieren(Datentyp,Name,Primary_key(Funktion nochmal verstehen)) 
    Name=Column("Artist",String,primary_key=True)
    genres=Column("genres",String)
    followers=Column("followers",Integer)
    popularity=Column("popularity",Integer)
    Img=Column("Img",String)
    external_urls=Column("url",String)
    
    def __init__(self,Name,popularity,followers,genres,Img,external_urls):#Klassen Attribute über Konstruktor vergeben
        self.Name=Name
        self.genres=genres
        self.followers=followers
        self.popularity=popularity
        self.external_urls=external_urls
        self.Img=Img
        
        
    def __repr__(self):#Gibt String Version der Klassen aus
        return f"{(self.Name)} {self.genres} {self.followers} ({self.popularity}) {self.external_urls}) {self.Img}"
    
engine= create_engine(r"sqlite+pysqlite:///C:\Users\Max\Documents\Schule\4CHEL\FSST\Spotify_Website_Projekt\ORM\selftest.db", echo=True)
#Erstellt Db Datei und verknüpft sich mit ihr
Base.metadata.create_all(bind=engine)#Alle Klasse werden in der Datenbank(db Datei) erzeugt

Session=sessionmaker(bind=engine)#Klasse Session erzeugen(good practice) 
session=Session()#Session wird über Instanz erzeugt

#Objekte erstellen
#p1=Artist("Kanye West",93,29826560,"Rap","https://i.scdn.co/image/ab6761610000e5eb6e835a500e791bf9c27a422a","https://open.spotify.com/artist/5K4W6rqBFWDnAN6FQUkS6x")
p1=Artist(ArtistN,ArtistP,ArtistF,ArtistG,ArtistI,ArtistU)
#Hier wird die Datenbank mit den Werten gefüllt

session.add(p1)#Objekt wird zur Klasse hinzugefügt
session.commit()#Alle Aktionen in der Session werden in die Datenbank geschickt



