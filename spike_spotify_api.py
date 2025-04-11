import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '203863a432824c938d40cbc2bafba8eb'
client_secret = '07e4f916fbb8447c80b48b0d38c75a4c'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


user_choice = input("Gib den Namen des Künstlers ein: ")
results = sp.search(q=user_choice, type='artist', limit=1)
print("Suchergebnisse:")
artist = results['artists']['items'][0]
print("Künstlername:", artist['name'])
print("Genre(s):", ", ".join(artist['genres']) if artist['genres'] else "Keine Angaben")
print("Popularität:", artist['popularity'])
print("Follower:", artist['followers']['total'])

top_tracks = sp.artist_top_tracks(artist['id'])['tracks']
print("\nTop Tracks:")
for i, track in enumerate(top_tracks, start=1):
    print(f"{i}. {track['name']} (Album: {track['album']['name']})")



#track_id = '10Ss7lQuGNNVshkN507X2J'  #Alex G - TV
#track_info = sp.track(track_id)

#print("Trackname:", track_info['name'])
#print("Künstler:", track_info['artists'][0]['name'])
#print("Album:", track_info['album']['name'])