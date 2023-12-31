import pandas as pd
from dotenv import load_dotenv
import os
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import FeatureAgglomeration, KMeans
import spotipy
from sklearn.preprocessing import StandardScaler
from spotipy.oauth2 import SpotifyClientCredentials

# Konrad -- Make sure .env variables have the same name
load_dotenv()
# SPOTIFY_KEY1 = '' # To prevent the need for authentification, we will change this once semester is over
# SPOTIFY_KEY2 = ''
SPOTIFY_DATA = os.getenv('SPOTIFY_DATA')

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIFY_KEY1,SPOTIFY_KEY2))

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


def nn_model(df,uisDATA):
        
    df_relevant_columns = df.drop(columns=['id','name','release_date','artists','year','duration_ms','liveness','key','mode','explicit','popularity'], axis=1)
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

def kmeanFS(df, uisDATA):

    features = ['valence', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'loudness', 'mode', 'speechiness', 'tempo' ]
    df_useful_features = df[features]
    input_song_details = uisDATA[df_useful_features.columns]
    model = KMeans(n_clusters=10)
    model.fit(df_useful_features)

    clustered = df.copy()
    clustered['type'] = model.labels_

    print(input_song_details) # Sanity check
    uisDATA = uisDATA.drop(columns = ['analysis_url', 'duration_ms', 'id', 'liveness', 'time_signature', 'track_href', "uri", 'type'])
    uisDATA = uisDATA[['valence', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'loudness', 'mode', 'speechiness', 'tempo']]
    
    test = model.predict(uisDATA)

    suggestions = clustered[clustered.type == test[0]]
    suggestions.drop_duplicates()
    suggestions = suggestions.sample(n=5)

    suggestions = suggestions[['artists', 'name', 'id']]

    return suggestions


def nn_FAR(df,uisDATA):

    df_relevant_columns = df.drop(columns=['id','name','release_date','year','artists','popularity','explicit','duration_ms','key','liveness','speechiness','mode'], axis=1)

    df_song = uisDATA[df_relevant_columns.columns]

    standard = StandardScaler()

    X_standard = standard.fit_transform(df_relevant_columns)
    song_standard = standard.transform(df_song)

    agglo = FeatureAgglomeration(n_clusters = 4)

    X_agglo = agglo.fit_transform(X_standard)
    song_agglo = agglo.transform(song_standard)

    knn_model = NearestNeighbors(n_neighbors=5, metric='euclidean', algorithm='ball_tree')
    knn_model.fit(X_agglo)

    distances, indices = knn_model.kneighbors(song_agglo)
    recommended_songs = df.iloc[indices.flatten()][['artists', 'name', 'id']]

    return recommended_songs

def kmeans_lvf(df,uisDATA):
    features = ['valence','acousticness','energy','instrumentalness','key','loudness','mode','tempo']
    df_lvf = df[features]
    df_song = uisDATA[features]

    kmeans_model = KMeans(n_clusters=10)
    kmeans_model.fit(df_lvf)

    clustered = df.copy()
    clustered['type'] = kmeans_model.labels_

    predictions = kmeans_model.predict(df_song)

    recommendations = clustered[clustered.type == predictions[0]]
    recommendations.drop_duplicates(inplace=True)
    recommendations = recommendations.sample(n=5)
    recommendations = recommendations[['artists', 'name', 'id']]

    return recommendations

def main():
    df_spotify = pd.read_csv(SPOTIFY_DATA)

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


    


if __name__ == '__main__':
    main()
