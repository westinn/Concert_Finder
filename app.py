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
   auth_token = request.args.get("code", None)
   if auth_token is None:
       return render_template('index.html')
   else:
       print "Have token: {}".format(auth_token)
       spot = spotipy.Spotify(auth=auth_token)
       return getArtists(spot)



@app.route('/auth')
def auth():
    return redirect(authorize(), code=302)


@app.route('/getArtists', methods=['GET'])
def getArtists(spot):
    followed_artists = spot.current_user_followed_artists(limit=100)
    return render_template('concerts.html', data=map(json.dumps, followed_artists))


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
