from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.practice_task import (
    PracticeTaskResponse,
    PracticeTaskSubmission,
)

from app.services.practice_task_service import (
    generate_and_save_task,
    get_learner_tasks,
    get_task,
    submit_task_attempt,
)


router = APIRouter(
    prefix="/api/v1/practice-tasks",
    tags=["Practice Tasks"],
)


# --------------------------------------------------
# Generate a personalized practice task
# --------------------------------------------------

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


# --------------------------------------------------
# Get all tasks for a learner
# --------------------------------------------------

@router.get(
    "/learners/{learner_id}",
    response_model=list[PracticeTaskResponse],
)
def list_tasks(
    learner_id: int,
    db: Session = Depends(get_db),
):
    return get_learner_tasks(
        db=db,
        learner_id=learner_id,
    )


# --------------------------------------------------
# Get one practice task
# --------------------------------------------------

@router.get(
    "/{task_id}",
    response_model=PracticeTaskResponse,
)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task(
        db=db,
        task_id=task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Practice task not found",
        )

    return task


# --------------------------------------------------
# Submit learner answer for a task
# --------------------------------------------------

@router.post("/{task_id}/submit")
def submit_task(
    task_id: int,
    request: PracticeTaskSubmission,
    db: Session = Depends(get_db),
):
    result = submit_task_attempt(
        db=db,
        task_id=task_id,
        text=request.text,
    )

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=404,
            detail=result["error"],
        )

    return {
        "attempt_id": result.id,
        "task_id": result.task_id,
        "learner_id": result.learner_id,
        "text": result.text,
        "attempt_number": result.attempt_number,
    }