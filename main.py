from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
import os
import secrets

app = FastAPI()

# Environment variables from Railway
CLIENT_ID = os.environ["OURA_CLIENT_ID"]
REDIRECT_URI = os.environ["OURA_REDIRECT_URI"]


@app.get("/")
def home():
    return {"status": "running"}


@app.get("/login")
def login():
    state = secrets.token_urlsafe(16)

    # Request every scope your app has been approved for
    scopes = [
        "email",
        "heartrate",
        "stress",
        "session",
        "personal",
        "tag",
        "spo2",
        "heart_health",
        "daily",
        "workout",
    ]

    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(scopes),
        "state": state,
    }

    auth_url = (
        "https://cloud.ouraring.com/oauth/authorize?"
        + urlencode(params)
    )

    print(auth_url)

    return RedirectResponse(auth_url)


@app.get("/oauth/callback")
def callback(
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    error_description: str | None = None,
):
    return {
        "code": code,
        "state": state,
        "error": error,
        "error_description": error_description,
    }
