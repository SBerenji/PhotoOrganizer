from fastapi import FastAPI
from fastapi.responses import JSONResponse
from photo_organizer_script import main

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to the photo organizer app!"}
