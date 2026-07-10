from sqlalchemy.orm import Session

from app.agents.task_evaluation_agent import (
    evaluate_task_response,
)
from app.models.practice_attempt import PracticeAttempt


def evaluate_practice_task(
    db: Session,
    attempt_id: int,
    task_instruction: str,
    target_skill: str,
):

    attempt = (
        db.query(PracticeAttempt)
        .filter(
            PracticeAttempt.id == attempt_id
        )
        .first()
    )

    if attempt is None:
        return None

    evaluation = evaluate_task_response(
        task_instruction=task_instruction,
        learner_response=attempt.text,
        target_skill=target_skill,
    )

    return {
        "attempt_id": attempt.id,
        "learner_response": attempt.text,
        "task_instruction": task_instruction,
        "target_skill": target_skill,
        "task_evaluation": evaluation,
    }