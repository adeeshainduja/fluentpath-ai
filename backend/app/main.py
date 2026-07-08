from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import engine
from app.api.practice import router as practice_router


app = FastAPI(
    title="FluentPath AI API",
    description="Backend API for the FluentPath AI Personal English Communication Coach",
    version="0.1.0",
)


app.include_router(practice_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to FluentPath AI"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.get("/health/database")
def database_health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "database": "connected"
    }