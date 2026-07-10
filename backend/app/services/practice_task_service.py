from sqlalchemy.orm import Session

from app.agents.learning_plan_agent import (
    create_learning_plan,
)
from app.memory.learner_memory import (
    get_learner_weaknesses,
)
from app.models.practice_task import PracticeTask
from app.models.practice_attempt import PracticeAttempt


def generate_and_save_task(
    db: Session,
    learner_id: int,
):
    weaknesses = get_learner_weaknesses(
        db=db,
        learner_id=learner_id,
    )

    plan = create_learning_plan(
        learner_id=learner_id,
        weaknesses=weaknesses,
    )

    if not plan.has_recommendation:
        return {
            "error": "No weaknesses available for task generation"
        }

    recommendation = plan.recommendation

    task = PracticeTask(
        learner_id=learner_id,
        target_skill=recommendation.priority_category,
        practice_type=recommendation.practice_type,
        difficulty=recommendation.difficulty,
        title=recommendation.title,
        instruction=recommendation.instruction,
        status="pending",
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_learner_tasks(
    db: Session,
    learner_id: int,
):
    return (
        db.query(PracticeTask)
        .filter(
            PracticeTask.learner_id == learner_id
        )
        .order_by(
            PracticeTask.created_at.desc()
        )
        .all()
    )


def get_task(
    db: Session,
    task_id: int,
):
    return (
        db.query(PracticeTask)
        .filter(
            PracticeTask.id == task_id
        )
        .first()
    )

def submit_task_attempt(
    db: Session,
    task_id: int,
    text: str,
):
    task = get_task(
        db=db,
        task_id=task_id,
    )

    if task is None:
        return {
            "error": "Practice task not found"
        }

    if task.status == "completed":
        return {
            "error": "This practice task is already completed"
        }

    previous_attempt_count = (
        db.query(PracticeAttempt)
        .filter(
            PracticeAttempt.task_id == task_id
        )
        .count()
    )

    next_attempt_number = previous_attempt_count + 1

    attempt = PracticeAttempt(
        learner_id=task.learner_id,
        task_id=task.id,
        text=text,
        attempt_number=next_attempt_number,
    )

    task.status = "submitted"

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return attempt

def get_task_attempts(
    db: Session,
    task_id: int,
):
    return (
        db.query(PracticeAttempt)
        .filter(
            PracticeAttempt.task_id == task_id
        )
        .order_by(
            PracticeAttempt.attempt_number.asc()
        )
        .all()
    )