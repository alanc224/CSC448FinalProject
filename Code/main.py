import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os
import spotipy
from sklearn.manifold import TSNE
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
    results = spotify.search(q="track" + song_name + "artist:" + artist_name, type="track", limit=1)

    if "tracks" in results and "items" in results["tracks"]:
        return results["tracks"]["items"][0]["id"]
    else:
        print("Track not found.")
        return None


def name_lookup(name, df):
    lookup = df[df['artist_name'].str.lower() == name.lower()]

    if not lookup.empty:
        return name
    else:
        print("Artist not found")
        return False


def song_lookup(song, df):
    lookup = df[df['track_name'].str.lower() == song.lower()]

    if not lookup.empty:
        return song
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
    df = pd.read_csv(TCC_DATA)
    df.drop_duplicates(subset=['track_name'], keep='first', inplace=True)
    df.drop(columns=['lyrics'], axis=1, inplace=True)
    # print(df.columns)

    ''' Konrad --- testing if .env variables work, they do :)
    #               make sure your path variables are good if you run into any errors
    df_spotify = pd.read_csv(SPOTIFY_DATA)
    print(df_spotify.head(10))
    print(df_spotify.columns)
    '''

    '''Testing spotify api, works so far
    found = False
    while not found:
        artist_name = input("Enter artist name: ")
        if name_lookup(artist_name, df):
            found = True

    found = False
    while not found:
        song_name = input("Enter song name: ")
        if song_lookup(song_name, df):
            found = True

    track_id = getid(artist_name, song_name)

    track = spotify.track(track_id)
    print_info(track)
    '''
    

# Preprocessing the lyrics

    lyrics_df = pd.read_csv(TCC_DATA)
    lyrics_df = lyrics_df.iloc[:, [0,1,2,3,4,5,6]] 

    # checked the data and there are no nulls or duplicates

    # print(len(lyrics_df))
    # print(lyrics_df.isnull().sum())
    # print(lyrics_df)
    # print(lyrics_df.duplicated().sum())

    lyrics_df.drop_duplicates(inplace=True)
    lyrics_df.dropna(inplace=True) # just in case
    
    def pipline(somestring):

        somestring = somestring.lower() #make lowercase
        somestring = re.sub(r'[^\w\s]','',somestring) #remove punctuation
        new_string=re.sub('[^a-zA-Z0-9]',' ',somestring) # takes only alphanumeric values
        somestring=re.sub('\s+',' ',new_string) # removes extra characters like extra spaces

        return somestring
    
    print(lyrics_df.columns)

    lyrics_df['cleaned'] = lyrics_df['lyrics'].apply(pipline)

    print(lyrics_df['cleaned'][0])




#

    # to have more data going to assign numbers to genre data
    genres = df['genre'].unique()  # need to assign unique elements in genre column a number for analysis later
    # print(genres)
    # mapping genres for kmeans later
    genre_mapping = {'pop': 1, 'country': 2, 'blues': 3, 'rock': 4, 'jazz': 5, 'reggae': 6, 'hip hop': 7}
    df['genre_mapping'] = df['genre'].map(genre_mapping)
    # print(df.columns)
    # print(df['genre_mapping'])

    # now to do the same with topic column
    topics = df['topic'].unique()  # need to assign unique elements in genre column a number for analysis later
    # print(topics)
    # mapping topics for kmeans later
    topic_mapping = {'sadness': 1, 'world/life': 2, 'music': 3, 'romantic': 4, 'violence': 5, 'obscene': 6,
                     'night/time': 7, 'feelings': 8}
    df['topic_mapping'] = df['topic'].map(topic_mapping)
    # print(df.columns)
    # print(df['topic_mapping'])

    # making new dataframe with relevant columns
    df_relevant_columns = df.drop(columns=['artist_name', 'track_name', 'len', 'genre', 'topic'], axis=1)
    # print(df_relevant_columns.columns)
    # print(df_relevant_columns)

    # Checking the aesthtic by decade
    Year_df = df_relevant_columns.drop(columns=['Unnamed: 0', 'genre_mapping', 'topic_mapping', 'age'], axis=1)
    Year_1950_1960s_df = Year_df[(df['release_date'] >= 1950) & (df['release_date'] <= 1960)] # need to do this until 2010....
    aggregateYear = Year_1950_1960s_df.groupby('release_date', as_index=False).mean(numeric_only=True)
    aestheticYear = px.bar(aggregateYear, x="release_date", y=Year_1950_1960s_df.columns ,barmode='group')
    aestheticYear.show()

    # Checking the aesthtic by year
    genre_df = df_relevant_columns.drop(columns=['Unnamed: 0', 'genre_mapping', 'topic_mapping', 'age', 'release_date'], axis=1)
    aggregate = df.groupby('genre', as_index=False).mean(numeric_only=True) # way too much data, so aggregate and get mean or use sample and choose a small random subset
    aesthetic = px.bar(aggregate, x="genre", y=genre_df.columns ,barmode='group')
    aesthetic.show()

    


if __name__ == '__main__':
    main()
