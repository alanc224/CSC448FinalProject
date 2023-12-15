import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os
from sklearn.neighbors import NearestNeighbors
from sklearn.manifold import TSNE
import spotipy
from sklearn.preprocessing import StandardScaler
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import plotly.express as px

import nltk
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

import string
import re

# Konrad -- Make sure .env variables have the same name
load_dotenv()
SPOTIFY_KEY1 = os.getenv('SPOTIFY_KEY1')
SPOTIFY_KEY2 = os.getenv('SPOTIFY_KEY2')
SPOTIFY_DATA = os.getenv('SPOTIFY_DATA')
TCC_DATA = os.getenv('TCC_DATA')

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIFY_KEY1,SPOTIFY_KEY2))

def getid(artist_name, song_name):
    artistname = artist_name.strip("['']")
    results = spotify.search(q="artist" + artistname + "track" + song_name, type="track", limit=1)
    SPOTIFY_ARTIST = results["tracks"]["items"][0]['artists'][0]['name']
    if "tracks" in results and "items" in results["tracks"] and SPOTIFY_ARTIST == artistname:
        return results["tracks"]["items"][0]["id"]
    else:
        print("Track not found.")
        return None


def name_lookup(name, df):
    formatting_input = "['{}']".format(string.capwords(name))
    lookup = df[df['artists'].str.lower() == formatting_input.lower()]

    if not lookup.empty:
        return formatting_input
    else:
        print("Artist not found")
        return False


def song_lookup(song, df):
    lookup = df[df['name'].str.lower() == song.lower()]

    if not lookup.empty:
        return string.capwords(song)
    else:
        print("Song not found.")
        return False


def print_info(track):
    print('\nArtist: ' + track['artists'][0]['name'])
    print('Track: ' + track['name'])
    print('Album: ' + track['album']['name'])
    print('Audio Preview: ' + track['preview_url'])
    print('Cover Art: ' + track['album']['images'][0]['url'])


def main():
    df_spotify = pd.read_csv(SPOTIFY_DATA)

    dupes = df_spotify[
    (df_spotify['name'].str.contains('Neon')) & (df_spotify['artists'].str.contains('John Mayer'))]
    print(dupes[['name', 'artists']])
    # need to drop dupes of same songs but contain extra words as seen in example above

    ''' Konrad --- testing if .env variables work, they do :)
    #               make sure your path variables are good if you run into any errors
    df_spotify = pd.read_csv(SPOTIFY_DATA)
    print(df_spotify.head(10))
    print(df_spotify.columns)
    '''

    # Testing spotify api, works so far
    found = False
    while not found:
        artist_name = input("Enter artist name: ")
        if name_lookup(artist_name, df_spotify):
            found = True
            artist_name=name_lookup(artist_name,df_spotify)

    found = False
    while not found:
        song_name = input("Enter song name: ")
        if song_lookup(song_name, df_spotify):
            found = True
            song_name = song_lookup(song_name, df_spotify)

    track_id = getid(artist_name, song_name)
    track = spotify.track(track_id)
    print_info(track)



    


if __name__ == '__main__':
    main()
