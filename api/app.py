import pandas as pd
import numpy as np
from http.server import BaseHTTPRequestHandler
import json
import pickle
import re

from .model import Result
from .utils import get_track_analysis, get_track_features, get_track_info

model = pickle.load(open("model.pkl", "rb"))


def predict(song_id):
    features = [
        "artist",
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
        "chorus_hit",
        "sections",
        "num_artists",
        "release_type",
    ]

    track_features = get_track_features(song_id)
    analysis_attrs = get_track_analysis(song_id)
    artists, track_name, album, img_url, release_type, song_url = get_track_info(song_id)

    num_artists = len(artists)
    artist = artists[0]["name"]

    input_list = [artist] + track_features + analysis_attrs + [num_artists, release_type]

    model_input = {}

    for i, feature in enumerate(features):
        model_input[feature] = input_list[i]

    input_df = pd.DataFrame(model_input, index=np.ndarray([0]))

    pred = model.predict(input_df)

    result = Result(
        song_id=song_id,
        track_name=track_name,
        album_name=album,
        artist=artist,
        image_url=img_url,
        song_url=song_url,
        result=pred
    )

    return result.to_json()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        match = re.search(r'/api/predict/([^/]+)/?$', self.path)

        if match:
            song_id = match.group(1)

            result = predict(song_id)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            # Handle case where song_id is missing
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing song_id parameter"}).encode())


    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

