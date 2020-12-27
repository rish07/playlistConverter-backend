from typing import Optional
from fastapi import FastAPI
import os
from traceback import print_exc
from converters.jio_spotify.jio_to_spotify import convert_jio_to_spotify
import providers.secrets as secrets
from providers.spotify import get_spotify_user
app = FastAPI()



@app.get('/')
def home():
    return {"status":"The API is healthy"}

@app.get('/getuser')
def getUser():
    spotify_user=get_spotify_user()
    if spotify_user:
        return spotify_user
    else:
        return {"status":spotify_user}

@app.get('/playlist/')
async def playlist(query: str,converter:int,bearer:Optional[str]=None):
    if(bearer):
        secrets.BEARER_TOKEN = bearer
    if query:
        response = ""
        if converter == 0: #JioSaavn to Spotify
            response = convert_jio_to_spotify(query)
        return response


    else:
        error = {
            "status": False,
            "error":'Query is required to search playlists!'
        }
        return {"Error":error}



