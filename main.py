from fastapi import FastAPI

from auth import router as auth_router
from oura import merge_daily_data

app = FastAPI()

app.include_router(auth_router)


@app.get("/")
def home():
    return {"status": "running"}


@app.get("/api/trmnl")
def trmnl():
    return merge_daily_data()
