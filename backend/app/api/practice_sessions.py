from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.practice_session import (
    SessionResponseSubmission,
)

from app.services.practice_session_service import (
    start_practice_session,
    submit_session_response,
)


router = APIRouter(
    prefix="/api/v1/practice-sessions",
    tags=["Practice Sessions"],
)


@router.post("/learners/{learner_id}/start")
def start_session(
    learner_id: int,
    db: Session = Depends(get_db),
):
    result = start_practice_session(
        db=db,
        learner_id=learner_id,
    )

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )

    return result


@router.post("/learners/{learner_id}/submit")
def submit_response(
    learner_id: int,
    request: SessionResponseSubmission,
    db: Session = Depends(get_db),
):
    result = submit_session_response(
        db=db,
        learner_id=learner_id,
        task_id=request.task_id,
        text=request.text,
    )

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )

    return result