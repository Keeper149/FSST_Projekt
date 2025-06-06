from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#def Artist_data(Name,popularity,followers,genres): 
file_path=r"C:\Users\Max\Documents\Schule\4CHEL\FSST\Spotify_Website_Projekt\ORM\selftest.db"
os.remove(file_path)
Base=declarative_base()

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
p1=Artist("Kanye West",93,29826560,"Rap","https://i.scdn.co/image/ab6761610000e5eb6e835a500e791bf9c27a422a","https://open.spotify.com/artist/5K4W6rqBFWDnAN6FQUkS6x")

session.add(p1)#Objekt wird zur Klasse hinzugefügt
session.commit()#Alle Aktionen in der Session werden in die Datenbank geschickt

results=session.query(Artist).all#Python Objekts der Session auslesen
#results=session.query(Artist).filter(Artist.lastname=="BOB")#Python Objekts
print(results)
