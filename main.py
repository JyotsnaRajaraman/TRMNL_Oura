from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import os
import secrets

app = FastAPI()

CLIENT_ID = os.environ["OURA_CLIENT_ID"]
REDIRECT_URI = os.environ["OURA_REDIRECT_URI"]


@app.get("/")
def home():
    return {"status": "running"}


# @app.get("/login")
# def login():
#     state = secrets.token_urlsafe(16)

#     scopes = [
#         "daily",
#         "heartrate",
#         "personal",
#     ]

#     url = (
#         "https://cloud.ouraring.com/oauth/authorize?"
#         f"response_type=code"
#         f"&client_id={CLIENT_ID}"
#         f"&redirect_uri={REDIRECT_URI}"
#         f"&scope={' '.join(scopes)}"
#         f"&state={state}"
#     )

#     return RedirectResponse(url)

from urllib.parse import urlencode

@app.get("/login")
def login():
    state = secrets.token_urlsafe(16)

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "daily personal heartrate",
        "state": state,
    }

    url = (
        "https://cloud.ouraring.com/oauth/authorize?"
        + urlencode(params)
    )

    return RedirectResponse(url)
    

@app.get("/oauth/callback")
def callback(code: str, state: str = ""):
    return {
        "success": True,
        "authorization_code": code,
        "state": state,
    }
