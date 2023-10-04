import logging
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
logger = logging.getLogger()

MONGODB_USER = os.getenv('MONGODB_USER')
MONGODB_PASS = os.getenv('MONGODB_PASS')

mongodb_uri = f'mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}@cluster0.dx0lwon.mongodb.net/?retryWrites=true&w=majority'

def _init_connection(collection_name, db_name='encountermarker'):
    client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
    db = client[db_name] 
    collection = db[collection_name]
    return client, collection

def get_tokens(user_id):
    client, access_token_collection = _init_connection("access_tokens")
    result = access_token_collection.find_one({"id": user_id})
    client.close()
    logger.info(result)
    return result["login"], result["token"], result["refresh_token"]

def get_user_id(login):
    client, access_token_collection = _init_connection("access_tokens")
    result = access_token_collection.find_one({"login": login})
    client.close()
    logger.info(result)
    return result["id"]

def upsert_access_token(user_id, user_login, access_token, refresh_token):
    # Key off user id, create an entry or update existing
    client, access_token_collection = _init_connection("access_tokens")
    result = access_token_collection.update_one(
        {"id": user_id},
        {"$set": {
            "login": user_login,
            "token": access_token,
            "refresh_token": refresh_token
            }
        },
        upsert=True
    )
    if result.upserted_id:
        logger.info("New access token INSERT success")
    else:
        logger.info("Access token updated or already exists.")
        client.close()