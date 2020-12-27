# pylint: disable=import-error
from providers.spotify import get_spotify_user,get_song_uris,create_playlist,append_playlist
from providers.jiosaavn import get_playlist, get_playlist_id


def convert_jio_to_spotify(url):
    id = get_playlist_id(url)
    playlist_name = get_playlist(id)['listname']
    songs = get_playlist(id)['songs']
    song_names = []
    for song in songs:
        song_names.append(song['song'])
    if(get_spotify_user()!=0):
        spotify_id=get_spotify_user()['id']
        uris = get_song_uris(song_names)
        if len(uris)!=0:
            playlist_id,playlist_url = create_playlist(playlist_name,spotify_id)
            success = append_playlist(uris,playlist_id)
            if success:
                return {"Spotify URL":playlist_url}
            else:
                return {'Error':"Error in generating spotify playlist"}
        else:
            return {'Error':"Error is song URI generation"}
    else:
        return {'Error':"Spotify user not found"}
