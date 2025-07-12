from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "🚀 Your D2C Growth AI is running!"}
