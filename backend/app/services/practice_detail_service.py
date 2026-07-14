from sqlalchemy.orm import Session

from app.models.practice_task import PracticeTask


def get_practice_detail(
    db: Session,
    task_id: int,
):
    task = (
        db.query(PracticeTask)
        .filter(PracticeTask.id == task_id)
        .first()
    )

    if not task:
        return None

    return {
        "id": task.id,
        "title": task.title,
        "instruction": task.instruction,
        "target_skill": task.target_skill,
        "practice_type": task.practice_type,
        "difficulty": task.difficulty,
        "strategy": task.strategy,
        "status": task.status,
        "created_at": task.created_at,
    }