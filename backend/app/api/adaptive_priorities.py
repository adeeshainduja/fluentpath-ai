from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.adaptive_priority_service import (
    calculate_adaptive_priorities,
)


router = APIRouter(
    prefix="/api/v1/adaptive-priorities",
    tags=["Adaptive Priorities"],
)


@router.get("/learners/{learner_id}")
def learner_adaptive_priorities(
    learner_id: int,
    db: Session = Depends(get_db),
):
    priorities = calculate_adaptive_priorities(
        db=db,
        learner_id=learner_id,
    )

    return {
        "learner_id": learner_id,
        "top_priority": (
            priorities[0]
            if priorities
            else None
        ),
        "priorities": priorities,
    }