from sklearn.cluster import KMeans

def kmeans_lvf_model(df,uisDATA):
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