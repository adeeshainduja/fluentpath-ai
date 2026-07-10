from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.task_evaluation_service import (
    evaluate_linked_practice_task,
)


router = APIRouter(
    prefix="/api/v1/task-evaluations",
    tags=["Task Evaluations"],
)


@router.post("/attempts/{attempt_id}")
def evaluate_task(
    attempt_id: int,
    db: Session = Depends(get_db),
):
    result = evaluate_linked_practice_task(
        db=db,
        attempt_id=attempt_id,
    )

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )

    return result