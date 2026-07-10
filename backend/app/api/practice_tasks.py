from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.practice_task import (
    PracticeTaskResponse,
)
from app.services.practice_task_service import (
    generate_and_save_task,
)


router = APIRouter(
    prefix="/api/v1/practice-tasks",
    tags=["Practice Tasks"],
)


@router.post(
    "/learners/{learner_id}/generate",
    response_model=PracticeTaskResponse,
)
def generate_task(
    learner_id: int,
    db: Session = Depends(get_db),
):
    result = generate_and_save_task(
        db=db,
        learner_id=learner_id,
    )

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )

    return result