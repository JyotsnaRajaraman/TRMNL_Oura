import requests

from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from storage import load_tokens, save_tokens

TOKEN_URL = "https://api.ouraring.com/oauth/token"
API_BASE = "https://api.ouraring.com/v2/usercollection"


def refresh_access_token():

    tokens = load_tokens()

    if tokens is None:
        raise Exception("No stored OAuth tokens. Visit /login first.")

    r = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": tokens["refresh_token"],
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )

    if not r.ok:
        raise Exception(f"Token refresh failed: {r.text}")

    new_tokens = r.json()

    # Oura rotates refresh tokens.
    save_tokens(new_tokens)

    return new_tokens


def get_access_token():

    tokens = load_tokens()

    if tokens is None:
        raise Exception("No OAuth tokens found.")

    return tokens["access_token"]


def request(endpoint):

    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    r = requests.get(
        f"{API_BASE}/{endpoint}",
        headers=headers,
    )

    # Token expired
    if r.status_code == 401:

        tokens = refresh_access_token()

        headers = {
            "Authorization": f"Bearer {tokens['access_token']}"
        }

        r = requests.get(
            f"{API_BASE}/{endpoint}",
            headers=headers,
        )

    r.raise_for_status()

    return r.json()


def get_daily_sleep():

    return request("daily_sleep")


def get_daily_activity():

    return request("daily_activity")


def get_daily_readiness():

    return request("daily_readiness")


def get_heartrate():

    return request("heartrate")
