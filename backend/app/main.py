from fastapi import FastAPI
from sqlalchemy import text

from app.models.correction_state import CorrectionState
from app.api.practice import router as practice_router
from app.core.database import Base, engine
from app.models.error_pattern import ErrorPattern
from app.models.practice_attempt import PracticeAttempt
from app.models.analysis import Analysis
from app.api.learning_plan import (
    router as learning_plan_router,
)
from app.api.hints import router as hints_router
from app.api.evaluations import (
    router as evaluations_router,
)
from app.api.task_evaluations import (
    router as task_evaluations_router,
)
from app.models.practice_task import PracticeTask
from app.api.practice_tasks import (
    router as practice_tasks_router,
)
from app.api.progress_comparisons import (
    router as progress_comparisons_router,
)
from app.models.progress_metric import ProgressMetric



app = FastAPI(
    title="FluentPath AI API",
    description="Backend API for the FluentPath AI Personal English Communication Coach",
    version="0.1.0",
)

Base.metadata.create_all(bind=engine)

app.include_router(practice_router)
app.include_router(learning_plan_router)
app.include_router(hints_router)
app.include_router(evaluations_router)
app.include_router(task_evaluations_router)
app.include_router(practice_tasks_router)
app.include_router(progress_comparisons_router)


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