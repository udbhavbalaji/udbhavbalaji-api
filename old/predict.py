import json

from utils.predict import predict

print("Coming into the module")

def handler(request):
    print("Im coming into the handler")
    params = request.get("query", {})
    song_id = params.get("song_id")
    if not song_id:
        # If song_id is missing, return a 400 error
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Missing song_id parameter."})
        }

    result = predict(song_id)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result)
    }
