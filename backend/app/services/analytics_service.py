from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.evaluation_records import (
    ListeningEvaluation,
    SpeakingEvaluation,
    VocabularyProgress,
    WritingEvaluation,
)
from app.models.practice_attempt import PracticeAttempt
from app.models.practice_task import PracticeTask
from app.models.progress_metric import ProgressMetric
from app.models.user import User

MODULES = ("reading", "listening", "speaking", "writing", "vocabulary")


def _round(value: float | None) -> float:
    return round(float(value or 0), 2)


def _avg(values) -> float:
    clean_values = [
        float(v)
        for v in values
        if v is not None
    ]

    if not clean_values:
        return 0.0

    return _round(sum(clean_values) / len(clean_values))


def _metric_points(metrics: list[ProgressMetric]) -> list[dict]:
    return [
        {
            "date": metric.created_at.date().isoformat(),
            "score": metric.task_score,
        }
        for metric in metrics
    ]


def _bucket_by_week(metrics: list[ProgressMetric]) -> list[dict]:
    grouped: dict[str, list[int]] = defaultdict(list)
    for metric in metrics:
        year, week, _ = metric.created_at.isocalendar()
        grouped[f"{year}-W{week:02d}"].append(metric.task_score)
    return [
        {
            "period": period,
            "average_score": _avg(scores),
            "practice_count": len(scores),
        }
        for period, scores in sorted(grouped.items())
    ]


def _bucket_by_month(metrics: list[ProgressMetric]) -> list[dict]:
    grouped: dict[str, list[int]] = defaultdict(list)
    for metric in metrics:
        grouped[metric.created_at.strftime("%Y-%m")].append(metric.task_score)
    return [
        {
            "period": period,
            "average_score": _avg(scores),
            "practice_count": len(scores),
        }
        for period, scores in sorted(grouped.items())
    ]


def _bucket_by_day(metrics: list[ProgressMetric]) -> list[dict]:
    grouped: dict[str, list[int]] = defaultdict(list)
    for metric in metrics:
        grouped[metric.created_at.date().isoformat()].append(metric.task_score)
    return [
        {
            "date": day,
            "average_score": _avg(scores),
            "practice_count": len(scores),
        }
        for day, scores in sorted(grouped.items())
    ]


