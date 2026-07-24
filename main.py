from fastapi import FastAPI

from auth import router as auth_router
from oura import (
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

    return {
        "sleep": get_daily_sleep(),
        "activity": get_daily_activity(),
        "readiness": get_daily_readiness(),
    }
