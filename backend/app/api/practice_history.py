from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.practice_history import (
    PracticeHistoryDetailResponse,
    PracticeHistoryResponse,
    PracticeHistoryType,
)
from app.services.practice_history_service import (
    get_practice_history_detail,
    get_practice_history,
    get_practice_history_summary,
)


router = APIRouter(
    prefix="/api/v1/practice-history",
    tags=["Practice History"],
)


@router.get(
    "",
    response_model=PracticeHistoryResponse,
)
def learner_practice_history(
    current_user: User = Depends(get_current_user),
    page: int = Query(default=1, ge=1),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    type: PracticeHistoryType = Query(default="all", alias="type"),
    sort: str = Query(default="newest"),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return get_practice_history(
        db=db,
        learner_id=current_user.id,
        page=page,
        limit=limit,
        practice_type=type,
        sort=sort,
        search=search,
    )


@router.get(
    "/{attempt_id}",
    response_model=PracticeHistoryDetailResponse,
)
def learner_practice_history_detail(
    attempt_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    detail = get_practice_history_detail(
        db=db,
        learner_id=current_user.id,
        attempt_id=attempt_id,
    )
    if detail is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Practice history not found")
    return detail
