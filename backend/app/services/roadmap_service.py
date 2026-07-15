from sqlalchemy.orm import Session

from app.models.practice_task import PracticeTask
from app.schemas.learning_path import RoadmapItem

from app.services.adaptive_priority_service import (
    calculate_adaptive_priorities,
)


def generate_learning_roadmap(
    db: Session,
    learner_id: int,
):
    """
    Generate a personalized learning roadmap
    using learner priorities and practice tasks.
    """

    priorities = calculate_adaptive_priorities(
        db=db,
        learner_id=learner_id,
    )

    roadmap = []

    task_id = 1

    for priority in priorities:

        tasks = (
            db.query(PracticeTask)
            .filter(
                PracticeTask.learner_id == learner_id,
                PracticeTask.target_skill == priority["skill"],
            )
            .order_by(
                PracticeTask.created_at.asc(),
            )
            .all()
        )

        for task in tasks:

            if task.status == "completed":
                status = "completed"

            elif len(roadmap) == 0:
                status = "current"

            else:
                status = "locked"

            roadmap.append(
                RoadmapItem(
                    id=task_id,
                    title=task.title,
                    skill=task.target_skill,
                    difficulty=task.difficulty,
                    estimated_minutes=20,
                    status=status,
                )
            )

            task_id += 1

    # ------------------------------------------
    # Fallback if learner has no tasks
    # ------------------------------------------

    if not roadmap:

        roadmap.append(
            RoadmapItem(
                id=1,
                title="Grammar Basics",
                skill="Grammar",
                difficulty="Beginner",
                estimated_minutes=20,
                status="current",
            )
        )

    return roadmap