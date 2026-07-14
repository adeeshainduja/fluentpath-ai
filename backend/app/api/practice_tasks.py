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
    generate_adaptive_practice_task,
    get_learner_tasks,
    get_task,
    get_task_attempts,
    submit_task_attempt,
)

from app.services.practice_evaluation_service import (
    evaluate_practice,
)

router = APIRouter(
    prefix="/api/v1/practice-tasks",
    tags=["Practice Tasks"],
)


# ==========================================================
# Generate Personalized Practice Task
# ==========================================================

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


# ==========================================================
# Generate Adaptive Practice Task
# ==========================================================

@router.post(
    "/learners/{learner_id}/generate-adaptive",
    response_model=PracticeTaskResponse,
)
def generate_adaptive_task_endpoint(
    learner_id: int,
    db: Session = Depends(get_db),
):
    result = generate_adaptive_practice_task(
        db=db,
        learner_id=learner_id,
    )

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )

    return result


# ==========================================================
# Get All Tasks
# ==========================================================

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


# ==========================================================
# Get One Task
# ==========================================================

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


# ==========================================================
# Submit Practice Task
# ==========================================================

@router.post("/{task_id}/submit")
def submit_task(
    task_id: int,
    request: PracticeTaskSubmission,
    db: Session = Depends(get_db),
):
    attempt = submit_task_attempt(
        db=db,
        task_id=task_id,
        text=request.text,
    )

    if isinstance(attempt, dict) and "error" in attempt:
        raise HTTPException(
            status_code=404,
            detail=attempt["error"],
        )

    evaluation = evaluate_practice(
        db=db,
        attempt_id=attempt.id,
    )

    return {
        "attempt": {
            "id": attempt.id,
            "task_id": attempt.task_id,
            "learner_id": attempt.learner_id,
            "text": attempt.text,
            "attempt_number": attempt.attempt_number,
        },
        "evaluation": evaluation,
    }


# ==========================================================
# Get Attempt History
# ==========================================================

@router.get("/{task_id}/attempts")
def list_task_attempts(
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

    attempts = get_task_attempts(
        db=db,
        task_id=task_id,
    )

    return {
        "task_id": task_id,
        "task_status": task.status,
        "total_attempts": len(attempts),
        "attempts": [
            {
                "attempt_id": attempt.id,
                "attempt_number": attempt.attempt_number,
                "text": attempt.text,
            }
            for attempt in attempts
        ],
    }