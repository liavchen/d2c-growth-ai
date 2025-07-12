from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "🚀 Your D2C Growth AI is running!"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Use Railway's dynamic port
    uvicorn.run("main:app", host="0.0.0.0", port=port)