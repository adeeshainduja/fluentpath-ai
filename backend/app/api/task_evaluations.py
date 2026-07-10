from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.task_evaluation import (
    TaskEvaluationRequest,
)
from app.services.task_evaluation_service import (
    evaluate_practice_task,
)


router = APIRouter(
    prefix="/api/v1/task-evaluations",
    tags=["Task Evaluations"],
)


@router.post("/attempts/{attempt_id}")
def evaluate_task(
    attempt_id: int,
    request: TaskEvaluationRequest,
    db: Session = Depends(get_db),
):

    result = evaluate_practice_task(
        db=db,
        attempt_id=attempt_id,
        task_instruction=request.task_instruction,
        target_skill=request.target_skill,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Practice attempt not found",
        )

    return result