from collections import defaultdict

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.error_pattern import ErrorPattern
from app.models.practice_task import PracticeTask
from app.models.progress_metric import ProgressMetric

from app.services.adaptive_priority_service import (
    calculate_adaptive_priorities,
)
from app.services.analytics_service import (
    get_skill_progress,
)
from app.services.practice_strategy_service import (
    determine_practice_strategy,
)


def get_dashboard_summary(
    db: Session,
    learner_id: int,
):
    average_score = (
        db.query(
            func.avg(
                ProgressMetric.task_score
            )
        )
        .filter(
            ProgressMetric.learner_id == learner_id
        )
        .scalar()
        or 0
    )

    completed_tasks = (
        db.query(PracticeTask)
        .filter(
            PracticeTask.learner_id == learner_id,
            PracticeTask.status == "completed",
        )
        .count()
    )

    pending_tasks = (
        db.query(PracticeTask)
        .filter(
            PracticeTask.learner_id == learner_id,
            PracticeTask.status != "completed",
        )
        .count()
    )

    skill_progress = get_skill_progress(
        db=db,
        learner_id=learner_id,
    )

    trend = "No Data"

    if skill_progress:
        trend = skill_progress[0]["trend"]

    priorities = calculate_adaptive_priorities(
        db=db,
        learner_id=learner_id,
    )

    recommended_skill = (
        priorities[0]["skill"]
        if priorities
        else None
    )

    recommendation = determine_practice_strategy(
        db=db,
        learner_id=learner_id,
    )

    return {
        "average_score": round(
            average_score,
            2,
        ),
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "learning_trend": trend,
        "recommended_skill": recommended_skill,
        "recommended_strategy": (
            recommendation.get("strategy")
            if isinstance(recommendation, dict)
            else None
        ),
    }


def get_learning_timeline(
    db: Session,
    learner_id: int,
):
    metrics = (
        db.query(ProgressMetric)
        .filter(
            ProgressMetric.learner_id == learner_id
        )
        .order_by(
            ProgressMetric.created_at.asc()
        )
        .all()
    )

    timeline = defaultdict(
        lambda: {
            "attempts": 0,
            "score": 0,
        }
    )

    for metric in metrics:

        day = (
            metric.created_at
            .date()
            .isoformat()
        )

        timeline[day]["attempts"] += 1
        timeline[day]["score"] += (
            metric.task_score
        )

    result = []

    for day, values in sorted(
        timeline.items()
    ):
        result.append(
            {
                "date": day,
                "practice_count": values[
                    "attempts"
                ],
                "average_score": round(
                    values["score"]
                    / values["attempts"],
                    2,
                ),
            }
        )

    return result
