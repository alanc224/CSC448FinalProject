import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import pandas as pd
from main import nn_model
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import string
import re

app = Flask(__name__)

load_dotenv()
SPOTIFY_KEY1 = '798c070d2d5e4ab98b36353e469dba19' # To prevent the need for authentification, we will delete this once the semester is over
SPOTIFY_KEY2 = 'ec5f36a15c864212a84ab03d15fc7c74'
SPOTIFY_DATA = os.getenv('SPOTIFY_DATA')

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIFY_KEY1,SPOTIFY_KEY2))

@app.route('/', methods=['GET','POST'])
def req():
    URI_exists = False

    if request.method == 'POST':
        URI_exists = True
        URI = request.form.get('URI')

        URI = URI.split("/")[-1].split("?")[0]

        URI = "spotify:track:"+URI

        print(URI) # now we're gonna take a link instead


        if is_valid_spotify_uri(URI) == False:
            URI_exists = False
            alert_user = "This URI is not recognized :("
            return render_template('index.html', alert_user=alert_user, 
                                            URI_exists=URI_exists)
        
        df_spotify = pd.read_csv(SPOTIFY_DATA)
        df_spotify.dropna()
        df_spotify.drop_duplicates()
        track = spotify.track(URI)
        # print_info(track)

        Cur_Artist = track['artists'][0]['name']
        Cur_Track = track['name']
        Cur_Album = track['album']['name']
        Cur_Audio_Preview = track['preview_url']
        Cur_Cover_Art = track['album']['images'][0]['url']

        track_list = [URI]
        audio_features_dict = spotify.audio_features(track_list)
        songDF = pd.DataFrame(audio_features_dict)
        results = nn_model(df_spotify,songDF)
        # print(results) # sanity check
        rec_songs = {}

        for i in range(5):
            Rec_URI = spotify.track(results.iloc[i]['id'])
            rec_songs[i] = {
           'artists' : results.iloc[i]['artists'],
           'song' : results.iloc[i]['name'],
           'album' : Rec_URI['album']['name'],
           'audio preview' : Rec_URI['preview_url'],
            'cover art' : Rec_URI['album']['images'][0]['url']
            }

        # print(audio_features_dict)
        print(rec_songs) # sanity check

        return render_template('index.html', URI_exists=URI_exists,
                                            Cur_Artist=Cur_Artist,
                                            Cur_Track=Cur_Track,
                                            Cur_Album=Cur_Album,
                                            Cur_Audio_Preview=Cur_Audio_Preview,
                                            Cur_Cover_Art=Cur_Cover_Art,
                                            rec_songs=rec_songs)
    
    return render_template('index.html', URI_exists=URI_exists)

def is_valid_spotify_uri(uri):
    # Define a regular expression pattern for a Spotify URI
    spotify_uri_pattern = r'^spotify:track:[a-zA-Z0-9]+$'

    # Check if the input URI matches the pattern
    if re.match(spotify_uri_pattern, uri):
        return True
    else:
        return False

# Taken from Alan/main.py
def name_lookup(name, df):
    formatting_input = "['{}']".format(string.capwords(name))
    lookup = df[df['artists'].str.lower() == formatting_input.lower()]

    if not lookup.empty:
        return formatting_input
    else:
        print("Artist not found")
        return False

# Taken from Alan/main.py
def song_lookup(song, df):
    lookup = df[df['name'].str.lower() == song.lower()]

    if not lookup.empty:
        return string.capwords(song)
    else:
        print("Song not found.")
        return False

# Taken from Alan/main.py
def print_info(track):
    print('\nArtist: ' + track['artists'][0]['name'])
    print('Track: ' + track['name'])
    print('Album: ' + track['album']['name'])
    AP = track['preview_url']
    if AP is None:
        print("No Audio Preview available")
    else:
        print('Audio Preview: ' + track['preview_url'])
    print('Cover Art: ' + track['album']['images'][0]['url'])


if __name__ == '__main__':
    app.run()