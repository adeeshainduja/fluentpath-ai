from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.practice_history import (
    PracticeHistoryResponse,
    PracticeHistorySummary,
    PracticeHistoryType,
)
from app.services.practice_history_service import (
    get_practice_history,
    get_practice_history_summary,
)


router = APIRouter(
    prefix="/api/v1/practice-history",
    tags=["Practice History"],
)


@router.get(
    "/learners/{learner_id}",
    response_model=PracticeHistoryResponse,
)
def learner_practice_history(
    learner_id: int,
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    practice_type: PracticeHistoryType = "all",
    db: Session = Depends(get_db),
):
    return get_practice_history(
        db=db,
        learner_id=learner_id,
        limit=limit,
        offset=offset,
        practice_type=practice_type,
    )


@router.get(
    "/learners/{learner_id}/summary",
    response_model=PracticeHistorySummary,
)
def learner_practice_history_summary(
    learner_id: int,
    practice_type: PracticeHistoryType = "all",
    db: Session = Depends(get_db),
):
    return get_practice_history_summary(
        db=db,
        learner_id=learner_id,
        practice_type=practice_type,
    )
