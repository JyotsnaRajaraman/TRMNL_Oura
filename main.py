from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/oauth/callback")
def oauth_callback():
    return {"message": "OAuth callback reached"}
