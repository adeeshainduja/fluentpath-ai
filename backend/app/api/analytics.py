from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.analytics_service import (
    get_learner_progress_history,
    get_learner_progress_summary,
    get_skill_progress,
    get_skill_priorities,
)


router = APIRouter(
    prefix="/api/v1/analytics",
    tags=["Analytics"],
)


@router.get("/learners/{learner_id}/history")
def progress_history(
    learner_id: int,
    db: Session = Depends(get_db),
):
    return {
        "learner_id": learner_id,
        "history": get_learner_progress_history(
            db=db,
            learner_id=learner_id,
        ),
    }


@router.get("/learners/{learner_id}/summary")
def progress_summary(
    learner_id: int,
    db: Session = Depends(get_db),
):
    return get_learner_progress_summary(
        db=db,
        learner_id=learner_id,
    )


@router.get("/learners/{learner_id}/skills")
def skill_progress(
    learner_id: int,
    db: Session = Depends(get_db),
):
    return {
        "learner_id": learner_id,
        "skills": get_skill_progress(
            db=db,
            learner_id=learner_id,
        ),
    }


@router.get(
    "/learners/{learner_id}/skill-priorities"
)
def skill_priorities(
    learner_id: int,
    db: Session = Depends(get_db),
):
    return {
        "learner_id": learner_id,
        "priorities": get_skill_priorities(
            db=db,
            learner_id=learner_id,
        ),
    }