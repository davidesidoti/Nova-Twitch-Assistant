import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

# Set up authentication
scope = "user-library-read playlist-read-private playlist-read-collaborative user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing"
sp = SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                  redirect_uri=redirect_uri, scope=scope)

# Get the user's playlists
results = sp.user_playlists('sidotidavide')
# Loop through each playlist and print its name
for playlist in results['items']:
    print(playlist['name'])

# Get the currently playing song
try:
    current_track = sp.current_playback()
    track_name = current_track['item']['name']
    artist_name = current_track['item']['artists'][0]['name']
    print("Currently playing:", track_name, "by", artist_name)
except:
    print("No track currently playing.")
