import logging
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from utils import setup_logging
logger = logging.getLogger()

MONGODB_USER = os.getenv('MONGODB_USER')
MONGODB_PASS = os.getenv('MONGODB_PASS')

mongodb_uri = f'mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}@cluster0.dx0lwon.mongodb.net/?retryWrites=true&w=majority'

def _init_connection(collection_name, db_name='encountermarker'):
    client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
    db = client[db_name] 
    collection = db[collection_name]
    return client, collection

def get_client_id(client_id: ObjectId):
    # Get twitch user id from Database _id
    client, access_token_collection = _init_connection("access_tokens")
    result = access_token_collection.find_one({"_id": client_id})
    client.close()
    logger.info(result)
    return result["id"]

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
    client.close()
    if result.upserted_id:
        logger.info("New access token INSERT success")
        return result.upserted_id
    else:
        logger.info("Access token updated or already exists.")
        client, access_token_collection = _init_connection("access_tokens")
        result = access_token_collection.find_one({"id": user_id})
        client.close()
        return result["_id"]

def validate_tokens():
    # TODO grab all the tokens and validate with twitch API https://dev.twitch.tv/docs/authentication/validate-tokens/
    # If the token is invalid then null the corresponding token and refresh_token in the DB 
    logger("validation complete")