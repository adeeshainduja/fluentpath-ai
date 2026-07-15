from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.learning_path import LearningPathResponse
from app.services.learning_path_service import get_learning_path

router = APIRouter(
    prefix="/api/v1/learning-path",
    tags=["Learning Path"],
)


@router.get(
    "/{learner_id}",
    response_model=LearningPathResponse,
)
def get_learning_path_api(
    learner_id: int,
    db: Session = Depends(get_db),
):
    return get_learning_path(
        db=db,
        learner_id=learner_id,
    )