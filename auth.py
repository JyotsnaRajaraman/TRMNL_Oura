from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
import secrets
import requests

from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from storage import save_tokens

router = APIRouter()

SCOPES = [
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


@router.get("/login")
def login():

    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "state": secrets.token_urlsafe(16),
    }

    url = (
        "https://cloud.ouraring.com/oauth/authorize?"
        + urlencode(params)
    )

    return RedirectResponse(url)


@router.get("/oauth/callback")
def callback(code: str):

    r = requests.post(
        "https://api.ouraring.com/oauth/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )

    tokens = r.json()

    save_tokens(tokens)

    return {
        "status": "connected to oura!",
        "expires_in": tokens.get("expires_in"),
    }
