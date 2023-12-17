from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def req():

    artist = request.form.get('artist')
    song = request.form.get('song')

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

    return render_template('index.html')

if __name__ == '__main__':
    app.run()