from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.vocabulary import (
    VocabularyPracticeResponse,
    VocabularySubmissionRequest,
    VocabularySubmissionResponse,
)
from app.services.vocabulary_service import (
    get_vocabulary_practice,
    get_personalized_vocabulary_practice,
    submit_vocabulary_practice,
)

router = APIRouter(
    prefix="/api/v1/vocabulary",
    tags=["Vocabulary"],
)


@router.get(
    "/generate",
    response_model=VocabularyPracticeResponse,
)
def generate_vocabulary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_personalized_vocabulary_practice(
        db=db,
        learner_id=current_user.id,
    )


@router.post(
    "/submit",
    response_model=VocabularySubmissionResponse,
)
def submit_vocabulary(
    request: VocabularySubmissionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    learner_id = current_user.id

    if learner_id is None:
        raise HTTPException(
            status_code=400,
            detail="learner_id is required.",
        )

    try:
        return submit_vocabulary_practice(
            db=db,
            learner_id=learner_id,
            session_id=request.session_id,
            answers=[answer.model_dump(by_alias=False) for answer in request.answers],
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
