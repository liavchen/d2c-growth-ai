from fastapi import FastAPI
from database import engine
from models import Base

app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "🚀 Your D2C Growth AI is running!"}
