import json

def handler(request):
    print("Im coming into the handler")

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"Message": "Hello World"})
    }
