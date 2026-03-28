from fastapi import FastAPI
from app.config import get_settings

app = FastAPI()
settings = get_settings()

@app.get("/health")
async def health_check():
    """
    This endpoint is CRITICAL.
    docker-compose relies on it to know when the AI Layer is ready 
    to accept connections from the bot and web services.
    """
    return {"status": "healthy", "model": settings.ORCHESTRATOR_MODEL}

@app.get("/")
async def root():
    return {"message": "Marka AI Backend is Running"}