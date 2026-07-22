from __future__ import annotations

from sqlalchemy.orm import Session

from app.memory.learner_memory import get_learner_weaknesses
from app.models.error_pattern import ErrorPattern
from app.models.practice_attempt import PracticeAttempt
from app.models.progress_metric import ProgressMetric
from app.services.analytics_service import get_user_analytics
from app.services.learning_path_service import get_learning_path


def _score_to_difficulty(score: float, improving: float = 0.0) -> str:
    if score < 50:
        return "Beginner"
    if score < 70:
        return "Intermediate"
    if improving > 8:
        return "Advanced"
    return "Intermediate"


def _priority_for(skill: str, score: float, streak_broken: bool, improving: float = 0.0) -> str:
    if streak_broken or score < 60:
        return "High"
    if improving > 8 or score >= 80:
        return "Medium"
    return "High" if skill in {"speaking", "vocabulary"} and score < 70 else "Medium"


def _estimated_time(priority: str, streak_broken: bool) -> str:
    if streak_broken:
        return "10 minutes"
    return "15 minutes" if priority == "High" else "20 minutes"


def get_adaptive_practice_recommendation(
    db: Session,
    learner_id: int,
) -> dict:
    analytics = get_user_analytics(db=db, learner_id=learner_id)
    learning_path = get_learning_path(db=db, learner_id=learner_id)
    weaknesses = get_learner_weaknesses(db=db, learner_id=learner_id)

    metrics = (
        db.query(ProgressMetric)
        .filter(ProgressMetric.learner_id == learner_id)
        .order_by(ProgressMetric.created_at.asc())
        .all()
    )
    attempts = (
        db.query(PracticeAttempt)
        .filter(PracticeAttempt.learner_id == learner_id)
        .order_by(PracticeAttempt.created_at.desc())
        .limit(5)
        .all()
    )

    weak_skill = learning_path.current_focus.lower()
    if weaknesses:
        weak_skill = weaknesses[0].category.lower()
    if analytics.get("speaking_accuracy", 100) < 60:
        weak_skill = "speaking"
    elif analytics.get("vocabulary_accuracy", 100) < 70:
        weak_skill = "vocabulary"
    elif analytics.get("reading_accuracy", 100) < 70:
        weak_skill = "reading"
    elif analytics.get("listening_accuracy", 100) < 70:
        weak_skill = "listening"
    elif analytics.get("writing_accuracy", 100) < 70:
        weak_skill = "writing"

    skill_scores = {
        "reading": analytics.get("reading_accuracy", 0),
        "listening": analytics.get("listening_accuracy", 0),
        "speaking": analytics.get("speaking_accuracy", 0),
        "writing": analytics.get("writing_accuracy", 0),
        "vocabulary": analytics.get("vocabulary_accuracy", 0),
    }
    skill_score = skill_scores.get(weak_skill, 0)

    skill_metrics = [metric for metric in metrics if metric.target_skill == weak_skill]
    change = 0.0
    if len(skill_metrics) >= 2:
        midpoint = max(1, len(skill_metrics) // 2)
        first_half = skill_metrics[:midpoint]
        second_half = skill_metrics[midpoint:]
        first_avg = sum(m.task_score for m in first_half) / len(first_half)
        second_avg = sum(m.task_score for m in second_half) / len(second_half) if second_half else first_avg
        change = second_avg - first_avg

    streak_broken = analytics.get("daily_streak", 0) == 0
    priority = _priority_for(weak_skill, skill_score, streak_broken, change)
    difficulty = _score_to_difficulty(skill_score, change)

    if weak_skill == "vocabulary" and change > 8:
        difficulty = "Advanced"

    reason_parts = []
    if weak_skill == "speaking" and skill_score < 60:
        reason_parts.append("Speaking is below 60, so focused practice will have the biggest impact.")
    elif weak_skill == "vocabulary" and skill_score < 70:
        reason_parts.append("Vocabulary accuracy has dropped during the last three sessions.")
    elif weak_skill == "reading" and skill_score < 70:
        reason_parts.append("Reading accuracy is below target and needs immediate attention.")
    elif weak_skill == "writing" and skill_score < 70:
        reason_parts.append("Writing quality is still below the healthy range.")
    else:
        reason_parts.append(f"{weak_skill.title()} is the weakest current skill in your learning path.")

    if streak_broken:
        reason_parts.append("Your daily streak is broken, so a short practice will help rebuild consistency.")
    if attempts:
        reason_parts.append(f"Your last completed practice was {attempts[0].practice_type}.")

    if learning_path.recommended_practice.lower() == weak_skill:
        reason_parts.append("This also matches your current learning path focus.")

    return {
        "recommendedPractice": weak_skill.title(),
        "difficulty": difficulty,
        "reason": " ".join(reason_parts),
        "estimatedTime": _estimated_time(priority, streak_broken),
        "priority": priority,
    }
