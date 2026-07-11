from sqlalchemy.orm import Session

from app.models.practice_attempt import PracticeAttempt
from app.models.practice_task import PracticeTask

from app.services.practice_task_service import (
    generate_adaptive_practice_task,
    submit_task_attempt,
)

from app.services.task_evaluation_service import (
    evaluate_task_attempt,
)


def start_practice_session(
    db: Session,
    learner_id: int,
):
    task = generate_adaptive_practice_task(
        db=db,
        learner_id=learner_id,
    )

    if isinstance(task, dict) and "error" in task:
        return task

    return {
        "session_status": "active",
        "learner_id": learner_id,
        "task": {
            "id": task.id,
            "target_skill": task.target_skill,
            "practice_type": task.practice_type,
            "difficulty": task.difficulty,
            "title": task.title,
            "instruction": task.instruction,
            "strategy": task.strategy,
            "status": task.status,
        },
    }


def submit_session_response(
    db: Session,
    learner_id: int,
    task_id: int,
    text: str,
):
    task = (
        db.query(PracticeTask)
        .filter(
            PracticeTask.id == task_id,
            PracticeTask.learner_id == learner_id,
        )
        .first()
    )

    if task is None:
        return {
            "error": "Practice task not found for this learner"
        }

    attempt = submit_task_attempt(
        db=db,
        task_id=task_id,
        text=text,
    )

    if isinstance(attempt, dict) and "error" in attempt:
        return attempt

    evaluation_result = evaluate_task_attempt(
        db=db,
        attempt_id=attempt.id,
    )

    if (
        isinstance(evaluation_result, dict)
        and "error" in evaluation_result
    ):
        return evaluation_result

    next_action = "continue"

    if task.status == "completed":
        next_action = "generate_next_task"

    elif task.status == "retry_required":
        next_action = "retry_current_task"

    return {
        "session_status": "active",
        "learner_id": learner_id,
        "task_id": task_id,
        "attempt_id": attempt.id,
        "attempt_number": attempt.attempt_number,
        "evaluation": evaluation_result,
        "next_action": next_action,
    }