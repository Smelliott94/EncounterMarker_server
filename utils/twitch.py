import requests
import logging
import math
import utils.affixes
import utils.mongo
import json

logger = logging.getLogger()

def request_stream_marker(client_id, user_id, access_token, description):
    # Construct the POST request headers
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    data = {
        "user_id": user_id,
        "description": description
    }

    # Make the POST request to set the stream marker
    marker_url = "https://api.twitch.tv/helix/streams/markers"
    logging.critical(json.dumps(headers))
    logging.critical(json.dumps(data))
    response = requests.post(marker_url, headers=headers, json=data)

    # Check the response
    if response.status_code == 200:
        logger.info("Stream marker set successfully.")
        response_data = response.json()
        logger.info(f"Marker ID: {json.dumps(response_data)}")
    else:
        logger.info(f"Failed to set stream marker. Status code: {response.status_code}")
        logger.info(response.text)
    return response

def request_chat_announcement(client_id, user_id, access_token, message):
    # Construct the POST request headers
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    params = {
        'broadcaster_id': user_id,
        'moderator_id': user_id
    }
    data = {
        'message': message
    }
    url = "https://api.twitch.tv/helix/chat/announcements"
    response = requests.post(url, headers=headers, json=data, params=params)

    # Check the response
    if response.status_code == 204:
        logger.info("Announcement sent successfully.")
        logger.info(response.text)
    else:
        logger.info(f"Failed to send Announcement. Status code: {response.status_code}")
        logger.info(response.text)

def refresh_token(token, client_id, secret):
    data = {
        "client_id": client_id,
        "client_secret": secret,
        "grant_type": "refresh_token",
        "refresh_token": token
    }
    response = requests.post("https://id.twitch.tv/oauth2/token", data=data)
    response_data = response.json()
    logger.info(json.dumps(response_data))
    access_token = None
    refresh_token = None
    if "access_token" in response_data:
        access_token = response_data["access_token"]
        refresh_token = response_data["refresh_token"]
    return access_token, refresh_token

def get_token(client_id, secret, code, redirect):
    # Construct the POST request data
    data = {
        "client_id": client_id,
        "client_secret": secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect
    }

    # Make the POST request to exchange the code for an access token
    
    response = requests.post("https://id.twitch.tv/oauth2/token", data=data)
    response_data = response.json()
    logger.info(json.dumps(response_data))
    access_token = None
    refresh_token = None
    if "access_token" in response_data:
        access_token = response_data["access_token"]
        refresh_token = response_data["refresh_token"]
    return access_token, refresh_token

def get_user_data(client_id, token):
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    user_response = requests.get(
        'https://api.twitch.tv/helix/users',
        headers=headers
    )
    user_response_data = user_response.json()
    logger.info(user_response_data)
    user_id = user_response_data["data"][0]["id"]
    user_login = user_response_data["data"][0]["login"]
    return user_id, user_login