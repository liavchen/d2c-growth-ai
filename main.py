from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine
from models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("⏳ Creating tables...")
    Base.metadata.create_all(bind=engine)
    yield  # App runs after this
    print("🛑 Shutting down...")  # Runs on app shutdown

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "App is working"}
