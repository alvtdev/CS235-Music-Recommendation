import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import sys
import os
import pprint
import json
from bottle import route, run, request

#global vars necessary for spotipy functions
scope = 'user-library-read'
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
client_uri = os.getenv('SPOTIPY_REDIRECT_URI')
cache = ""

def getArtistGenres(uri, sp):
    artist = sp.artist(uri)
    return artist['genres']

def getAlbumGenres(uri, sp):
    album = sp.album(uri)
    return album['genres']

def getSavedMusic(sp):

    #if oauth._is_token_expired(token):
    #   oauth.refresh_access_token(token)
    track_results = sp.current_user_saved_tracks(limit=50)
    for item in track_results['items']:
        track = item['track']
        print track['name'] + ' - ' + track['artists'][0]['name'] + ' - ',
        print track['album']['name'] + ' - ',
        genres = getArtistGenres(track['artists'][0]['uri'], sp)
        print genres
        #print track
        #print "\n"

#@route('/')
def main():
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print "Enter your Spotify username: ",
        username = raw_input()

    cache = '.cache-' + username
    oauth = SpotifyOAuth(client_id, client_secret, client_uri, scope=scope, cache_path=cache)
    token = ""
    token_info = oauth.get_cached_token()
    #print "Token info: ",
    #print token_info

    if token_info:
        token = token_info['access_token']
        #print token
    else:
        url = oauth.get_authorize_url()
        code = oauth.parse_response_code(url)
        if code:
            token_info = oauth.get_access_token(code)
            token = token_info['access_token']

    sp = spotipy.Spotify(auth=token)
    getSavedMusic(sp)


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
