import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_track_features(song_id):
    track_features = spotify.audio_features(tracks=[song_id])[0]

    features = [
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "duration_ms",
        "time_signature",
    ]

    features_value_list = []

    if track_features is None:
        return None

    for feature in features:
        features_value_list.append(track_features[feature])

    return features_value_list


def get_required_track_analysis(song_id):
    track_analysis = spotify.audio_analysis(song_id)

    sections = track_analysis["sections"]
    chorus_hit = sections[2]["start"]

    return [chorus_hit, len(sections)]


def get_track_info(song_id):
    track = spotify.track(song_id)
    image_url = track["album"]["images"][0]["url"]
    album_name = track["album"]["name"]
    release_type = track["album"]["album_type"]
    track_name = track["name"]
    song_url = track["external_urls"]["spotify"]
    # return track['artists'][0]['name'], track_name, album_name, image_url, release_type
    return track["artists"], track_name, album_name, image_url, release_type, song_url
