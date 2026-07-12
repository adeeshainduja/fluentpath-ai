from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.dashboard_service import (
    get_dashboard_summary,
)

router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/learners/{learner_id}",
)
def dashboard_summary(
    learner_id: int,
    db: Session = Depends(get_db),
):
    return get_dashboard_summary(
        db=db,
        learner_id=learner_id,
    )