from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends

from app.core.database import get_db

from app.services.recommendation_service import (
    get_next_recommended_task,
)

router = APIRouter(
    prefix="/api/v1/recommendations",
    tags=["Recommendations"],
)


@router.get("/{learner_id}")
def get_recommendation(
    learner_id: int,
    db: Session = Depends(get_db),
):

    task = get_next_recommended_task(
        db=db,
        learner_id=learner_id,
    )

    return {
        "id": task.id,
        "title": task.title,
        "practice_type": task.practice_type,
        "skill": task.target_skill,
        "difficulty": task.difficulty,
        "estimated_minutes": 20,
    }