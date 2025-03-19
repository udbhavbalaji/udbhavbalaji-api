from typing import TypedDict, Optional
from dotenv import load_dotenv
from upstash_redis import Redis

import requests
import base64
import json
import os

load_dotenv();

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

REDIS_URL = os.getenv("UPSTASH_REDIS_REST_URL")
REDIS_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")

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
    BASE_API_URL = "https://api.spotify.com/v1"

    def __init__(self) -> None: 
        token_str = self.token
        if token_str: 
            self.access_token = token_str
        else: 
            self.access_token = self.__authorize();

    @property
    def auth_headers(self): 
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    @property
    def token(self) -> Optional[str]: 
        try: 
            access_token = cache.get('spotify_access_token')
            if access_token: 
                return access_token
        except Exception as err: 
            print(f"Error: Couldn't access cache", err)

    def __authorize(self) -> str: 
        auth_string = f'{CLIENT_ID}:{CLIENT_SECRET}'
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

        headers = {
            "Authorization": f'Basic {auth_base64}',
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials"
        }
        result = requests.post(self.AUTH_URL, headers=headers, data=data)
        print('result_auth', result.json())
        json_result = json.loads(result.content)

        token = json_result['access_token']

        # add the token to the cache ensure it expires in the supplied number of seconds
        cache.set("spotify_access_token", token, ex=json_result['expires_in'])

        # return the token
        return token

    def get_track(self, song_id: str):
        url = f"{self.BASE_API_URL}/tracks/{song_id}"

        response = requests.get(url, headers=self.auth_headers)

        response_json = response.json()

        if "error" in response_json.keys(): 
            print("get_track")
            raise Exception("Error while fetching data")

        return response_json

    def get_track_features(self, song_id: str): 
        url = f"{self.BASE_API_URL}/audio-features/{song_id}"

        print(self.auth_headers)

        response = requests.get(url, headers=self.auth_headers)
        print(response)
        response_json = response.json()

        if "error" in response_json.keys(): 
            print("get_track_features")
            print(response_json)
            raise Exception("Error while fetching data")

        return response_json

    def get_track_analysis(self, song_id: str): 
        url = f"{self.BASE_API_URL}/audio-analysis/{song_id}"

        response = requests.get(url, headers=self.auth_headers)

        response_json = response.json()

        if "error" in response_json.keys(): 
            print("get_track_analysis")
            raise Exception("Error while fetching data")

        return response_json




# class SpotifyClient:
#
#     AUTH_URL = "https://accounts.spotify.com/api/token"
#
#     def __init__(self) -> None: 
#         if not self.is_token_valid:
#             self.token = self.authorize()
#         else: 
#             self.token = self.get_existing_token()
#
#
#     @property
#     def auth_headers(self): 
#         return {
#             "Authorization": f'Bearer {self.token}',
#             "Content-Type": "application/json"
#         }
#
#     @property
#     def is_token_valid(self): 
#         token = self.token_object
#         if token: 
#             formatted_time_accessed = token['time_accessed']
#             # note: since redis has an option to auto-delete token after sometime, I don't need to worry too much about this... but still need to fix this shit
#             time_since_last_auth = datetime.now(tz=timezone.utc) - formatted_time_accessed
#
#             if time_since_last_auth.seconds < 3600:
#                 return True
#         return False
#
#     @property
#     def token_object(self) -> Optional[SpotifyToken]: 
#         try: 
#             token_object = cache.get("spotify_auth_token")
#
#             if token_object is None: 
#                 return 
#
#             token_object = json.loads(token_object)
#
#             if not isinstance(token_object, dict):
#                 print(f'Warning: Unexpected cache item returned')
#                 return
#
#             included_fields = ['token', 'time_accessed']
#
#             if not all(field in token_object for field in included_fields): 
#                 print(f'Warning: Token missing required fields')
#                 return
#
#             return SpotifyToken(**token_object)
#
#         except Exception as e:
#             print(f"Error: Couldn't Retrieve the tokan. Ran into error {e}")
#
#     def get_existing_token(self) -> Optional[str]: 
#         if (self.token_object):
#             return self.token_object['token']
#
#         return None
#
#     def authorize(self):
#         auth_string = f'{CLIENT_ID}:{CLIENT_SECRET}'
#         auth_bytes = auth_string.encode('utf-8')
#         auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
#
#         headers = {
#             "Authorization": f'Basic {auth_base64}',
#             "Content_Type": "application/x-www-form-urlencoded"
#         }
#         data = {
#             "grant_type": "client_credentials"
#         }
#         result = requests.post(self.AUTH_URL, headers=headers, data=data)
#         json_result = json.loads(result.content)
#
#         token = json_result['access_token']
#
#         old_token_obj = self.token_object
#         if old_token_obj:
#             db.session.delete(old_token_obj)
#         new_token_obj = OAuthToken(access_token=json_result['access_token'])
#         db.session.add(new_token_obj)
#         db.session.commit()
#         return token
#
#
