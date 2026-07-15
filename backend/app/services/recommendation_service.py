from sqlalchemy.orm import Session

from app.models.practice_task import PracticeTask
from app.services.adaptive_priority_service import (
    calculate_adaptive_priorities,
)


def get_next_recommended_task(
    db: Session,
    learner_id: int,
):
    """
    Returns the highest priority pending practice task
    based on the learner's weakest skill.
    """

    priorities = calculate_adaptive_priorities(
        db=db,
        learner_id=learner_id,
    )

    if not priorities:
        return None

    weakest_skill = priorities[0]["skill"]

    task = (
        db.query(PracticeTask)
        .filter(
            PracticeTask.learner_id == learner_id,
            PracticeTask.target_skill == weakest_skill,
            PracticeTask.status == "pending",
        )
        .order_by(
            PracticeTask.created_at.asc(),
        )
        .first()
    )

    if task:
        return task

    task = (
        db.query(PracticeTask)
        .filter(
            PracticeTask.learner_id == learner_id,
            PracticeTask.target_skill == weakest_skill,
        )
        .order_by(
            PracticeTask.created_at.desc(),
        )
        .first()
    )

    return task