from flask import Flask, render_template, request
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import string

app = Flask(__name__)

load_dotenv()
SPOTIFY_KEY1 = '798c070d2d5e4ab98b36353e469dba19' # To prevent the need for authentification, we will delete this once the semester is over
SPOTIFY_KEY2 = 'ec5f36a15c864212a84ab03d15fc7c74'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIFY_KEY1,SPOTIFY_KEY2))

@app.route('/', methods=['GET','POST'])
def req():
    URI_exists = False

    if request.method == 'POST':
        URI_exists = True
        URI = request.form.get('URI')

        print(URI)

        URI_exists = True
        track_id = URI

        if track_id == None:
            URI_exists = False
            alert_user = "This combination of artist and song is not recognized :("
            return render_template('index.html', alert_user=alert_user, 
                                            URI_exists=URI_exists)
        
        track = spotify.track(track_id)
        print_info(track)

        Cur_Artist = track['artists'][0]['name']
        Cur_Track = track['name']
        Cur_Album = track['album']['name']
        Cur_Audio_Preview = track['preview_url']
        Cur_Cover_Art = track['album']['images'][0]['url']

        track_list = [track_id]
        audio_features_dict = spotify.audio_features(track_list)
        print(audio_features_dict)

        return render_template('index.html', URI_exists=URI_exists,
                                            Cur_Artist=Cur_Artist,
                                            Cur_Track=Cur_Track,
                                            Cur_Album=Cur_Album,
                                            Cur_Audio_Preview=Cur_Audio_Preview,
                                            Cur_Cover_Art=Cur_Cover_Art)
    
    return render_template('index.html', URI_exists=URI_exists)

# Taken from Alan/main.py
def getid(artist_name, song_name):
    if artist_name == None and song_name == None:
        print("On app start")
        return None

    #artistname = artist_name.strip("['']")
    results = spotify.search(q="artist" + artist_name + "track" + song_name, type="track", limit=1)
    SPOTIFY_ARTIST = results["tracks"]["items"][0]['artists'][0]['name']
    if "tracks" in results and "items" in results["tracks"] and SPOTIFY_ARTIST == artist_name:
        return results["tracks"]["items"][0]["id"]
    else:
        print("Track not found.")
        return None

# Taken from Alan/main.py
def name_lookup(name, df):
    formatting_input = "['{}']".format(string.capwords(name))
    lookup = df[df['artists'].str.lower() == formatting_input.lower()]

    if not lookup.empty:
        return formatting_input
    else:
        print("Artist not found")
        return False

# Taken from Alan/main.py
def song_lookup(song, df):
    lookup = df[df['name'].str.lower() == song.lower()]

    if not lookup.empty:
        return string.capwords(song)
    else:
        print("Song not found.")
        return False

# Taken from Alan/main.py
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


if __name__ == '__main__':
    app.run()