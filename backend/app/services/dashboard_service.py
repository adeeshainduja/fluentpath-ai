from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from app.models.evaluation_records import (
    Achievement,
    ListeningEvaluation,
    VocabularyProgress,
    SpeakingEvaluation,
    WritingEvaluation,
)
from app.models.practice_attempt import PracticeAttempt
from app.models.practice_task import PracticeTask
from app.models.progress_metric import ProgressMetric
from app.models.user import User
from app.services.analytics_service import get_skill_progress
from app.services.analytics_service import get_recent_attempts
from app.services.weak_skills_service import get_weak_skills
from app.services.daily_mission_service import generate_daily_mission
from app.services.achievement_service import get_achievement_badges
from app.services.practice_strategy_service import determine_practice_strategy
from app.services.adaptive_priority_service import calculate_adaptive_priorities
from app.services.analytics_service import get_user_analytics
from app.services.practice_history_service import get_practice_history_items


def _round_score(value: float | None) -> float:
    return round(float(value or 0), 2)


def _average(query_result: float | None) -> float:
    return _round_score(query_result)


def _get_daily_streak(db: Session, learner_id: int) -> int:
    dates = (
        db.query(func.date(PracticeAttempt.created_at))
        .join(
            PracticeTask,
            PracticeAttempt.task_id == PracticeTask.id,
        )
        .filter(
            PracticeAttempt.learner_id == learner_id,
            PracticeTask.status == "completed",
        )
        .distinct()
        .order_by(desc(func.date(PracticeAttempt.created_at)))
        .all()
    )

    if not dates:
        return 0

    streak = 1
    current = dates[0][0]

    for row in dates[1:]:
        day = row[0]
        if current - day == timedelta(days=1):
            streak += 1
            current = day
        else:
            break

    return streak


def _get_weekly_progress(db: Session, learner_id: int) -> tuple[int, int, float]:
    today = datetime.now(timezone.utc).date()
    week_start = today - timedelta(days=6)

    completed_this_week = (
        db.query(func.count(PracticeTask.id))
        .filter(
            PracticeTask.learner_id == learner_id,
            PracticeTask.status == "completed",
            func.date(PracticeTask.created_at) >= week_start,
        )
        .scalar()
        or 0
    )

    user = db.query(User).filter(User.id == learner_id).first()
    daily_goal = user.daily_goal if user and user.daily_goal else 1
    weekly_target = max(int(daily_goal) * 7, 1)
    progress = min((completed_this_week / weekly_target) * 100, 100.0)
    return completed_this_week, weekly_target, round(progress, 2)


def _get_latest_practice(db: Session, learner_id: int):
    history = get_practice_history_items(db=db, learner_id=learner_id)

    if not history:
        return None

    latest = history[0]

    return {
        "task_id": latest.attempt_id,
        "title": latest.title,
        "practice_type": latest.practice_type,
        "target_skill": latest.target_skill,
        "score": latest.score,
        "created_at": latest.completed_date,
    }


def _get_skill_average(db: Session, learner_id: int, skill: str) -> float:
    return _average(
        db.query(func.avg(ProgressMetric.task_score))
        .filter(
            ProgressMetric.learner_id == learner_id,
            ProgressMetric.target_skill == skill,
        )
        .scalar()
    )


def _get_writing_average(db: Session, learner_id: int) -> float:
    return _average(
        db.query(func.avg(WritingEvaluation.result["score"].as_integer()))
        .filter(WritingEvaluation.user_id == learner_id)
        .scalar()
    )


def _get_vocabulary_average(db: Session, learner_id: int) -> float:
    return _average(
        db.query(func.avg(VocabularyProgress.mastery_level))
        .filter(VocabularyProgress.user_id == learner_id)
        .scalar()
    )


def _get_listening_average(db: Session, learner_id: int) -> float:
    return _average(
        db.query(func.avg(ListeningEvaluation.score))
        .filter(ListeningEvaluation.user_id == learner_id)
        .scalar()
    )


def _get_speaking_average(db: Session, learner_id: int) -> float:
    evaluations = (
        db.query(SpeakingEvaluation.result)
        .filter(SpeakingEvaluation.user_id == learner_id)
        .all()
    )

    if not evaluations:
        return 0.0

    scores: list[float] = []
    for (result,) in evaluations:
        component_scores = [
            float(result.get("grammar_score", 0)),
            float(result.get("vocabulary_score", 0)),
            float(result.get("fluency_score", 0)),
            float(result.get("pronunciation_score", 0)),
            float(result.get("confidence_score", 0)),
        ]
        scores.append(sum(component_scores) / len(component_scores))

    return _round_score(sum(scores) / len(scores))


