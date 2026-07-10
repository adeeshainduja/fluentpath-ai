from sqlalchemy.orm import Session

from app.agents.learning_plan_agent import (
    create_learning_plan,
)
from app.memory.learner_memory import (
    get_learner_weaknesses,
)
from app.models.practice_task import PracticeTask
from app.models.practice_attempt import PracticeAttempts


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

    attempt = PracticeAttempt(
        learner_id=task.learner_id,
        task_id=task.id,
        text=text,
        attempt_number=1,
    )

    task.status = "completed"

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return attempt