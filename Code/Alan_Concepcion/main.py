import numpy as np
import pandas as pd
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


def nn_model(df,uisDATA):
        
        df_relevant_columns = df.drop(columns=['id','name','release_date','artists','year', 'explicit', 'popularity'
                                               ,'mode','key','liveness','duration_ms'], axis=1)
        df_relevant_columns.dropna(inplace=True)
        scaler = StandardScaler() # tested other scalers
        X = scaler.fit_transform(df_relevant_columns)
        k = NearestNeighbors(n_neighbors=7, metric='euclidean', algorithm='ball_tree')
        k.fit(X)

        # Extract features for the input song
        input_song_details = uisDATA[df_relevant_columns.columns]
        input_song_aesthetic = scaler.transform(input_song_details)
        print(input_song_details) # Sanity check
        # print(input_song_aesthetic)

        scaler.fit_transform(df_relevant_columns)
        distance, indices = k.kneighbors(input_song_aesthetic)
        recommended_songs = df.iloc[indices.flatten()][['artists', 'name','id']]

        # having issues with same songs showing up i.e Artist: Taylor Swift Track: I Knew You Were Trouble, showing up 3 times since there is like 5 versions, here is a hack fix
        # only issue is if song that is inputted is NOT in dataset wont have dupes and it just ends up ommiting a song
        recommended_songs = recommended_songs.drop_duplicates()
        return recommended_songs.head(6)[1:]


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
    song_features = spotify.audio_features(track_id)
    songDF = pd.DataFrame(song_features)
    print(songDF)
    songDF = songDF.drop(columns=['track_href','analysis_url','type','id','uri','time_signature'
                                  ,'mode','key','liveness','duration_ms'])
    print(songDF)
    # making new dataframe with relevant columns
    '''df_relevant_columns = df_spotify.drop(columns=['id','name','release_date','artists','year', 'explicit', 'popularity'
                                                   ,'mode','key','liveness','duration_ms'], axis=1)'''
    
    df_relevant_columns = df_spotify.drop(columns=['id','name','release_date','artists','year','duration_ms','liveness','key','mode','explicit','popularity','speechiness'
                                                   ,'tempo'], axis=1)

    # Using content based filtering
    # Using Factor Analysis
    chi_square_value,p_value=calculate_bartlett_sphericity(df_relevant_columns)
    print(chi_square_value, p_value)
    kmo_all,kmo_model=calculate_kmo(df_relevant_columns)
    print("kmo model: ", kmo_model) # this number should be higher than 0.60 and as close to 1.0 as possible
    print("Individual kmo values:")
    print(kmo_all) # If any of the values are less than 0.50, they could be dropped depending on how much value they have to the model, liveness was below 0.50 

    fa = FactorAnalyzer()
    fa.fit(df_relevant_columns, 25)
    # Check Eigenvalues
    ev, v = fa.get_eigenvalues()
    print(ev) # look at the matrix here, how many values above 1.0, in this case its 2 so for n_factors at fa.set_params(n_factors=2, rotation="varimax"), using 2

    plt.scatter(range(1,df_relevant_columns.shape[1]+1),ev) # extra verification with this graph
    plt.plot(range(1,df_relevant_columns.shape[1]+1),ev) # notice that after 2 we don't get significant changes and it just sorta repeats
    plt.title('Scree Plot')
    plt.xlabel('Factors')
    plt.ylabel('Eigenvalue')
    plt.grid()
    plt.show()

    fa.set_params(n_factors=3, rotation="varimax") # using 2 here for n_factors from above
    fa.fit(df_relevant_columns)
    factor_loading_matrix = pd.DataFrame(fa.loadings_, columns=['Factor 1', 'Factor 2','Factor 3'], index=df_relevant_columns.columns.tolist())
    print(factor_loading_matrix) # for further details please read the datacamp link on what these values signify
    factor_get_factor_matrix = pd.DataFrame(fa.get_factor_variance(), columns=['Factor 1', 'Factor 2','Factor 3'],index=['SS Loadings', 'Proportion Var', 'Cumulative Var'])
    print(factor_get_factor_matrix) # for further details please read the datacamp link on what these values signify but tldr look at the last 
                                    # Cumulative Var number in this case it's 0.477090 or 47% 


    print(nn_model(df_spotify,songDF))

    


if __name__ == '__main__':
    main()