def _get_achievements(db: Session, learner_id: int):
    earned = (
        db.query(Achievement)
        .filter(Achievement.user_id == learner_id)
        .order_by(Achievement.earned_at.desc().nullslast())
        .all()
    )

    return [
        {
            "title": item.title,
            "description": item.description,
            "earned": True,
            "icon": "award",
        }
        for item in earned
    ]


def get_dashboard_data(db: Session, learner_id: int):
    user = db.query(User).filter(User.id == learner_id).first()

    total_practices = (
        db.query(func.count(PracticeTask.id))
        .filter(
            PracticeTask.learner_id == learner_id,
            PracticeTask.status == "completed",
        )
        .scalar()
        or 0
    )

    average_score = _average(
        db.query(func.avg(ProgressMetric.task_score))
        .filter(ProgressMetric.learner_id == learner_id)
        .scalar()
    )

    reading_score = _get_skill_average(db, learner_id, "reading")
    listening_score = _get_listening_average(db, learner_id)
    speaking_score = _get_speaking_average(db, learner_id)
    vocabulary_score = _get_vocabulary_average(db, learner_id)
    writing_score = _get_writing_average(db, learner_id)

    completed_this_week, weekly_target, weekly_progress = _get_weekly_progress(
        db, learner_id
    )

    skill_progress = get_skill_progress(db=db, learner_id=learner_id)
    recommendations = determine_practice_strategy(db=db, learner_id=learner_id)
    weak_skills = get_weak_skills(db=db, learner_id=learner_id)
    daily_missions = generate_daily_mission(db=db, learner_id=learner_id)
    achievement_badges = get_achievement_badges(db=db, learner_id=learner_id)
    analytics = get_user_analytics(db=db, learner_id=learner_id)

    learning_timeline = analytics.get("weekly_progress", [])
    practice_history = get_recent_attempts(db=db, learner_id=learner_id)

    summary = {
        "average_score": average_score,
        "daily_streak": _get_daily_streak(db, learner_id),
        "total_practices": total_practices,
        "completed_tasks": total_practices,
        "pending_tasks": 0,
        "learning_trend": "Stable",
        "recommended_skill": (
            calculate_adaptive_priorities(db=db, learner_id=learner_id)[0]["skill"]
            if calculate_adaptive_priorities(db=db, learner_id=learner_id)
            else None
        ),
        "recommended_strategy": (
            recommendations.get("strategy")
            if isinstance(recommendations, dict)
            else None
        ),
    }

    return {
        "learner_name": user.full_name if user else "Learner",
        "total_practices": total_practices,
        "average_score": average_score,
        "reading_score": reading_score,
        "listening_score": listening_score,
        "speaking_score": speaking_score,
        "writing_score": writing_score,
        "vocabulary_score": vocabulary_score,
        "daily_streak": _get_daily_streak(db, learner_id),
        "weekly_goal_progress": {
            "completed": completed_this_week,
            "target": weekly_target,
            "percentage": weekly_progress,
        },
        "completed_practices_this_week": completed_this_week,
        "achievements": _get_achievements(db, learner_id),
        "latest_practice": _get_latest_practice(db, learner_id),
        "ai_recommendation_summary": (
            "Keep building consistency and focus on your weakest recent skill."
            if total_practices
            else "Start with one practice module to establish a baseline."
        ),
        "summary": summary,
        "skill_progress": skill_progress,
        "learning_timeline": learning_timeline,
        "practice_history": practice_history,
        "recommendations": {
            "strategy": recommendations.get("strategy") if isinstance(recommendations, dict) else None,
            "priority_skill": recommendations.get("selected_skill") if isinstance(recommendations, dict) else None,
            "selected_skill": recommendations.get("selected_skill") if isinstance(recommendations, dict) else None,
            "reason": recommendations.get("reason") if isinstance(recommendations, dict) else None,
        },
        "error_statistics": {
            "total_errors": analytics.get("grammar_mistakes", []).__len__(),
            "active_errors": analytics.get("grammar_mistakes", []).__len__(),
            "resolved_errors": 0,
            "error_distribution": {},
        },
        "trend_analytics": analytics.get("summary", {}),
        "weak_skills": weak_skills,
        "daily_missions": daily_missions,
        "achievement_badges": achievement_badges,
    }
