import pandas as pd
from flask import jsonify
from api.songsavvy.v1 import songsavvy_v1_blueprint, model, db
from ..spotify_client import (
    get_track_info,
    get_track_features,
    get_required_track_analysis,
)
from ..models import Results, ResultEnum


@songsavvy_v1_blueprint.route("/predict/<song_id>", methods=["GET"])
def predict(song_id):
    # todo: need to check if the result for this id has already been stored in the db
    # Add code here:
    track_result = Results.query.get(song_id)

    if track_result:
        output = {
            "result": 1 if track_result.result == ResultEnum.HIT else 0,
            "trackName": track_result.track_name,
            "songUrl": track_result.song_url,
            "artist": track_result.artist,
            "album": track_result.album_name,
            "imgUrl": track_result.image_url,
        }
        return jsonify({"result": output}), 200

    # model_output = {}

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

    # Getting required metrics from spotify
    track_features = get_track_features(song_id)
    analysis_attrs = get_required_track_analysis(song_id)
    artists, track_name, album, img_url, release_type, song_url = get_track_info(
        song_id
    )

    num_artists = len(artists)
    artist = artists[0]["name"]

    input_list = (
        [artist] + track_features + analysis_attrs + [num_artists, release_type]
    )

    model_input = {}

    for i, feature in enumerate(features):
        model_input[feature] = input_list[i]

    input_df = pd.DataFrame(model_input, index=[0])

    pred = model.predict(input_df)

    # todo: need to add result to the database (if it doesn't already exist)
    # Add code here:
    result = Results(
        id=song_id,
        track_name=track_name,
        album_name=album,
        artist=artist,
        image_url=img_url,
        song_url=song_url,
        result=ResultEnum.HIT if pred == 1 else ResultEnum.FLOP,
    )

    db.session.add(result)
    db.session.commit()

    return jsonify({"result": result.to_dict()}), 200
