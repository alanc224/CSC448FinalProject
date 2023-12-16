import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
from factor_analyzer import calculate_bartlett_sphericity, calculate_kmo, FactorAnalyzer
import spotipy
from sklearn.preprocessing import StandardScaler, MaxAbsScaler
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns


def nn_model(df,uisDATA,df_relevant_columns):
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