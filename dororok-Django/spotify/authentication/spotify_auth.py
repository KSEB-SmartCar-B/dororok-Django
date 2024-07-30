import os
from django.conf import settings
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def get_spotify_client():
    client_id = os.getenv('SPOTIFY_CID')
    client_secret = os.getenv('SPOTIFY_SECRET')
    if not client_id or not client_secret:
        raise ValueError("Spotify client id and client secret must be set")

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp
