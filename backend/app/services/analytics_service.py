from collections import defaultdict
from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.error_pattern import ErrorPattern
from app.models.practice_attempt import PracticeAttempt
from app.models.practice_task import PracticeTask
from app.models.progress_metric import ProgressMetric
from app.models.speaking_attempt import SpeakingAttempt


def get_overall_score(
    db: Session,
    learner_id: int,
) -> int:
    score = (
        db.query(
            func.avg(ProgressMetric.task_score)
        )
        .filter(
            ProgressMetric.learner_id == learner_id
        )
        .scalar()
    )

    return round(score or 0)


def get_skill_scores(
    db: Session,
    learner_id: int,
):
    result = (
        db.query(
            func.avg(ProgressMetric.grammar_score),
            func.avg(ProgressMetric.vocabulary_score),
            func.avg(ProgressMetric.fluency_score),
            func.avg(ProgressMetric.pronunciation_score),
        )
        .filter(
            ProgressMetric.learner_id == learner_id
        )
        .first()
    )

    if not result:
        return {
            "grammar": 0,
            "vocabulary": 0,
            "fluency": 0,
            "pronunciation": 0,
        }

    return {
        "grammar": round(result[0] or 0),
        "vocabulary": round(result[1] or 0),
        "fluency": round(result[2] or 0),
        "pronunciation": round(result[3] or 0),
    }


def get_learning_trend(
    db: Session,
    learner_id: int,
):
    metrics = (
        db.query(ProgressMetric)
        .filter(
            ProgressMetric.learner_id == learner_id
        )
        .order_by(
            ProgressMetric.created_at.desc()
        )
        .limit(7)
        .all()
    )

    metrics.reverse()

    return [
        {
            "date": metric.created_at.strftime("%Y-%m-%d"),
            "score": metric.task_score,
        }
        for metric in metrics
    ]


def get_recent_attempts(
    db: Session,
    learner_id: int,
):
    rows = (
        db.query(
            PracticeAttempt,
            PracticeTask,
            ProgressMetric,
        )
        .join(
            PracticeTask,
            PracticeAttempt.task_id == PracticeTask.id,
        )
        .join(
            ProgressMetric,
            PracticeAttempt.id == ProgressMetric.attempt_id,
        )
        .filter(
            PracticeAttempt.learner_id == learner_id,
        )
        .order_by(
            PracticeAttempt.created_at.desc(),
        )
        .limit(5)
        .all()
    )

    attempts = []

    for attempt, task, metric in rows:
        attempts.append(
            {
                "title": task.title,
                "practice_type": task.practice_type,
                "target_skill": task.target_skill,
                "score": metric.task_score,
                "date": attempt.created_at.strftime(
                    "%Y-%m-%d"
                ),
            }
        )

    return attempts


def get_weakest_skills(skill_scores: dict):
    return [
        skill.title()
        for skill, score in sorted(
            skill_scores.items(),
            key=lambda item: item[1],
        )[:2]
    ]


def get_strongest_skills(skill_scores: dict):
    return [
        skill.title()
        for skill, score in sorted(
            skill_scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:2]
    ]