def _get_daily_streak(db: Session, learner_id: int) -> int:
    dates = (
        db.query(func.date(PracticeAttempt.created_at))
        .filter(PracticeAttempt.learner_id == learner_id)
        .distinct()
        .order_by(func.date(PracticeAttempt.created_at).desc())
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


def _recent_improvement(metrics: list[ProgressMetric]) -> float:
    if len(metrics) < 2:
        return 0.0
    split = max(1, len(metrics) // 2)
    first_half = metrics[:split]
    second_half = metrics[split:]
    return _avg([m.task_score for m in second_half]) - _avg([m.task_score for m in first_half])


def _module_averages(db: Session, learner_id: int) -> dict[str, float]:
    reading = _avg(
        [
            score
            for (score,) in db.query(func.avg(ProgressMetric.task_score))
            .filter(ProgressMetric.learner_id == learner_id, ProgressMetric.target_skill == "reading")
            .all()
        ]
    )
    listening = _avg(
        [
            score
            for (score,) in db.query(func.avg(ListeningEvaluation.score))
            .filter(ListeningEvaluation.user_id == learner_id)
            .all()
        ]
    )
    writing = _avg(
        [
            score
            for (score,) in db.query(func.avg(WritingEvaluation.result["score"].as_integer()))
            .filter(WritingEvaluation.user_id == learner_id)
            .all()
        ]
    )
    vocabulary = _avg(
        [
            score
            for (score,) in db.query(func.avg(VocabularyProgress.mastery_level))
            .filter(VocabularyProgress.user_id == learner_id)
            .all()
        ]
    )
    speaking_rows = db.query(SpeakingEvaluation.result).filter(SpeakingEvaluation.user_id == learner_id).all()
    speaking_scores: list[float] = []
    for (result,) in speaking_rows:
        components = [
            float(result.get("grammar_score", 0)),
            float(result.get("vocabulary_score", 0)),
            float(result.get("fluency_score", 0)),
            float(result.get("pronunciation_score", 0)),
            float(result.get("confidence_score", 0)),
        ]
        speaking_scores.append(sum(components) / len(components))
    speaking = _avg(speaking_scores)
    return {
        "reading": reading,
        "listening": listening,
        "speaking": speaking,
        "writing": writing,
        "vocabulary": vocabulary,
    }


def get_skill_progress(db: Session, learner_id: int) -> list[dict]:
    metrics = (
        db.query(ProgressMetric)
        .filter(ProgressMetric.learner_id == learner_id)
        .order_by(ProgressMetric.created_at.asc())
        .all()
    )
    groups: dict[str, list[ProgressMetric]] = defaultdict(list)
    for metric in metrics:
        groups[metric.target_skill or "unknown"].append(metric)
    result: list[dict] = []
    for skill, skill_metrics in groups.items():
        scores = [metric.task_score for metric in skill_metrics]
        change = scores[-1] - scores[0] if len(scores) > 1 else 0
        trend = "improving" if change >= 10 else "declining" if change <= -10 else "stable"
        result.append(
            {
                "skill": skill,
                "total_attempts": len(skill_metrics),
                "average_score": _avg(scores),
                "first_score": scores[0],
                "latest_score": scores[-1],
                "score_change": change,
                "trend": trend,
            }
        )
    return sorted(result, key=lambda item: item["average_score"])


def get_skill_priorities(db: Session, learner_id: int) -> list[dict]:
    skills = get_skill_progress(db=db, learner_id=learner_id)
    priorities = []
    for skill in skills:
        score = max(0.0, min(100.0, 100 - skill["average_score"] + (15 if skill["trend"] == "declining" else -5 if skill["trend"] == "improving" else 0)))
        priorities.append(
            {
                "skill": skill["skill"],
                "priority_score": _round(score),
                "average_score": skill["average_score"],
                "trend": skill["trend"],
            }
        )
    return sorted(priorities, key=lambda item: item["priority_score"], reverse=True)


def get_recent_attempts(db: Session, learner_id: int) -> list[dict]:
    rows = (
        db.query(PracticeAttempt, PracticeTask, ProgressMetric)
        .outerjoin(PracticeTask, PracticeAttempt.task_id == PracticeTask.id)
        .outerjoin(ProgressMetric, PracticeAttempt.id == ProgressMetric.attempt_id)
        .filter(PracticeAttempt.learner_id == learner_id)
        .order_by(PracticeAttempt.created_at.desc())
        .limit(5)
        .all()
    )
    attempts = []
    for attempt, task, metric in rows:
        attempts.append(
            {
                "title": task.title if task else "Practice",
                "practice_type": task.practice_type if task else attempt.practice_type,
                "target_skill": task.target_skill if task else None,
                "score": metric.task_score if metric else None,
                "date": attempt.created_at.date().isoformat(),
            }
        )
    return attempts


def get_learner_analytics(db: Session, learner_id: int) -> dict:
    metrics = (
        db.query(ProgressMetric)
        .filter(ProgressMetric.learner_id == learner_id)
        .order_by(ProgressMetric.created_at.asc())
        .all()
    )
    user = db.query(User).filter(User.id == learner_id).first()
    attempts_count = db.query(func.count(PracticeAttempt.id)).filter(PracticeAttempt.learner_id == learner_id).scalar() or 0
    total_minutes = db.query(func.coalesce(func.sum(ProgressMetric.response_length), 0)).filter(ProgressMetric.learner_id == learner_id).scalar() or 0
    avg_score = _avg([metric.task_score for metric in metrics])
    latest = metrics[-1].task_score if metrics else 0
    previous = metrics[-2].task_score if len(metrics) >= 2 else latest
    weekly = [m for m in metrics if m.created_at >= datetime.now(timezone.utc) - timedelta(days=7)]
    monthly = [m for m in metrics if m.created_at >= datetime.now(timezone.utc) - timedelta(days=30)]
    module_averages = _module_averages(db, learner_id)
    skill_progress = get_skill_progress(db=db, learner_id=learner_id)
    weakest = min(module_averages.items(), key=lambda item: item[1])[0] if module_averages else "reading"
    strongest = max(module_averages.items(), key=lambda item: item[1])[0] if module_averages else "reading"
    practice_distribution_rows = (
        db.query(PracticeAttempt.practice_type, func.count(PracticeAttempt.id))
        .filter(PracticeAttempt.learner_id == learner_id)
        .group_by(PracticeAttempt.practice_type)
        .all()
    )
    practice_distribution = [
        {"practice_type": practice_type, "count": count, "percentage": round((count / attempts_count) * 100, 2) if attempts_count else 0}
        for practice_type, count in practice_distribution_rows
    ]
    weekly_scores = _bucket_by_week(metrics)
    monthly_scores = _bucket_by_month(metrics)
    daily_activity = _bucket_by_day(metrics)
    improvement = _recent_improvement(metrics)
    week_start = datetime.utcnow() - timedelta(days=7)
    prev_week_start = datetime.utcnow() - timedelta(days=14)
    current_week = [m.task_score for m in metrics if m.created_at >= week_start]
    previous_week = [m.task_score for m in metrics if prev_week_start <= m.created_at < week_start]
    weekly_change = _avg(current_week) - _avg(previous_week)
    monthly_change = (
        _avg([m.task_score for m in monthly[-7:]]) - _avg([m.task_score for m in monthly[:-7]])
        if len(monthly) > 7
        else _avg([m.task_score for m in monthly])
    )
    return {
        "overall_performance": _round(avg_score),
        "average_score": _round(avg_score),
        "total_practices": int(attempts_count),
        "practice_minutes": int(total_minutes),
        "weekly_progress": _round(weekly_change),
        "monthly_progress": _round(monthly_change),
        "reading_accuracy": module_averages["reading"],
        "listening_accuracy": module_averages["listening"],
        "speaking_accuracy": module_averages["speaking"],
        "writing_accuracy": module_averages["writing"],
        "vocabulary_accuracy": module_averages["vocabulary"],
        "daily_streak": _get_daily_streak(db, learner_id),
        "weakest_skill": weakest,
        "strongest_skill": strongest,
        "practice_distribution": practice_distribution,
        "recent_improvement": _round(improvement),
        "skill_trend": skill_progress,
        "weekly_score_trend": weekly_scores,
        "monthly_score_trend": monthly_scores,
        "practice_type_distribution": practice_distribution,
        "skill_comparison": [
            {"skill": skill, "score": score}
            for skill, score in module_averages.items()
        ],
        "progress_timeline": _metric_points(metrics),
        "daily_activity": daily_activity,
        "recent_attempts": get_recent_attempts(db=db, learner_id=learner_id),
        "weakest_skill_insight": weakest,
        "strongest_skill_insight": strongest,
        "insights": _build_insights(module_averages, weekly_change, improvement, weakest, strongest),
        "summary": {
            "average_score": _round(avg_score),
            "weekly_change": _round(weekly_change),
            "monthly_change": _round(monthly_change),
            "recent_improvement": _round(improvement),
        },
    }


def _build_insights(
    module_averages: dict[str, float],
    weekly_change: float,
    improvement: float,
    weakest: str,
    strongest: str,
) -> list[str]:
    insights = []
    if improvement > 0:
        insights.append(f"Your overall score improved by {round(improvement, 1)}% across recent practices.")
    if weekly_change > 0:
        insights.append(f"Your daily consistency increased by {round(weekly_change, 1)}% this week.")
    if strongest:
        insights.append(f"{strongest.title()} is becoming your strongest skill.")
    if weakest:
        insights.append(f"{weakest.title()} needs additional practice.")
    if module_averages.get("reading", 0) > module_averages.get("speaking", 0):
        insights.append("Reading is currently ahead of speaking performance.")
    return insights[:4]


def get_user_analytics(db: Session, learner_id: int):
    return get_learner_analytics(db=db, learner_id=learner_id)
