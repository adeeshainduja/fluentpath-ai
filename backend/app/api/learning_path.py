from fastapi import APIRouter

from app.schemas.learning_path import LearningPathResponse
from app.services.learning_path_service import get_learning_path

router = APIRouter(
    prefix="/api/v1/test-learning-path",
    tags=["TEST"],
)


@router.get(
    "/{learner_id}",
    response_model=LearningPathResponse,
)
def get_learning_path_api(learner_id: int):
    return get_learning_path(learner_id)