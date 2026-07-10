from sqlalchemy.orm import Session

from app.agents.task_evaluation_agent import (
    evaluate_task_response,
)
from app.models.practice_attempt import PracticeAttempt
from app.models.practice_task import PracticeTask


def evaluate_linked_practice_task(
    db: Session,
    attempt_id: int,
):
    # Find the learner attempt
    attempt = (
        db.query(PracticeAttempt)
        .filter(
            PracticeAttempt.id == attempt_id
        )
        .first()
    )

    if attempt is None:
        return {
            "error": "Practice attempt not found"
        }

    # The attempt must belong to a generated task
    if attempt.task_id is None:
        return {
            "error": (
                "This attempt is not linked "
                "to a practice task"
            )
        }

    # Load the linked task
    task = (
        db.query(PracticeTask)
        .filter(
            PracticeTask.id == attempt.task_id
        )
        .first()
    )

    if task is None:
        return {
            "error": "Linked practice task not found"
        }

    # Ask Gemini to evaluate task completion
    evaluation = evaluate_task_response(
        task_instruction=task.instruction,
        learner_response=attempt.text,
        target_skill=task.target_skill,
    )

    return {
        "attempt_id": attempt.id,
        "task_id": task.id,
        "task_title": task.title,
        "task_instruction": task.instruction,
        "target_skill": task.target_skill,
        "learner_response": attempt.text,
        "task_evaluation": evaluation,
    }