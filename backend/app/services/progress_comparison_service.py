from sqlalchemy.orm import Session

from app.agents.progress_comparison_agent import (
    compare_attempt_progress,
)
from app.models.practice_attempt import PracticeAttempt
from app.models.practice_task import PracticeTask


def compare_task_attempts(
    db: Session,
    task_id: int,
    previous_attempt_id: int,
    current_attempt_id: int,
):
    task = (
        db.query(PracticeTask)
        .filter(
            PracticeTask.id == task_id
        )
        .first()
    )

    if task is None:
        return {
            "error": "Practice task not found"
        }

    previous_attempt = (
        db.query(PracticeAttempt)
        .filter(
            PracticeAttempt.id == previous_attempt_id
        )
        .first()
    )

    current_attempt = (
        db.query(PracticeAttempt)
        .filter(
            PracticeAttempt.id == current_attempt_id
        )
        .first()
    )

    if previous_attempt is None or current_attempt is None:
        return {
            "error": "One or both attempts were not found"
        }

    if (
        previous_attempt.task_id != task_id
        or current_attempt.task_id != task_id
    ):
        return {
            "error": (
                "Both attempts must belong to "
                "the same practice task"
            )
        }

    if (
        current_attempt.attempt_number
        <= previous_attempt.attempt_number
    ):
        return {
            "error": (
                "Current attempt must be newer "
                "than previous attempt"
            )
        }

    comparison = compare_attempt_progress(
        task_instruction=task.instruction,
        target_skill=task.target_skill,
        previous_response=previous_attempt.text,
        current_response=current_attempt.text,
    )

    return {
        "task_id": task.id,
        "target_skill": task.target_skill,
        "previous_attempt": {
            "id": previous_attempt.id,
            "attempt_number": previous_attempt.attempt_number,
            "text": previous_attempt.text,
        },
        "current_attempt": {
            "id": current_attempt.id,
            "attempt_number": current_attempt.attempt_number,
            "text": current_attempt.text,
        },
        "comparison": comparison,
    }