from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

import json

from utils.predict import predict

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        print("coming into handler function")
        query_components = parse_qs(urlparse(self.path).query)

        song_id = query_components.get('song_id', [''])[0]

        if not song_id: 
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'message': 'Missing song_id',
                'status': 'Error'
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        result = predict(song_id)

        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        response = {
            'result': result,
            'status': "Success"
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))




# import json
#
# def predict(request):
#     print("Im coming into the handler")
#     params = request.get("query", {})
#     song_id = params.get("song_id")
#     if not song_id:
#         # If song_id is missing, return a 400 error
#         return {
#             "statusCode": 400,
#             "headers": {"Content-Type": "application/json"},
#             "body": json.dumps({"error": "Missing song_id parameter."})
#         }
#
#     result = predict(song_id)
#
#     return {
#         "statusCode": 200,
#         "headers": {"Content-Type": "application/json"},
#         "body": json.dumps(result)
#     }
#
# # from http.server import BaseHTTPRequestHandler
# #
# # class handler(BaseHTTPRequestHandler):
# #
# #     def do_GET(self):
# #
# #
