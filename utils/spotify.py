import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

from utils.spotify_client import SpotifyClient

# load_dotenv()
#
# CLIENT_ID = os.getenv("CLIENT_ID")
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
#
# client_credentials_manager = SpotifyClientCredentials(
#     client_id=CLIENT_ID, client_secret=CLIENT_SECRET
# )
# spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


spotify = SpotifyClient()


def get_track_features(song_id):
    track_features = spotify.get_track_features(song_id);

    if track_features is None:
        raise Exception("No track features")

    track_features = track_features[0]

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
        raise Exception("No track features")

    for feature in features:
        features_value_list.append(track_features[feature])

    return features_value_list

def get_track_analysis(song_id):
    track_analysis = spotify.get_track_analysis(song_id)

    if track_analysis is None:
        raise Exception("No track analysis")

    sections = track_analysis["sections"]
    chorus_hit = sections[2]["start"]

    return [chorus_hit, len(sections)]


def get_track_info(song_id):
    track = spotify.get_track(song_id)

    if track is None:
        raise Exception("No track info")

    image_url = track["album"]["images"][0]["url"]
    album_name = track["album"]["name"]
    release_type = track["album"]["album_type"]
    track_name = track["name"]
    song_url = track["external_urls"]["spotify"]
    return track["artists"], track_name, album_name, image_url, release_type, song_url


