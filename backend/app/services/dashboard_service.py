from collections import defaultdict

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.error_pattern import ErrorPattern
from app.models.practice_task import PracticeTask
from app.models.progress_metric import ProgressMetric
from app.services.weak_skills_service import get_weak_skills
from app.services.daily_mission_service import generate_daily_mission
from app.services.achievement_service import get_achievement_badges

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

def get_practice_history(
    db: Session,
    learner_id: int,
):
    tasks = (
        db.query(PracticeTask)
        .filter(
            PracticeTask.learner_id == learner_id
        )
        .order_by(
            PracticeTask.created_at.desc()
        )
        .limit(10)
        .all()
    )

    history = []

    for task in tasks:
        history.append(
            {
                "task_id": task.id,
                "title": task.title,
                "target_skill": task.target_skill,
                "practice_type": task.practice_type,
                "difficulty": task.difficulty,
                "status": task.status,
                "strategy": task.strategy,
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

    total_errors = 0
    active_errors = 0
    resolved_errors = 0

    for error in errors:

        distribution[error.category] = {
            "error_type": error.error_type,
            "occurrences": error.occurrence_count,
            "resolved": error.resolved_count,
            "status": error.status,
        }

        total_errors += error.occurrence_count
        resolved_errors += error.resolved_count

        active_errors += max(
            error.occurrence_count
            - error.resolved_count,
            0,
        )

    return {
        "total_errors": total_errors,
        "active_errors": active_errors,
        "resolved_errors": resolved_errors,
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
        .order_by(
            ProgressMetric.created_at.asc()
        )
        .all()
    )

    if not metrics:
        return {
            "trend": "No Data",
            "average_score": 0,
            "recent_average": 0,
            "highest_score": 0,
            "lowest_score": 0,
            "total_attempts": 0,
        }

    scores = [
        metric.task_score
        for metric in metrics
    ]

    average_score = (
        sum(scores) / len(scores)
    )

    recent_scores = scores[-5:]

    recent_average = (
        sum(recent_scores)
        / len(recent_scores)
    )

    trend = "Stable"

    if recent_average > average_score:
        trend = "Improving"

    elif recent_average < average_score:
        trend = "Declining"

    return {
        "trend": trend,
        "average_score": round(
            average_score,
            2,
        ),
        "recent_average": round(
            recent_average,
            2,
        ),
        "highest_score": max(scores),
        "lowest_score": min(scores),
        "total_attempts": len(scores),
    }

def get_dashboard_data(
    db: Session,
    learner_id: int,
):
    """
    Collect all dashboard sections into a single response.
    """

    summary = get_dashboard_summary(
        db=db,
        learner_id=learner_id,
    )

    skill_progress = get_skill_progress(
        db=db,
        learner_id=learner_id,
    )

    learning_timeline = get_learning_timeline(
        db=db,
        learner_id=learner_id,
    )

    practice_history = get_practice_history(
        db=db,
        learner_id=learner_id,
    )

    recommendation = determine_practice_strategy(
        db=db,
        learner_id=learner_id,
    )

    error_statistics = get_error_statistics(
        db=db,
        learner_id=learner_id,
    )

    trend_analytics = get_trend_analytics(
        db=db,
        learner_id=learner_id,
    )

    # Keep the API response consistent even when there is
    # not enough learner data.
    if not isinstance(recommendation, dict):
        recommendation = {}

    recommendation.setdefault(
        "strategy",
        None,
    )
    recommendation.setdefault(
        "selected_skill",
        None,
    )
    recommendation.setdefault(
        "reason",
        None,
    )

    return {
        "summary": summary,
        "skill_progress": skill_progress,
        "learning_timeline": learning_timeline,
        "practice_history": practice_history,
        "recommendations": {
            "strategy": recommendation.get("strategy"),
            "priority_skill": recommendation.get(
                "selected_skill"
            ),
            "reason": recommendation.get(
                "reason"
            ),
        },
        "error_statistics": error_statistics,
        "trend_analytics": trend_analytics,
        "weak_skills": get_weak_skills(db, learner_id),
        "daily_missions": generate_daily_mission(db, learner_id),
        "achievement_badges": get_achievement_badges(db, learner_id),
    }

