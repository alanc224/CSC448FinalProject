import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
from sklearn.manifold import TSNE
from factor_analyzer import calculate_bartlett_sphericity, calculate_kmo, FactorAnalyzer
import spotipy
from sklearn.preprocessing import StandardScaler
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

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


def nn_model(df,df_relevant_columns,artist_name,song_name):
        scaler = StandardScaler()
        artistname = "['{}']".format(artist_name)

        X = df_relevant_columns.drop('popularity', axis = 1)
        y = df_relevant_columns['popularity']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        # Scale the features using StandardScaler
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        # find optimal k
        print("Finding optimal k...")
        k_values = [i for i in range (1,12)]
        scores = []
        X = scaler.fit_transform(X)

        for k in k_values:
            print("im here",k)
            knn = KNeighborsClassifier(n_neighbors=k)
            score = cross_val_score(knn, X, y, cv=5)
            scores.append(np.mean(score))
        
        sns.lineplot(x = k_values, y = scores, marker = 'o')
        plt.xlabel("K Values")
        plt.ylabel("Accuracy Score")
        print("Done...")

        k = KNeighborsClassifier(n_neighbors=3)
        print("Fitting data...")
        k.fit(X_train,y_train)
        y_pred = k.predict(X_test)
        print("Done")

        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy:", accuracy)

        '''# Getting values from input song, and attempting to train model
        input_song_details = df[(df['name'] == song_name) & (df['artists'] == artistname)][df_relevant_columns.columns]
        input_song_aesthetic = scaler.transform(input_song_details)
        print(input_song_details) # sanity check
        # print(input_song_aesthetic)

        distance, indices = k.kneighbors(input_song_aesthetic)
        recommended_songs = df.iloc[indices.flatten()][['artists', 'name']].iloc[1:][:5]
'''
        

        return 0



def getid(artist_name, song_name):
    artistname = artist_name.strip("['']")
    results = spotify.search(q="track" + song_name + "artist" + artistname, type="track", limit=1)
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
    '''df_spotify.drop_duplicates(subset=None, inplace=True)
    dupes = df_spotify[(df_spotify['name'].str.contains('Neon')) & (df_spotify['artists'].str.contains('John Mayer'))]
    print(dupes[['name', 'artists']])'''
    # need to drop dupes of same songs but contain extra words as seen in example above

    '''print(df_spotify.head())
    print(df_spotify.shape)'''

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

# Preprocessing the lyrics
    '''
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
'''

#
    
    # Using content based filtering
    # making new dataframe with relevant columns
    df_relevant_columns = df_spotify.drop(columns=['id','name','release_date','artists'], axis=1)
    df_relevant_columns.dropna(inplace=True)
    chi_square_value,p_value=calculate_bartlett_sphericity(df_relevant_columns)
    print(chi_square_value, p_value)
    kmo_all,kmo_model=calculate_kmo(df_relevant_columns)
    print(kmo_model)

    fa = FactorAnalyzer()
    fa.fit(df_relevant_columns, 25)
    # Check Eigenvalues
    ev, v = fa.get_eigenvalues()
    print(ev)

    plt.scatter(range(1,df_relevant_columns.shape[1]+1),ev)
    plt.plot(range(1,df_relevant_columns.shape[1]+1),ev)
    plt.title('Scree Plot')
    plt.xlabel('Factors')
    plt.ylabel('Eigenvalue')
    plt.grid()
    plt.show()

    fa.set_params(n_factors=4, rotation="varimax")
    fa.fit(df_relevant_columns)
    print(fa.loadings_)
    print(fa.get_factor_variance())


    print(df_relevant_columns.columns) # sanity check
    print(nn_model(df_spotify,df_relevant_columns,track['artists'][0]['name'],track['name'])) # using track['name'] as a lazy fix for songs like "the arms of sorrow" -> "The Arms of Sorrow"

    


if __name__ == '__main__':
    main()
