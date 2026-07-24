from datetime import date, timedelta

import requests

from config import CLIENT_ID, CLIENT_SECRET
from storage import load_tokens, save_tokens

TOKEN_URL = "https://api.ouraring.com/oauth/token"
API_BASE = "https://api.ouraring.com/v2/usercollection"

session = requests.Session()


def refresh_access_token():
    """Refresh the Oura access token using the stored refresh token."""

    tokens = load_tokens()

    if tokens is None:
        raise Exception("No OAuth tokens found. Visit /login first.")

    r = session.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": tokens["refresh_token"],
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )

    r.raise_for_status()

    new_tokens = r.json()

    # Oura rotates refresh tokens, so always overwrite.
    save_tokens(new_tokens)

    return new_tokens


def get_access_token():
    tokens = load_tokens()

    if tokens is None:
        raise Exception("No OAuth tokens stored.")

    return tokens["access_token"]


def request(endpoint, days=14):
    """
    Request one Oura endpoint.
    Automatically refreshes the token if necessary.
    """

    today = date.today()
    start = today - timedelta(days=days)

    params = {
        "start_date": start.isoformat(),
        "end_date": today.isoformat(),
    }

    headers = {
        "Authorization": f"Bearer {get_access_token()}"
    }

    r = session.get(
        f"{API_BASE}/{endpoint}",
        headers=headers,
        params=params,
    )

    if r.status_code == 401:

        tokens = refresh_access_token()

        headers = {
            "Authorization": f"Bearer {tokens['access_token']}"
        }

        r = session.get(
            f"{API_BASE}/{endpoint}",
            headers=headers,
            params=params,
        )

    r.raise_for_status()

    return r.json()["data"]


def merge_daily_data(days=14):
    """
    Returns one dictionary keyed by date.

    Example:

    {
        "2026-07-15": {
            ...
        },
        ...
    }
    """

    merged = {}

    #
    # Sleep
    #

    for s in request("daily_sleep", days):

        day = s["day"]

        merged.setdefault(day, {})

        merged[day]["sleep_score"] = s.get("score")
        merged[day]["sleep_seconds"] = s.get("total_sleep_duration")
        merged[day]["sleep_hours"] = round(
            s.get("total_sleep_duration", 0) / 3600,
            2,
        )

    #
    # Activity
    #

    for a in request("daily_activity", days):

        day = a["day"]

        merged.setdefault(day, {})

        merged[day]["activity_score"] = a.get("score")
        merged[day]["steps"] = a.get("steps")
        merged[day]["active_calories"] = a.get("active_calories")
        merged[day]["total_calories"] = a.get("total_calories")
        merged[day]["equivalent_walking_distance"] = a.get(
            "equivalent_walking_distance"
        )

    #
    # Readiness
    #

    for r in request("daily_readiness", days):

        day = r["day"]

        merged.setdefault(day, {})

        merged[day]["readiness_score"] = r.get("score")
        merged[day]["hrv"] = r.get("average_hrv")
        merged[day]["resting_hr"] = r.get("resting_heart_rate")
        merged[day]["temperature_deviation"] = r.get(
            "temperature_deviation"
        )

    return dict(sorted(merged.items()))
