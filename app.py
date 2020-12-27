from flask import Flask, request, redirect, jsonify, json
import time
import jiosaavn
import os
from traceback import print_exc
from flask_cors import CORS
import spotify
import secrets

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return jsonify({"status":"The API is healthy"})

@app.route('/getuser')
def test():
    spotify_user=spotify.get_spotify_user()
    if spotify_user:
        return spotify_user
    else:
        return {"status":spotify_user}

@app.route('/playlist/')
def playlist():
    query = request.args.get('query')
    if(request.args.get('bearer')):
        secrets.BEARER_TOKEN = request.args.get('bearer')
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
            return jsonify({"Spotify URL":playlist_url})
        else:
            return jsonify({'status':"Error"})
    else:
        error = {
            "status": False,
            "error":'Query is required to search playlists!'
        }
        return jsonify(error)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4000, use_reloader=True, threaded=True)
