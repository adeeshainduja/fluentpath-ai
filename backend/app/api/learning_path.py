from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.learning_path import (
    LearningPathResponse,
    LearningPathUpdateResponse,
)
from app.services.learning_path_service import (
    get_learning_path,
    update_learning_path,
)

router = APIRouter(
    prefix="/api/v1/learning-path",
    tags=["Learning Path"],
)


@router.get("", response_model=LearningPathResponse)
def get_learning_path_api(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_learning_path(
        db=db,
        learner_id=current_user.id,
    )


@router.post("/update", response_model=LearningPathUpdateResponse)
def update_learning_path_api(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return LearningPathUpdateResponse(
        path=update_learning_path(
            db=db,
            learner_id=current_user.id,
        ),
    )
