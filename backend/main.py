import sys
import os

# Make sure Python can find local modules in backend/
sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine
from models import Base
from routers import fatigue

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("⏳ Creating tables...")
    Base.metadata.create_all(bind=engine)
    yield
    print("🛑 Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "App is working"}

# Register prediction endpoint
app.include_router(fatigue.router)
