from flask import Flask, render_template, request
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import string

# IMPLEMENTED ON 12/15/2023

app = Flask(__name__)

load_dotenv()
SPOTIFY_KEY1 = '798c070d2d5e4ab98b36353e469dba19' # To prevent the need for authentification, we will delete this once the semester is over
SPOTIFY_KEY2 = 'ec5f36a15c864212a84ab03d15fc7c74'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIFY_KEY1,SPOTIFY_KEY2))

@app.route('/', methods=['GET','POST'])
def req():
    song_exists = False

    if request.method == 'POST':
        song_exists = True
        artist = request.form.get('artist')
        song = request.form.get('song')

        print(artist)
        print(song)

        song_exists = True
        track_id = getid(artist, song)

        if track_id == None:
            song_exists = False
            alert_user = "This combination of artist and song is not recognized :("
            return render_template('index.html', alert_user=alert_user, 
                                            song_exists=song_exists)
        
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

        return render_template('index.html', song_exists=song_exists,
                                            Cur_Artist=Cur_Artist,
                                            Cur_Track=Cur_Track,
                                            Cur_Album=Cur_Album,
                                            Cur_Audio_Preview=Cur_Audio_Preview,
                                            Cur_Cover_Art=Cur_Cover_Art)
    
    return render_template('index.html', song_exists=song_exists)

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
    print('Audio Preview: ' + track['preview_url'])
    print('Cover Art: ' + track['album']['images'][0]['url'])


if __name__ == '__main__':
    app.run()

# IMPLEMENTED ON 12/16/2023
    
def is_valid_spotify_uri(uri):
    # Define a regular expression pattern for a Spotify URI
    spotify_uri_pattern = r'^spotify:track:[a-zA-Z0-9]+$'

    # Check if the input URI matches the pattern
    if re.match(spotify_uri_pattern, uri):
        return True
    else:
        return False