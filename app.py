from flask import Flask, render_template, request, redirect, g
from bandsintown import Artist, base_url, app_id
import urllib2
import os
import json
import base64
import requests

import spotipy
import spotipy.util as util
from spotipy import oauth2 as oauth2
from api import authorize
from bs4 import BeautifulSoup

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def main():
    auth_code = request.args.get("code", None)
    if auth_code is None:
        return render_template('index.html')
    else:
        print "Have token: {}".format(auth_code)
        auth = authorize()
        token = auth.get_access_token(auth_code)
        spot = spotipy.Spotify(auth=token['access_token'])
        return getArtists(spot)


@app.route('/auth')
def auth():
    return redirect(authorize().get_authorize_url(), code=302)


@app.route('/getArtists', methods=['GET'])
def getArtists(spot):
    followed_artists = spot.current_user_followed_artists(limit=30)
    indivs = followed_artists["artists"]["items"]
    location = []
    dates = []
    findbands(artistnames(followed_artists), location, dates)
    sorted(dates, key=comp)
    for artist in indivs:
        if len(artist["images"]) == 0:
           artist["images"] = []
           artist["images"].append({})
           artist["images"][0]["url"] = "https://www.freebeerandhotwings.com/images/blog/tyson.jpeg"
    return render_template('concerts.html', data=indivs, locations=location, dates=dates)


def artistnames(followed_artists):
    names = []
    for item in followed_artists["artists"]["items"]:
        names.append(item["name"])
    return names

def findbands(names, indivs, dates):
    bandstuff = []
    for name in names:
        bandstuff.append(Artist.events(name=name))
        a = Artist.events(name=name)
        if len(a) > 0:
            indivs.append(str(a[0]))
            r  = requests.get(a[0])
            data = r.text
            soup = BeautifulSoup(data)
            for x in soup.findAll('meta'):
                if x.parent.name == "h3":
                    dates.append(x['content'])
        else:
            indivs.append("#")
            dates.append("No date")
    f = open("/opt/fbt/Concert_Finder/bt_json.txt", "r+")
    a = bandstuff[0]

    f.write(str(len(a)))

def comp(x,y):
    monthx = x[5:7]
    dayx = x[8:]
    monthy = y[5:7]
    dayy = y[8:]
    if monthx == monthy:
        return dayx - dayy
    else:
        return monthx - monthy

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
