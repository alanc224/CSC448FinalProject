import numpy as np
import pandas as pd
import string
from dotenv import load_dotenv
import os
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier,KNeighborsRegressor
from sklearn.manifold import TSNE
from factor_analyzer import calculate_bartlett_sphericity, calculate_kmo, FactorAnalyzer
import spotipy
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# Konrad -- Make sure .env variables have the same name
load_dotenv()
SPOTIFY_KEY1 = os.getenv('SPOTIFY_KEY1')
SPOTIFY_KEY2 = os.getenv('SPOTIFY_KEY2')
SPOTIFY_DATA = os.getenv('SPOTIFY_DATA')
TCC_DATA = os.getenv('TCC_DATA')

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIFY_KEY1,SPOTIFY_KEY2))


def nn_model(df,uisDATA,df_relevant_columns,artist_name,song_name):
        scaler = MaxAbsScaler()
        X = scaler.fit_transform(df_relevant_columns)

        k = NearestNeighbors(n_neighbors=8, metric='euclidean', algorithm='brute')
        k.fit(X)

        # Extract features for the input song
        input_song_details = uisDATA[df_relevant_columns.columns]
        input_song_aesthetic = scaler.transform(input_song_details)
        print(input_song_details) # Sanity check
        print(input_song_aesthetic)

        scaler.fit_transform(df_relevant_columns)
        distance, indices = k.kneighbors(input_song_aesthetic)
        recommended_songs = df.iloc[indices.flatten()][['artists', 'name']]

        # having issues with same songs showing up i.e Artist: Taylor Swift Track: I Knew You Were Trouble, showing up 3 times since there is like 5 versions, here is a hack fix
        # only issue is if song that is inputted is NOT in dataset wont have dupes and it just ends up ommiting a song
        recommended_songs = recommended_songs.drop_duplicates()
        return recommended_songs.head(6)[1:]


def getid(artist_name, song_name):
    artistname = artist_name.strip("['']")
    results = spotify.search(q="track" + song_name + "artists" + artistname, type="track", limit=1)
    if "tracks" in results and "items" in results["tracks"]:
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
    AP = track['preview_url']
    if AP is None:
        print("No Audio Preview available")
    else:
        print('Audio Preview: ' + track['preview_url'])
    print('Cover Art: ' + track['album']['images'][0]['url'])


def main():
    df_spotify = pd.read_csv(SPOTIFY_DATA)
    df_spotify.dropna()
    df_spotify.drop_duplicates()

    # Testing spotify api, works so far
    found = False
    while not found:
        track_id = input("Enter uri: ")
        if spotify.track(track_id):
            found = True

    track = spotify.track(track_id)
    print_info(track)
    artist_name = track['artists'][0]['name']
    song_name = track['name']
    song_features = spotify.audio_features(track_id)
    songDF = pd.DataFrame(song_features)
    songDF = songDF.drop(columns=['track_href','analysis_url','type','id','uri','time_signature','mode','key','duration_ms','tempo',])
    # print(songDF)

    # Using content based filtering
    # making new dataframe with relevant columns
    df_relevant_columns = df_spotify.drop(columns=['id','name','release_date','artists','year', 'explicit', 'popularity','mode','key','duration_ms','tempo'], axis=1)
    df_relevant_columns.dropna(inplace=True)
    chi_square_value,p_value=calculate_bartlett_sphericity(df_relevant_columns)
    print(chi_square_value, p_value)
    kmo_all,kmo_model=calculate_kmo(df_relevant_columns)
    print(kmo_model)

    fa = FactorAnalyzer()
    fa.fit(df_relevant_columns, 25)
    # Check Eigenvalues
    ev, v = fa.get_eigenvalues()
    # print(ev)

    plt.scatter(range(1,df_relevant_columns.shape[1]+1),ev)
    plt.plot(range(1,df_relevant_columns.shape[1]+1),ev)
    plt.title('Scree Plot')
    plt.xlabel('Factors')
    plt.ylabel('Eigenvalue')
    plt.grid()
    plt.show()

    fa.set_params(n_factors=4, rotation="varimax")
    fa.fit(df_relevant_columns)
    # print(fa.loadings_)
    print(fa.get_factor_variance())


    print(df_relevant_columns.columns) # sanity check
    print(nn_model(df_spotify,songDF,df_relevant_columns,artist_name,song_name))

    


if __name__ == '__main__':
    main()
