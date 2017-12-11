import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import sys
import os
import pprint
import json

#global vars necessary for spotipy functions
playlistsfile = "plsongs.tsv"
topsongsfile = "topsongs.txt"
scope = 'user-library-read'
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
client_uri = os.getenv('SPOTIPY_REDIRECT_URI')
cache = ""
username = "" 

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Enter your Spotify username: ",
    username = raw_input()

cache = '.cache-' + username

def getArtistGenres(uri, sp):
    artist = sp.artist(uri)
    return artist['genres']

def getAlbumGenres(uri, sp):
    album = sp.album(uri)
    return album['genres']

def printTrackDetails(sp, tracks):
    i = 1
    
    while True:
        for item in tracks['items']:
            track = item['track']
            print track['name'] + ' - ' + track['artists'][0]['name'] + ' - ',
            print track['album']['name'] + ' - ',
            genres = getArtistGenres(track['artists'][0]['uri'], sp)
            genreList = [genre.encode('UTF8') for genre in genres]
            print genreList
            #song_title = str(i) + '. ' + track['name'] +' - '
            #song_title += track['artists'][0]['name']
            #print(song_title)
            i += 1
        #check if there are more pages
        if tracks['next']:
            tracks = sp.next(tracks)
        else: 
            break

#function to generate a comma delimited file with data
def printTracksToFile(sp, tracks, F):
    i = 1
    dataHeader = "Song Name \t Artist Name \t Genres \t "
    dataHeader += "Acousticness \t Danceability \t Energy \t"
    dataHeader += "Instrumentalness \t Liveness \t Speechiness \n"
    F.write(dataHeader)
    pp = pprint.PrettyPrinter(depth=6)
    while True:
        for item in tracks['items']:
            track = item['track']
            uri = [track['uri'].split(":")[2]]
            trackinfo = sp.audio_features(uri)

            #append track metadata to string, tab separated
            trackdata = track['name'] + "\t" + track['artists'][0]['name'] + "\t"
            #trackdata += track['album']['name'] + '\t'
            genres = getArtistGenres(track['artists'][0]['uri'], sp)
            genreList = [genre.encode('UTF8') for genre in genres]
            for genre in genres:
                trackdata += genre + "," 
            trackdata = trackdata[:-1] +"\t"

            #append other characteristics from audio_features()
            trackdata += str(trackinfo[0]['acousticness']) + "\t" 
            trackdata += str(trackinfo[0]['danceability']) + "\t" 
            trackdata += str(trackinfo[0]['energy']) + "\t" 
            trackdata += str(trackinfo[0]['instrumentalness']) + "\t" 
            trackdata += str(trackinfo[0]['liveness']) + "\t" 
            trackdata += str(trackinfo[0]['speechiness']) + "\t" 
        
            #print trackdata
            F.write(trackdata + "\n")
            i += 1
        #check if there are more pages
        if tracks['next']:
            tracks = sp.next(tracks)
        else: 
            break

def printPlaylist(sp, playlist, F):
    results = sp.user_playlist(playlist['owner']['id'], playlist['id'], fields='tracks,next')
    tracks = results['tracks']
    #printTrackDetails(sp, tracks)
    printTracksToFile(sp, tracks, F)

def getPlaylists(sp, username):
    playlists = sp.user_playlists(username)
    filename = "playlists-" + username + ".txt"
    F = open(filename, "w")
    while True:
        for playlist in playlists['items']:
            if playlist['name'] is not None:
                print '\nplaylist: '
                playlist_name = playlist['name']
                print playlist_name
                printPlaylist(sp, playlist, F)
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            break
    F.close()

def main():
    oauth = SpotifyOAuth(client_id, client_secret, client_uri, scope=scope, cache_path=cache)
    token = ""
    token_info = oauth.get_cached_token()

    if token_info:
        token = token_info['access_token']
    else:
        url = oauth.get_authorize_url()
        code = oauth.parse_response_code(url)
        if code:
            token_info = oauth.get_access_token(code)
            token = token_info['access_token']
    if token:
        sp = spotipy.Spotify(auth=token)
        getPlaylists(sp, username)


if __name__ == "__main__":
    main()
