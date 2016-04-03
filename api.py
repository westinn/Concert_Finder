import spotipy
from spotipy import oauth2
import os


def authorize():
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

    return oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope="user-follow-read")
