from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import Base, engine


# --------------------------------------------------
# Import database models
# These imports register the tables with Base.metadata
# before create_all() runs.
# --------------------------------------------------

from app.models.analysis import Analysis
from app.models.correction_state import CorrectionState
from app.models.error_pattern import ErrorPattern
from app.models.practice_attempt import PracticeAttempt
from app.models.practice_task import PracticeTask
from app.models.progress_metric import ProgressMetric
from app.api.dashboard import router as dashboard_router

# --------------------------------------------------
# Import API routers
# --------------------------------------------------

from app.api.practice import (
    router as practice_router,
)

from app.api.learning_plan import (
    router as learning_plan_router,
)

from app.api.hints import (
    router as hints_router,
)

from app.api.evaluations import (
    router as evaluations_router,
)

from app.api.task_evaluations import (
    router as task_evaluations_router,
)

from app.api.practice_tasks import (
    router as practice_tasks_router,
)

from app.api.progress_comparisons import (
    router as progress_comparisons_router,
)

from app.api.adaptive_priorities import (
    router as adaptive_priorities_router,
)

from app.api.practice_strategies import (
    router as practice_strategies_router,
)

from app.api.practice_sessions import (
    router as practice_sessions_router,
)
from fastapi.middleware.cors import CORSMiddleware

# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="FluentPath AI API",
    description=(
        "Backend API for the FluentPath AI "
        "Personal English Communication Coach"
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------------------------
# Create database tables
# --------------------------------------------------

Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# Register routers
# --------------------------------------------------

app.include_router(practice_router)
app.include_router(learning_plan_router)
app.include_router(hints_router)
app.include_router(evaluations_router)
app.include_router(task_evaluations_router)
app.include_router(practice_tasks_router)
app.include_router(progress_comparisons_router)
app.include_router(adaptive_priorities_router)
app.include_router(practice_strategies_router)
app.include_router(practice_sessions_router)
app.include_router(dashboard_router)


# --------------------------------------------------
# Root endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Welcome to FluentPath AI"
    }


# --------------------------------------------------
# Application health check
# --------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# Database health check
# --------------------------------------------------

@app.get("/health/database")
def database_health_check():
    with engine.connect() as connection:
        connection.execute(
            text("SELECT 1")
        )

    return {
        "database": "connected"
    }