from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.progress_comparison_service import (
    compare_task_attempts,
)


router = APIRouter(
    prefix="/api/v1/progress-comparisons",
    tags=["Progress Comparisons"],
)


@router.post("/tasks/{task_id}/compare")
def compare_progress(
    task_id: int,
    previous_attempt_id: int,
    current_attempt_id: int,
    db: Session = Depends(get_db),
):

    result = compare_task_attempts(
        db=db,
        task_id=task_id,
        previous_attempt_id=previous_attempt_id,
        current_attempt_id=current_attempt_id,
    )

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )

    return result