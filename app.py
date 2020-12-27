from typing import Optional
from fastapi import FastAPI
import jiosaavn
import os
from traceback import print_exc
import spotify
import secrets

app = FastAPI()



@app.get('/')
def home():
    return {"status":"The API is healthy"}

@app.get('/getuser')
def test():
    spotify_user=spotify.get_spotify_user()
    if spotify_user:
        return spotify_user
    else:
        return {"status":spotify_user}

@app.get('/playlist/')
async def playlist(query: str,bearer:Optional[str]=None):
    query = query
    if(bearer):
        secrets.BEARER_TOKEN = bearer
    if query:
        id = jiosaavn.get_playlist_id(query)
        playlist_name = jiosaavn.get_playlist(id)['listname']
        songs = jiosaavn.get_playlist(id)['songs']
        song_names = []
        for song in songs:
            song_names.append(song['song'])
        spotify_id=spotify.get_spotify_user()['id']
        uris = spotify.get_song_uris(song_names)
        playlist_id,playlist_url = spotify.create_playlist(playlist_name,spotify_id)
        success = spotify.append_playlist(uris,playlist_id)
        if success:
            return {"Spotify URL":playlist_url}
        else:
            return {'status':"Error"}
    else:
        error = {
            "status": False,
            "error":'Query is required to search playlists!'
        }
        return {"Error":error}



