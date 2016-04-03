from flask import Flask, render_template, request, redirect, g
import urllib2
import json
import base64
import requests

import spotipy
import spotipy.util as util
from api import authorize

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def main():
   return render_template('index.html')


@app.route('/auth')
def auth():
    return redirect(authorize(), code=302)


@app.route('/getArtists', methods=['GET'])
def getArtists(my_spotify):
    followed_artists = my_spotify.current_users_followed_artists(limit=100)
    return render_template('concerts.html', data=map(json.dumps, followed_artists))


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
