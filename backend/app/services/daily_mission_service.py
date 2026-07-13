from sqlalchemy.orm import Session

from app.services.adaptive_priority_service import (
    calculate_adaptive_priorities,
)


def generate_daily_mission(
    db: Session,
    learner_id: int,
):
    priorities = calculate_adaptive_priorities(
        db=db,
        learner_id=learner_id,
    )

    missions = []

    for item in priorities[:3]:
        missions.append(
            {
                "skill": item["skill"],
                "target": 2,
                "completed": 0,
                "priority": item["priority_score"],
            }
        )

    return missions