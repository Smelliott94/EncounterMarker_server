# EncounterMarker Server

Server component of [EncounterMarker](https://github.com/Smelliott94/EncounterMarker). Handles user authentication, authorization, and calls to the Twitch API.

Built using python 3.11.6, FastAPI, and MongoDB
Hosted on render.com

[Interactive docs](https://encountermarkerserver.onrender.com/docs)

[app auth link for clients](https://id.twitch.tv/oauth2/authorize?client_id=8188onbz5c834x47p07lfopa4kp0uv&redirect_uri=https://encountermarkerserver.onrender.com/auth&response_type=code&scope=user:edit:broadcast)

[auth link for local testing](https://id.twitch.tv/oauth2/authorize?client_id=8188onbz5c834x47p07lfopa4kp0uv&redirect_uri=http://localhost:8080/auth&response_type=code&scope=user:edit:broadcast)