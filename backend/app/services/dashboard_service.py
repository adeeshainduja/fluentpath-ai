from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.progress_metric import ProgressMetric
from app.models.practice_task import PracticeTask
from app.services.analytics_service import get_skill_progress
from app.services.adaptive_priority_service import (
    calculate_adaptive_priorities,
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
    )

    if average_score is None:
        average_score = 0

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

    skills = get_skill_progress(
        db=db,
        learner_id=learner_id,
    )

    trend = "No Data"

    if skills:
        trend = skills[0]["trend"]

    priorities = calculate_adaptive_priorities(
        db=db,
        learner_id=learner_id,
    )

    recommended_skill = (
        priorities[0]["skill"]
        if priorities
        else "None"
    )

    strategy_result = determine_practice_strategy(
        db=db,
        learner_id=learner_id,
    )

    return {
        "overall_score": round(
            average_score,
            2,
        ),
        "average_score": round(
            average_score,
            2,
        ),
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "learning_trend": trend,
        "recommended_skill": recommended_skill,
        "recommended_strategy": strategy_result["strategy"],
    }