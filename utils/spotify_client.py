from typing import TypedDict, Optional, cast
from dotenv import load_dotenv
from upstash_redis import Redis
from datetime import datetime, timezone

import requests
import base64
import json
import os

load_dotenv();

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

REDIS_URL = os.getenv("REDIS_URL")
REDIS_TOKEN = os.getenv("REDIS_TOKEN")

if not CLIENT_ID or not CLIENT_SECRET: 
    raise Exception("Missing Spotify App Credentials")

if not REDIS_TOKEN or not REDIS_URL: 
    raise Exception("Missing Redis credentials")


cache = Redis(url=REDIS_URL, token=REDIS_TOKEN)

class SpotifyToken(TypedDict): 
    token: str
    time_accessed: int

class SpotifyClient:

    AUTH_URL = "https://accounts.spotify.com/api/token"

    def __init__(self) -> None: 
        if not self.is_token_valid:
            self.token = self.authorize()
        else: 
            self.token = self.get_existing_token()


    @property
    def auth_headers(self): 
        return {
            "Authorization": f'Bearer {self.token}',
            "Content-Type": "application/json"
        }

    @property
    def is_token_valid(self): 
        token = self.token_object
        if token: 
            formatted_time_accessed = token['time_accessed']
            # note: since redis has an option to auto-delete token after sometime, I don't need to worry too much about this... but still need to fix this shit
            time_since_last_auth = datetime.now(tz=timezone.utc) - formatted_time_accessed

            if time_since_last_auth.seconds < 3600:
                return True
        return False

    @property
    def token_object(self) -> Optional[SpotifyToken]: 
        try: 
            token_object = cache.get("spotify_auth_token")

            if token_object is None: 
                return 

            token_object = json.loads(token_object)

            if not isinstance(token_object, dict):
                print(f'Warning: Unexpected cache item returned')
                return

            included_fields = ['token', 'time_accessed']

            if not all(field in token_object for field in included_fields): 
                print(f'Warning: Token missing required fields')
                return

            return SpotifyToken(**token_object)

        except Exception as e:
            print(f"Error: Couldn't Retrieve the tokan. Ran into error {e}")

    def get_existing_token(self) -> Optional[str]: 
        if (self.token_object):
            return self.token_object['token']

        return None

    def authorize(self):
        auth_string = f'{CLIENT_ID}:{CLIENT_SECRET}'
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

        headers = {
            "Authorization": f'Basic {auth_base64}',
            "Content_Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials"
        }
        result = requests.post(self.AUTH_URL, headers=headers, data=data)
        json_result = json.loads(result.content)

        token = json_result['access_token']

        old_token_obj = self.token_object
        if old_token_obj:
            db.session.delete(old_token_obj)
        new_token_obj = OAuthToken(access_token=json_result['access_token'])
        db.session.add(new_token_obj)
        db.session.commit()
        return token


