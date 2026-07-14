from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import practice_service

from app.schemas.practice import (
    PracticeAttemptCreate,
    RetryAttemptCreate,
)

from app.memory.learner_memory import (
    get_learner_weaknesses,
)

from app.services.practice_detail_service import (
    get_practice_detail,
)

router = APIRouter(
    prefix="/api/v1/practice",
    tags=["Practice"],
)


# --------------------------------------------------
# Create Writing Attempt
# --------------------------------------------------

@router.post("/writing")
def create_writing_attempt(
    attempt: PracticeAttemptCreate,
    db: Session = Depends(get_db),
):
    saved_attempt = practice_service.create_writing_attempt(
        db=db,
        attempt=attempt,
    )

    return {
        "id": saved_attempt.id,
        "text": saved_attempt.text,
        "practice_type": saved_attempt.practice_type,
        "created_at": saved_attempt.created_at,
        "message": "Practice attempt saved successfully",
    }


# --------------------------------------------------
# Get All Attempts
# --------------------------------------------------

@router.get("/attempts")
def get_attempts(
    db: Session = Depends(get_db),
):
    return practice_service.get_all_attempts(db)


# --------------------------------------------------
# Get Attempt
# --------------------------------------------------

@router.get("/attempts/{attempt_id}")
def get_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
):
    attempt = practice_service.get_attempt_by_id(
        db=db,
        attempt_id=attempt_id,
    )

    if attempt is None:
        raise HTTPException(
            status_code=404,
            detail="Practice attempt not found",
        )

    return attempt


# --------------------------------------------------
# Analyze Attempt
# --------------------------------------------------

@router.post("/attempts/{attempt_id}/analyze")
def analyze_practice_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
):
    result = practice_service.analyze_attempt(
        db=db,
        attempt_id=attempt_id,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Practice attempt not found",
        )

    return result


# --------------------------------------------------
# Retry Attempt
# --------------------------------------------------

@router.post("/attempts/{attempt_id}/retry")
def retry_practice_attempt(
    attempt_id: int,
    retry_data: RetryAttemptCreate,
    db: Session = Depends(get_db),
):
    result = practice_service.create_retry_attempt(
        db=db,
        original_attempt_id=attempt_id,
        retry_data=retry_data,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Original practice attempt not found",
        )

    return result


# --------------------------------------------------
# Learner Weaknesses
# --------------------------------------------------

@router.get("/learners/{learner_id}/weaknesses")
def get_weaknesses(
    learner_id: int,
    db: Session = Depends(get_db),
):
    return get_learner_weaknesses(
        db=db,
        learner_id=learner_id,
    )


# --------------------------------------------------
# Practice Detail
# --------------------------------------------------

@router.get("/{task_id}")
def get_practice(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_practice_detail(
        db=db,
        task_id=task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Practice not found",
        )

    return task