from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.listening import (
    ListeningPracticeResponse,
    ListeningSubmissionRequest,
    ListeningSubmissionResponse,
)
from app.services.listening_service import (
    get_listening_practice,
    get_personalized_listening_practice,
    submit_listening_practice,
)

router = APIRouter(
    prefix="/api/v1/listening",
    tags=["Listening"],
)


@router.get(
    "/generate",
    response_model=ListeningPracticeResponse,
)
def generate_listening(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_personalized_listening_practice(
        db=db,
        learner_id=current_user.id,
    )


@router.post(
    "/submit",
    response_model=ListeningSubmissionResponse,
)
def submit_listening(
    request: ListeningSubmissionRequest,
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
        return submit_listening_practice(
            db=db,
            learner_id=learner_id,
            practice_id=request.practice_id,
            answers=request.answers,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
