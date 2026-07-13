from sqlalchemy.orm import Session

from app.services.adaptive_priority_service import (
    calculate_adaptive_priorities,
)


def get_weak_skills(
    db: Session,
    learner_id: int,
):
    priorities = calculate_adaptive_priorities(
        db=db,
        learner_id=learner_id,
    )

    weak_skills = []

    for item in priorities[:3]:
        score = round(100 - item["priority_score"], 2)

        if item["priority_score"] >= 70:
            priority = "High"
        elif item["priority_score"] >= 40:
            priority = "Medium"
        else:
            priority = "Low"

        weak_skills.append(
            {
                "skill": item["skill"],
                "score": score,
                "priority": priority,
                "recommendation": (
                    f"Practice {item['skill']} using "
                    f"{item['trend']} reinforcement."
                ),
            }
        )

    return weak_skills