from dotenv import load_dotenv
import os
from requests import post, get
import json
import base64
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 

USER = "wtna1cbeqe542xcjuusmshtx1"
CHILL_HOUSE = "summer fun chill dance?? yes"

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    """Request access token"""
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
name = ["Jane Remover"]
result = sp.search(name) 
result['tracks']['items'][1]['artists']


#Extract Artist's uri
artists_uris = result['tracks']['items'][0]['artists'][0]['uri']
#Pull all of the artist's albums
artist_albums = sp.artist_albums(artists_uris, album_type='album')
#Store artist's albums' names' and uris in separate lists
artist_album_names = []
artist_album_uris = []
for i in range(len(artist_albums['items'])):
    artist_album_names.append(artist_albums['items'][i]['name'])
    artist_album_uris.append(artist_albums['items'][i]['uri'])
    
artist_album_names
artist_album_uris
#Keep names and uris in same order to keep track of duplicate albums


def album_songs(uri):
    album = uri 
    spotify_albums[album] = {}
    #Create keys-values of empty lists inside nested dictionary for album
    spotify_albums[album]['album'] = [] 
    spotify_albums[album]['track_number'] = []
    spotify_albums[album]['id'] = []
    spotify_albums[album]['name'] = []
    spotify_albums[album]['uri'] = []
    #pull data on album tracks
    tracks = sp.album_tracks(album) 
    for n in range(len(tracks['items'])): 
        spotify_albums[album]['album'].append(artist_album_names[album_count]) 
        spotify_albums[album]['track_number'].append(tracks['items'][n]['track_number'])
        spotify_albums[album]['id'].append(tracks['items'][n]['id'])
        spotify_albums[album]['name'].append(tracks['items'][n]['name'])
        spotify_albums[album]['uri'].append(tracks['items'][n]['uri'])


spotify_albums = {}
album_count = 0
for i in artist_album_uris: #each album
    album_songs(i)
    print(str(artist_album_names[album_count]) + " album songs has been added to spotify_albums dictionary")
    album_count+=1 #Updates album count once all tracks have been added




def audio_features(track):
    #Add new key-values to store audio features
    spotify_albums[track]['acousticness'] = []
    spotify_albums[track]['danceability'] = []
    spotify_albums[track]['energy'] = []
    spotify_albums[track]['instrumentalness'] = []
    spotify_albums[track]['liveness'] = []
    spotify_albums[track]['loudness'] = []
    spotify_albums[track]['speechiness'] = []
    spotify_albums[track]['tempo'] = []
    spotify_albums[track]['valence'] = []
    spotify_albums[track]['popularity'] = []
    

    

def get_playlist(user_id, playlist_name) -> str:
    """ Enter exact user id and playlist name, and retrieve the playlist id
        The playlist id is used later to access all items"""
    playlists = sp.user_playlists(user_id)
    
    playlist = None
    for item in playlists["items"]:
        if item["name"] == playlist_name:
            playlist = item
    # print(playlist)
    playlist_id = playlist["id"]
    return playlist_id    

def load_playlist(playlist_id):
    playlist = sp.playlist_items(playlist_id)
    
    track_ids = [item["track"]["id"]
                    for item in playlist["items"]
                    if item.get("track") and item["track"].get("id")]

    print(track_ids)
    features = sp.audio_features(track_ids)  # returns list of dicts    
    # print(features)




token = get_token()

if __name__ == "__main__":

    playlist_id = get_playlist(USER, CHILL_HOUSE)
    playlist = load_playlist(playlist_id)


    # for item in results["items"]:
    #     track = item["track"]
    #     if track is None:
    #         continue
    #     print(track["name"], "-", track["artists"][0]["name"])


