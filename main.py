from fastapi import FastAPI

from app.auth import router as auth_router
from app.oura import (
    get_daily_sleep,
    get_daily_activity,
    get_daily_readiness,
)

app = FastAPI()

app.include_router(auth_router)


@app.get("/")
def root():
    return {"status": "running"}


@app.get("/api/trmnl")
def trmnl():

    sleep = get_daily_sleep()["data"][0]
    readiness = get_daily_readiness()["data"][0]
    activity = get_daily_activity()["data"][0]

    return {
        "date": sleep["day"],

        "sleep_score": sleep["score"],
        "sleep_duration": sleep["contributors"]["total_sleep"],

        "readiness_score": readiness["score"],
        "hrv": readiness["contributors"]["hrv_balance"],
        "resting_hr": readiness["contributors"]["resting_heart_rate"],

        "activity_score": activity["score"],
        "steps": activity["steps"],
        "calories": activity["active_calories"],
    }
