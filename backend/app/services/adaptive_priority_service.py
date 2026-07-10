from sqlalchemy.orm import Session

from app.models.error_pattern import ErrorPattern
from app.services.analytics_service import (
    get_skill_progress,
)


def calculate_adaptive_priorities(
    db: Session,
    learner_id: int,
):
    # ---------------------------------------------
    # 1. Load skill analytics
    # ---------------------------------------------

    skill_progress = get_skill_progress(
        db=db,
        learner_id=learner_id,
    )

    # ---------------------------------------------
    # 2. Load recurring error patterns
    # ---------------------------------------------

    error_patterns = (
        db.query(ErrorPattern)
        .filter(
            ErrorPattern.learner_id == learner_id
        )
        .all()
    )

    # ---------------------------------------------
    # 3. Create combined skill dictionary
    # ---------------------------------------------

    combined = {}

    for skill in skill_progress:
        skill_name = skill["skill"]

        combined[skill_name] = {
            "skill": skill_name,
            "average_score": skill["average_score"],
            "latest_score": skill["latest_score"],
            "trend": skill["trend"],
            "error_frequency": 0,
        }

    # ---------------------------------------------
    # 4. Add error memory information
    # ---------------------------------------------

    for pattern in error_patterns:
        category = pattern.category

        if category not in combined:
            combined[category] = {
                "skill": category,
                "average_score": None,
                "latest_score": None,
                "trend": "unknown",
                "error_frequency": 0,
            }

        active_error_count = max(
            pattern.occurrence_count
            - pattern.resolved_count,
            0,
        )

        combined[category]["error_frequency"] += (
            active_error_count
        )

    # ---------------------------------------------
    # 5. Calculate adaptive priority score
    # ---------------------------------------------

    priorities = []

    for skill_data in combined.values():

        average_score = skill_data["average_score"]
        error_frequency = skill_data["error_frequency"]
        trend = skill_data["trend"]

        # Performance weakness: maximum 60 points
        if average_score is not None:
            performance_priority = (
                (100 - average_score) * 0.6
            )
        else:
            performance_priority = 0

        # Repeated errors: maximum 30 points
        error_priority = min(
            error_frequency * 5,
            30,
        )

        # Trend adjustment
        trend_priority = 0

        if trend == "declining":
            trend_priority = 10

        elif trend == "improving":
            trend_priority = -5

        final_priority = (
            performance_priority
            + error_priority
            + trend_priority
        )

        final_priority = max(
            0,
            min(100, final_priority),
        )

        priorities.append(
            {
                "skill": skill_data["skill"],
                "priority_score": round(
                    final_priority,
                    2,
                ),
                "average_score": average_score,
                "latest_score": (
                    skill_data["latest_score"]
                ),
                "trend": trend,
                "error_frequency": error_frequency,
                "priority_breakdown": {
                    "performance": round(
                        performance_priority,
                        2,
                    ),
                    "error_memory": round(
                        error_priority,
                        2,
                    ),
                    "trend_adjustment": (
                        trend_priority
                    ),
                },
            }
        )

    priorities.sort(
        key=lambda item: item["priority_score"],
        reverse=True,
    )

    return priorities