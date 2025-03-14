import pickle
import pandas as pd
import numpy as np
from flask import Flask, jsonify
from flask_cors import CORS

from ..utils import get_track_features, get_track_analysis, get_track_info
from ..model import Result

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route("/api/predict/<song_id>", methods=['GET'])
def songsavvy(song_id):
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

    return jsonify({ result: result.to_json() }), 200


if __name__ == "__main__":
    app.run(debug=true)

