import os
from pymongo import MongoClient
from pymongo.collection import Collection
from redis import Redis
import weaviate

# # # MongoDB configuration
# MONGO_USER = os.getenv('MONGO_USER', default="username")  # Optional
# MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', default="password")  # Optional
MONGO_HOST = os.getenv('MONGO_HOST', default="mongo")
MONGO_PORT = os.getenv('MONGO_PORT', default="27017")
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', default="db")

def get_mongo_url():
    '''
    To support db password retrieval for all environment types
    '''
    # if MONGO_USER and MONGO_PASSWORD:
    #     mongo_url = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}?authSource=admin"
    # else:
    mongo_url = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}?authSource=admin"
    return mongo_url


# Connect to MongoDB
mongo_url = get_mongo_url()
client = MongoClient(mongo_url)
database = client[MONGO_DB_NAME]

def get_collection(collection_name: str) -> Collection:
    '''
    Get a collection from the database
    '''
    return database[collection_name]


REDIS_URL = "redis://redis:6379"
redis_client = Redis.from_url(REDIS_URL)

def get_redis():
    return redis_client


weaviate_client = weaviate.connect_to_local(host="weaviate",port=8080, grpc_port=50051)
