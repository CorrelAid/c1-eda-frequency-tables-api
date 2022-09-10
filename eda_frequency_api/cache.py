import redis
from dotenv import load_dotenv
import os

load_dotenv()

REDIS_ADR = os.environ.get("REDIS_ADR")
REDIS_PORT = os.environ.get("REDIS_PORT")

r = redis.Redis(host=REDIS_ADR, port=REDIS_PORT, db=0)

