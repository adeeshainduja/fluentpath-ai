from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.learning_plan_service import (
    generate_learning_plan,
)


router = APIRouter(
    prefix="/api/v1/learning-plans",
    tags=["Learning Plans"],
)


@router.get("/learners/{learner_id}")
def get_learning_plan(
    learner_id: int,
    db: Session = Depends(get_db),
):

    return generate_learning_plan(
        db=db,
        learner_id=learner_id,
    )