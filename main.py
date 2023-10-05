import dotenv
import os
import logging
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from utils import setup_logging
import utils.twitch
import utils.mongo
from apscheduler.schedulers.background import BackgroundScheduler
from bson import ObjectId

logger = logging.getLogger()
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
REDIRECT_URL = os.getenv('REDIRECT_URL')

app = FastAPI()

# Initialize the APScheduler
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    utils.mongo.validate_tokens,
    trigger="interval",
    hours=1,
    id="hourly_token_validation",
    replace_existing=True,
)

# only allow valid id formats
async def validate_client_code_header(
    X_Client_Code: str = Header(..., description="Client code supplied during authentication", convert_underscores=True)
):
    if object is None:
        raise HTTPException(status_code=400, detail="Missing X-Client-Code header")
    
    try:
        bson_object_id = ObjectId(X_Client_Code)
        return bson_object_id
    
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid X-Client-Code header")

class MarkerPayload(BaseModel):
    user_id: str
    description: str

def authorize_user(user, client_code):
    target_user = utils.mongo.get_client_id(client_code)
    logger.info(f"target_user {target_user}")
    if user != target_user:
        raise HTTPException(status_code=403, detail="Permission denied")
    logging.info(f"user {user} authorized")

# Define the /auth endpoint to handle authorization code
# This is where the user is redirected to after allowing the app
@app.get("/auth")
async def auth(code: str, scope: str):
    try:
        access_token, refresh_token = utils.twitch.get_token(
            TWITCH_CLIENT_ID,
            TWITCH_CLIENT_SECRET,
            code,
            REDIRECT_URL
        )
        if access_token:
            user_id, user_login = utils.twitch.get_user_data(TWITCH_CLIENT_ID, access_token)
            # Store user data and access tokens in mongoDB
            app_user_id = utils.mongo.upsert_access_token(user_id, user_login, access_token, refresh_token)
            
        else:
            return {"message": "Failed to obtain an access token"}

        return f"Authentication successful! Private client code: {app_user_id}"

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user")
async def user(login):
    try:
        user_id = utils.mongo.get_user_id(login)
        return {"user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/marker")
async def marker(
    markerPayload: MarkerPayload,
    X_Client_Code: ObjectId = Depends(validate_client_code_header)
):
    try:
        authorize_user(markerPayload.user_id, X_Client_Code)
        login_id, access_token, refresh_token =  utils.mongo.get_tokens(markerPayload.user_id)
        response = utils.twitch.request_stream_marker(
            TWITCH_CLIENT_ID,
            markerPayload.user_id,
            access_token,
            markerPayload.description            
        )

        if response.status_code == 401:
            # Try to refresh tokens and retry
            access_token, refresh_token = utils.twitch.refresh_token(refresh_token, TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
            utils.mongo.upsert_access_token(markerPayload.user_id, login_id, access_token, refresh_token)
            response = utils.twitch.request_stream_marker(
                TWITCH_CLIENT_ID,
                markerPayload.user_id,
                access_token,
                markerPayload.description
            )
        return response.json()

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/auth_link")
async def auth_link():
    link = f"https://id.twitch.tv/oauth2/authorize?client_id={TWITCH_CLIENT_ID}&redirect_uri=https://encountermarkerserver.onrender.com/auth&response_type=code&scope=user:edit:broadcast"
    return {"twitch_auth_link": link}

@app.get("/validate_user")
async def validate_user(X_Client_Code: ObjectId = Depends(validate_client_code_header)):
    valid_id = utils.mongo.get_client_id(X_Client_Code)
    return {"valid_user_id": valid_id}


if __name__ == "__main__":
    import uvicorn

    # Start the FastAPI application using Uvicorn
    uvicorn.run(app, host="localhost", port=8080)