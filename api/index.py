from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

import json
 
class handler(BaseHTTPRequestHandler):
 
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)

        param = query_components.get('param', [''])[0]

        if param: 
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            response = {
                'param': param,
                'status': "Success"
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else: 
            self.send_response(400)
            self.send_header('Content-type','application/json')
            self.end_headers()
            response = {
                "message": "Missing path param",
                'status': "Error"
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        return
