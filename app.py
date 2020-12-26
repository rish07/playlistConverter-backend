from flask import Flask, request, redirect, jsonify, json
import time
import jiosaavn
import os
from traceback import print_exc
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET",'thankyoutonystark#weloveyou3000')
CORS(app)


@app.route('/')
def home():
    return jsonify({"status":"The API is healthy"})

@app.route('/playlist/')
def playlist():
    query = request.args.get('query')
    if query:
        id = jiosaavn.get_playlist_id(query)
        songs = jiosaavn.get_playlist(id)['songs']
        song_names = []
        for song in songs:
            song_names.append(song['song'])
        return jsonify({"song_names":song_names})
    else:
        error = {
            "status": False,
            "error":'Query is required to search playlists!'
        }
        return jsonify(error)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4000, use_reloader=True, threaded=True)
