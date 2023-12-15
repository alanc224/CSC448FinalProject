import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
from factor_analyzer import calculate_bartlett_sphericity, calculate_kmo, FactorAnalyzer
import spotipy
from sklearn.preprocessing import StandardScaler
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns


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