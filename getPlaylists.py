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
#client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_id = "c99e7cb3f74441b4be09fa5e6406055e"
#client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
client_secret = "373e4b91a7b74bdab6dc02bfa8236a03"
#client_uri = os.getenv('SPOTIPY_REDIRECT_URI')
client_uri = "http://localhost/"
cache = ""
username = "" 

#initial input checking
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Enter your Spotify username: "),
    username = raw_input()

cache = '.tokencache'

#get spotify artist uri 
def getArtistGenres(uri, sp):
    artist = sp.artist(uri)
    return artist['genres']

#get album genres given uri
def getAlbumGenres(uri, sp):
    album = sp.album(uri)
    return album['genres']

#function to generate a comma delimited file with data
def printTracksToFile(sp, tracks, F):
    i = 1
    while True:
        for item in tracks['items']:
            track = item['track']
            uri = [track['uri'].split(":")[2]]
            trackinfo = sp.audio_features(uri)

            artistURI = track['artists'][0]['uri'];
            #if artist exists
            if artistURI:
                #append track metadata to string, tab separated
                trackdata = track['name'].encode('utf-8') + "\t"
                trackdata += track['artists'][0]['name'].encode('utf-8') + "\t"
                genres = getArtistGenres(artistURI, sp)
                genreList = [genre.encode('utf-8') for genre in genres]
                if len(genreList) > 0:
                    for genre in genres:
                        trackdata += genre.encode('utf-8')+ "," 
                    trackdata = trackdata[:-1] +"\t"
                else:
                    trackdata += "none \t"

                #append other characteristics from audio_features()
                trackdata += str(trackinfo[0]['acousticness']) + "\t" 
                trackdata += str(trackinfo[0]['danceability']) + "\t" 
                trackdata += str(trackinfo[0]['energy']) + "\t" 
                trackdata += str(trackinfo[0]['instrumentalness']) + "\t" 
                trackdata += str(trackinfo[0]['liveness']) + "\t" 
                trackdata += str(trackinfo[0]['speechiness'])
            
                #print trackdata to file
                F.write(trackdata + "\n")
            i += 1
        #check if there are more tracks
        if tracks['next']:
            tracks = sp.next(tracks)
        else: 
            break

#intermediate function that calls printTracksToFile for a given playlist
def printPlaylist(sp, playlist, F):
    results = sp.user_playlist(playlist['owner']['id'], playlist['id'], 
            fields='tracks,next')
    tracks = results['tracks']
    printTracksToFile(sp, tracks, F)

#function that goes through a user's playlists and calls other helper
#helper functions to print the contents to file 
def getPlaylists(sp, username):
    playlists = sp.user_playlists(username)
    #custom tsv name
    filename = "playlists-" + username + ".tsv"
    #print tsv header
    F = open(filename, "w")
    dataHeader = "Song Name \t Artist Name \t Genres \t "
    dataHeader += "Acousticness \t Danceability \t Energy \t"
    dataHeader += "Instrumentalness \t Liveness \t Speechiness \n"
    F.write(dataHeader)
    #iterate through playlists and print them to file
    print("Getting Data...")
    while True:
        for playlist in playlists['items']:
            if playlist['name'] is not None:
                print('playlist: '),
                playlist_name = playlist['name']
                print(playlist_name)
                printPlaylist(sp, playlist, F)
        #check if there are any more playlists
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            break
    F.close()

def main():
    #program authentication
    oauth = SpotifyOAuth(client_id, client_secret, client_uri, scope=scope, 
            cache_path=cache)
    #obtain authentication token
    token = ""
    token_info = oauth.get_cached_token()

    if token_info:
        #token = token_info['access_token']
        token_info = oauth.refresh_access_token(token_info['refresh_token']) 
        token = token_info['access_token']

    #FIXME: program authentication when no tokens have been used before
    else:
        #print("GET NEW TOKEN")
        url = oauth.get_authorize_url()
        #print(url)
        code = oauth.parse_response_code(url)
        #print(code)
        if code:
            #print("CODE FOUND")
            token_info = oauth.get_access_token(code)
            token = token_info['access_token']

    #if authentication token exists, crawl and create dataset
    if token:
        sp = spotipy.Spotify(auth=token)
        getPlaylists(sp, username)
    else:
        print("ERROR: TOKEN NOT FOUND") 


if __name__ == "__main__":
    main()
