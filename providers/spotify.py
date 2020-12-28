# pylint: disable=import-error

import requests
import providers.endpoints as endpoints
import json
import providers.secrets as secrets
import helper

def get_spotify_user():
    response = requests.get(endpoints.spotify_user_details,headers={'Authorization': secrets.BEARER_TOKEN})
    if response.status_code==200:
        return response.json()
    else:
        return 0

def get_song_uris(song_list):
    song_uris = []

    for song in song_list:
       
        response = requests.get(
        endpoints.spotify_track_search+song+"&type=track&market=US&limit=1",headers={'Authorization': secrets.BEARER_TOKEN})
        if response.status_code == 200:
            if(len(response.json()['tracks']['items'])!=0):
                song_uris.append(response.json()['tracks']['items'][0]['uri'])
    return song_uris
        

def append_playlist(song_uris,playlist_id):
    response = requests.post(endpoints.spotify_playlist_append+str(playlist_id)+"/tracks",headers={'Authorization': secrets.BEARER_TOKEN},json={
            "uris":song_uris
        })
    
    if response.status_code==201:
        return True
    else:
        return False
        
def create_playlist(playlist_name,user_id):
    response = requests.post(endpoints.spotify_create_playlist+str(user_id)+"/playlists",headers={'Authorization': secrets.BEARER_TOKEN},json={
            "name":playlist_name
        })
    if response.status_code==201:
        
        return response.json()['id'],response.json()['external_urls']['spotify']
    else:
        return Exception
    
def get_playlist_details(playlist_url,token):
    songs = []
    id = helper.get_spotify_playlist_id(playlist_url)
    response = requests.get(endpoints.spotify_playlist_detail+id,headers={'Authorization': token})
    
    all_songs=response.json()['tracks']['items']
    for song in all_songs:
        if "(" in song['track']['name']:
            songs.append(song['track']['name'].split("(")[0])
        else:
            songs.append(song['track']['name'])
    return songs
