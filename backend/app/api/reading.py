from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.reading import (
    ReadingPracticeResponse,
    ReadingSubmissionRequest,
    ReadingSubmissionResponse,
)
from app.services.reading_service import (
    get_reading_practice,
    submit_reading_practice,
)

router = APIRouter(
    prefix="/api/v1/reading",
    tags=["Reading"],
)


@router.get(
    "/generate",
    response_model=ReadingPracticeResponse,
)
def generate_reading(
    current_user: User = Depends(get_current_user),
):
    return get_reading_practice()


@router.post(
    "/submit",
    response_model=ReadingSubmissionResponse,
)
def submit_reading(
    request: ReadingSubmissionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    learner_id = current_user.id or request.learner_id

    if learner_id is None:
        raise HTTPException(
            status_code=400,
            detail="learner_id is required.",
        )

    try:
        return submit_reading_practice(
            db=db,
            learner_id=learner_id,
            passage_id=request.passage_id,
            answers=request.answers,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
