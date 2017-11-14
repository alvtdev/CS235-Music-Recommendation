import spotipy
import spotipy.util as util
import sys
import os
import pprint
from spotipy.oauth2 import SpotifyClientCredentials

scope = 'user-library-read'

def getArtistGenres(uri, sp):
    artist = sp.artist(uri)
    return artist['genres']

def getAlbumGenres(uri, sp):
    album = sp.album(uri)
    return album['genres']

def getSavedMusic():
    #get id & secret locally stored on device
    #client_id = os.getenv('SPOTIPY_CLIENT_ID')
    #client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    #user authentication
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print "Enter your Spotify username: ",
        username = raw_input()

    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        track_results = sp.current_user_saved_tracks()
        for item in track_results['items']:
            track = item['track']
            print track['name'] + ' - ' + track['artists'][0]['name'] + ' - ',
            print track['album']['name'] + ' - ',
            genres = getArtistGenres(track['artists'][0]['uri'], sp)
            print genres
            #print track
            #print "\n"
    else:
        print "Can't get token for", username

def main():
    getSavedMusic()
'''
    credentials = SpotifyClientCredentials(client_id=client_id,
            client_secret=client_secret)
    token = credentials.get_access_token()
    sp = spotipy.Spotify(auth=token)
    sp.trace=False;
    #sp = spotipy.Spotify(client_credentials_manager=credentials)

    playlists = sp.user_playlists('spotify')
'''


if __name__ == "__main__":
    main()
