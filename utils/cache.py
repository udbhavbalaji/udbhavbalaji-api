from  dotenv import load_dotenv
from upstash_redis import Redis

import os

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
REDIS_TOKEN = os.getenv("REDIS_TOKEN")

if not REDIS_TOKEN or not REDIS_URL: 
    raise Exception("Missing Redis credentials")

cache = Redis(url=REDIS_URL, token=REDIS_TOKEN)

