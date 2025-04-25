import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '203863a432824c938d40cbc2bafba8eb'
client_secret = '07e4f916fbb8447c80b48b0d38c75a4c'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


user_choice = input("Gib den Namen des Künstlers ein: ")
results = sp.search(q=user_choice, type='artist', limit=1)
print(results)
file = open("spike_spotify_api.json", "w")
file.write(json.dumps(results))
file.close()