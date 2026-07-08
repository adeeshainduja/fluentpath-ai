from fastapi import FastAPI

app = FastAPI(
    title="FluentPath AI API",
    description="Backend API for the FluentPath AI Personal English Communication Coach",
    version="0.1.0",
)


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