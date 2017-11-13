import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials


def main():
    #get id & secret
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    playlists = sp.user_playlists('spotify')
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print ("%4d $s $s" % (i + 1 + playlists['offset'], playlist['uri'],
                playlist['name']))
            if playlists['next']:
                playlists = sp.next(playlists)
            else:
                playlists = None


if __name__ == "__main__":
    main()
