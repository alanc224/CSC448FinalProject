import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials('798c070d2d5e4ab98b36353e469dba19',
                                                                              'ec5f36a15c864212a84ab03d15fc7c74'))


def getid(artist_name, song_name):
    results = spotify.search(q="track" + song_name + "artist:" + artist_name, type="track", limit=1)

    if "tracks" in results and "items" in results["tracks"]:
        return results["tracks"]["items"][0]["id"]
    else:
        print("Track not found.")
        return None


def name_lookup(name, df):
    lookup = df[df['artist_name'].str.lower() == name.lower()]

    if not lookup.empty:
        return name
    else:
        print("Artist not found")
        exit()


def song_lookup(song, df):
    lookup = df[df['track_name'].str.lower() == song.lower()]

    if not lookup.empty:
        return song
    else:
        print("Song not found.")
        exit()


def print_info(track):
    print('\nArtist: ' + track['artists'][0]['name'])
    print('Track: ' + track['name'])
    print('Album: ' + track['album']['name'])
    print('Audio Preview: ' + track['preview_url'])
    print('Cover Art: ' + track['album']['images'][0]['url'])


def main():
    df = pd.read_csv('../Documents/tcc_ceds_music.csv')
    df.drop_duplicates(subset=['track_name'], keep='first', inplace=True)
    print(df.columns)
    # x = df.genere
    print(x)


''' Testing spotify api, works so far
    artist_name = input("Enter artist name: ")
    artist_name = name_lookup(artist_name, df)
    song_name = input("Enter song name: ")
    song_name = song_lookup(song_name, df)

    track_id = getid(artist_name, song_name)

    track = spotify.track(track_id)
    print_info(track)
    '''

if __name__ == '__main__':
    main()
