from collections import defaultdict
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.progress_metric import ProgressMetric
from app.models.practice_task import PracticeTask
from app.models.error_pattern import ErrorPattern

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
        db.query(func.avg(ProgressMetric.task_score))
        .filter(ProgressMetric.learner_id == learner_id)
        .scalar()
    ) or 0

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
        trend = skills[0].get("trend", "No Data")

    priorities = calculate_adaptive_priorities(
        db=db,
        learner_id=learner_id,
    )

    recommended_skill = (
        priorities[0]["skill"]
        if priorities
        else None
    )

    strategy = determine_practice_strategy(
        db=db,
        learner_id=learner_id,
    )

    return {
        "average_score": round(average_score, 2),
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "learning_trend": trend,
        "recommended_skill": recommended_skill,
        "recommended_strategy": strategy.get("strategy"),
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
        .order_by(ProgressMetric.created_at)
        .all()
    )

    timeline = defaultdict(
        lambda: {
            "attempts": 0,
            "score": 0,
        }
    )

    for metric in metrics:
        day = metric.created_at.date().isoformat()

        timeline[day]["attempts"] += 1
        timeline[day]["score"] += metric.task_score

    result = []

    for day, values in sorted(timeline.items()):
        result.append(
            {
                "date": day,
                "practice_count": values["attempts"],
                "average_score": round(
                    values["score"] / values["attempts"],
                    2,
                ),
            }
        )

    return result


def get_practice_history(
    db: Session,
    learner_id: int,
):
    tasks = (
        db.query(PracticeTask)
        .filter(
            PracticeTask.learner_id == learner_id
        )
        .order_by(PracticeTask.created_at.desc())
        .limit(10)
        .all()
    )

    history = []

    for task in tasks:
        history.append(
            {
                "task_id": task.id,
                "task_type": task.task_type,
                "difficulty": task.difficulty,
                "status": task.status,
                "created_at": task.created_at,
            }
        )

    return history


def get_error_statistics(
    db: Session,
    learner_id: int,
):
    errors = (
        db.query(ErrorPattern)
        .filter(
            ErrorPattern.learner_id == learner_id
        )
        .all()
    )

    distribution = {}

    for error in errors:
        error_type = error.error_type

        distribution[error_type] = (
            distribution.get(error_type, 0) + 1
        )

    return {
        "total_errors": len(errors),
        "error_distribution": distribution,
    }


def get_trend_analytics(
    db: Session,
    learner_id: int,
):
    metrics = (
        db.query(ProgressMetric)
        .filter(
            ProgressMetric.learner_id == learner_id
        )
        .order_by(ProgressMetric.created_at)
        .all()
    )

    if not metrics:
        return {
            "trend": "No Data",
            "average_score": 0,
            "recent_average": 0,
        }

    scores = [m.task_score for m in metrics]

    average = sum(scores) / len(scores)

    recent = scores[-5:]

    recent_average = sum(recent) / len(recent)

    trend = "Stable"

    if recent_average > average:
        trend = "Improving"
    elif recent_average < average:
        trend = "Declining"

    return {
        "trend": trend,
        "average_score": round(average, 2),
        "recent_average": round(recent_average, 2),
    }


def get_dashboard_data(
    db: Session,
    learner_id: int,
):
    return {
        "summary": get_dashboard_summary(
            db,
            learner_id,
        ),
        "skill_progress": get_skill_progress(
            db,
            learner_id,
        ),
        "learning_timeline": get_learning_timeline(
            db,
            learner_id,
        ),
        "practice_history": get_practice_history(
            db,
            learner_id,
        ),
        "recommendations": determine_practice_strategy(
            db,
            learner_id,
        ),
        "error_statistics": get_error_statistics(
            db,
            learner_id,
        ),
        "trend_analytics": get_trend_analytics(
            db,
            learner_id,
        ),
    }