def get_skill_progress(
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

    skill_groups = defaultdict(list)

    for metric in metrics:
        skill_groups[
            metric.target_skill
        ].append(metric)

    skill_progress = []

    for (
        skill,
        skill_metrics,
    ) in skill_groups.items():

        scores = [
            metric.task_score
            for metric in skill_metrics
        ]

        average_score = round(
            sum(scores) / len(scores),
            2,
        )

        first_score = scores[0]

        latest_score = scores[-1]

        score_change = (
            latest_score - first_score
        )

        if score_change >= 10:
            trend = "improving"

        elif score_change <= -10:
            trend = "declining"

        else:
            trend = "stable"

        skill_progress.append(
            {
                "skill": skill,
                "total_attempts": len(
                    skill_metrics
                ),
                "average_score": average_score,
                "first_score": first_score,
                "latest_score": latest_score,
                "score_change": score_change,
                "trend": trend,
            }
        )

    return skill_progress


def get_skill_priorities(
    db: Session,
    learner_id: int,
):
    skills = get_skill_progress(
        db=db,
        learner_id=learner_id,
    )

    priorities = []

    for skill in skills:
        priority_score = (
            100 - skill["average_score"]
        )

        if (
            skill["trend"]
            == "declining"
        ):
            priority_score += 15

        elif (
            skill["trend"]
            == "improving"
        ):
            priority_score -= 5

        priority_score = max(
            0,
            min(100, priority_score),
        )

        priorities.append(
            {
                "skill": skill["skill"],
                "priority_score": round(
                    priority_score,
                    2,
                ),
                "average_score": skill[
                    "average_score"
                ],
                "trend": skill["trend"],
            }
        )

    priorities.sort(
        key=lambda item: item[
            "priority_score"
        ],
        reverse=True,
    )

    return priorities


def _bucket_progress_by_period(
    metrics: list[ProgressMetric],
    period: str,
):
    grouped = defaultdict(
        lambda: {
            "total": 0,
            "count": 0,
        }
    )

    for metric in metrics:
        if period == "monthly":
            label = metric.created_at.strftime("%Y-%m")
        else:
            year, week, _ = metric.created_at.isocalendar()
            label = f"{year}-W{week:02d}"

        grouped[label]["total"] += metric.task_score
        grouped[label]["count"] += 1

    return [
        {
            "period": label,
            "average_score": round(
                values["total"] / values["count"],
                2,
            ),
            "practice_count": values["count"],
        }
        for label, values in sorted(grouped.items())
    ]


def get_user_analytics(
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

    speaking_attempts = (
        db.query(SpeakingAttempt)
        .filter(
            SpeakingAttempt.learner_id == learner_id
        )
        .order_by(
            SpeakingAttempt.created_at.asc()
        )
        .all()
    )

    errors = (
        db.query(ErrorPattern)
        .filter(
            ErrorPattern.learner_id == learner_id
        )
        .all()
    )

    vocabulary_scores = [
        metric.vocabulary_score
        for metric in metrics
    ]
    pronunciation_scores = [
        metric.pronunciation_score
        for metric in metrics
        if metric.pronunciation_score is not None
    ] + [
        attempt.pronunciation_score
        for attempt in speaking_attempts
    ]

    now = datetime.utcnow()
    last_week = now - timedelta(days=7)
    previous_week = now - timedelta(days=14)

    current_week_metrics = [
        metric
        for metric in metrics
        if metric.created_at >= last_week
    ]
    previous_week_metrics = [
        metric
        for metric in metrics
        if previous_week <= metric.created_at < last_week
    ]

    def average(values: list[int]) -> float:
        if not values:
            return 0

        return round(sum(values) / len(values), 2)

    current_week_score = average(
        [
            metric.task_score
            for metric in current_week_metrics
        ]
    )
    previous_week_score = average(
        [
            metric.task_score
            for metric in previous_week_metrics
        ]
    )

    return {
        "weekly_progress": _bucket_progress_by_period(
            metrics=metrics,
            period="weekly",
        ),
        "monthly_progress": _bucket_progress_by_period(
            metrics=metrics,
            period="monthly",
        ),
        "skill_improvements": get_skill_progress(
            db=db,
            learner_id=learner_id,
        ),
        "grammar_mistakes": [
            {
                "category": error.category,
                "error_type": error.error_type,
                "occurrences": error.occurrence_count,
                "resolved": error.resolved_count,
                "active": max(
                    error.occurrence_count
                    - error.resolved_count,
                    0,
                ),
            }
            for error in errors
        ],
        "vocabulary_growth": [
            {
                "date": metric.created_at.strftime("%Y-%m-%d"),
                "score": metric.vocabulary_score,
            }
            for metric in metrics
        ],
        "pronunciation_trend": [
            {
                "date": attempt.created_at.strftime("%Y-%m-%d"),
                "score": attempt.pronunciation_score,
            }
            for attempt in speaking_attempts
        ],
        "summary": {
            "average_score": get_overall_score(
                db=db,
                learner_id=learner_id,
            ),
            "weekly_change": round(
                current_week_score - previous_week_score,
                2,
            ),
            "vocabulary_growth": (
                vocabulary_scores[-1] - vocabulary_scores[0]
                if len(vocabulary_scores) >= 2
                else 0
            ),
            "pronunciation_trend": (
                pronunciation_scores[-1]
                - pronunciation_scores[0]
                if len(pronunciation_scores) >= 2
                else 0
            ),
        },
    }
