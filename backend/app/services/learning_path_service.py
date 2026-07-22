from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.evaluation_records import (
    ListeningEvaluation,
    VocabularyProgress,
    SpeakingEvaluation,
    WritingEvaluation,
)
from app.models.practice_attempt import PracticeAttempt
from app.models.progress_metric import ProgressMetric
from app.models.user import User
from app.schemas.learning_path import (
    LearningPathResponse,
    LearningPathTask,
)

SKILLS = ["reading", "listening", "speaking", "writing", "vocabulary"]


@dataclass
class SkillSnapshot:
    skill: str
    score: float
    change: float


def _avg(values: list[float | int]) -> float:
    return round(sum(values) / len(values), 2) if values else 0.0


def _skill_scores(db: Session, learner_id: int) -> dict[str, float]:
    reading = (
        db.query(func.avg(ProgressMetric.task_score))
        .filter(ProgressMetric.learner_id == learner_id, ProgressMetric.target_skill == "reading")
        .scalar()
        or 0
    )
    listening = (
        db.query(func.avg(ListeningEvaluation.score))
        .filter(ListeningEvaluation.user_id == learner_id)
        .scalar()
        or 0
    )
    writing = (
        db.query(func.avg(WritingEvaluation.result["score"].as_integer()))
        .filter(WritingEvaluation.user_id == learner_id)
        .scalar()
        or 0
    )
    vocabulary = (
        db.query(func.avg(VocabularyProgress.mastery_level))
        .filter(VocabularyProgress.user_id == learner_id)
        .scalar()
        or 0
    )
    speaking_rows = db.query(SpeakingEvaluation.result).filter(SpeakingEvaluation.user_id == learner_id).all()
    speaking_scores: list[float] = []
    for (result,) in speaking_rows:
        speaking_scores.append(
            _avg(
                [
                    float(result.get("grammar_score", 0)),
                    float(result.get("vocabulary_score", 0)),
                    float(result.get("fluency_score", 0)),
                    float(result.get("pronunciation_score", 0)),
                    float(result.get("confidence_score", 0)),
                ]
            )
        )
    speaking = _avg(speaking_scores)
    return {
        "reading": round(float(reading), 2),
        "listening": round(float(listening), 2),
        "speaking": speaking,
        "writing": round(float(writing), 2),
        "vocabulary": round(float(vocabulary), 2),
    }


def _progress_change(metrics: list[ProgressMetric], skill: str | None = None) -> float:
    filtered = [m.task_score for m in metrics if skill is None or m.target_skill == skill]
    if len(filtered) < 2:
        return 0.0
    midpoint = max(1, len(filtered) // 2)
    return _avg(filtered[midpoint:]) - _avg(filtered[:midpoint])


def _level_from_score(score: float) -> str:
    if score >= 85:
        return "C1"
    if score >= 75:
        return "B2"
    if score >= 60:
        return "B1"
    if score >= 45:
        return "A2"
    return "A1"


def _milestone_for_level(level: str) -> str:
    return {
        "A1": "Reach A2",
        "A2": "Reach B1",
        "B1": "Reach B2",
        "B2": "Reach C1",
        "C1": "Reach C2",
    }.get(level, "Reach next level")


def _build_tasks(weakest: str, strongest: str, recommended: str, current_level: str) -> list[LearningPathTask]:
    return [
        LearningPathTask(title=f"Complete {recommended.title()} Practice", completed=False),
        LearningPathTask(title=f"Review {weakest.title()} Weak Spots", completed=False),
        LearningPathTask(title=f"Maintain {strongest.title()} Strength", completed=current_level in ("B2", "C1")),
    ]


def _timeline(metrics: list[ProgressMetric]) -> list[dict]:
    return [
        {"date": metric.created_at.date().isoformat(), "score": metric.task_score}
        for metric in metrics[-14:]
    ]


def _roadmap(scores: dict[str, float], recommended: str) -> list[dict]:
    ordered = sorted(scores.items(), key=lambda item: item[1])
    roadmap = []
    for skill, score in ordered:
        roadmap.append(
            {
                "skill": skill.title(),
                "priority": "high" if skill == recommended else "medium" if score < 70 else "low",
                "target_score": 80 if skill == recommended else 75,
            }
        )
    return roadmap


def get_learning_path(db: Session, learner_id: int) -> LearningPathResponse:
    metrics = (
        db.query(ProgressMetric)
        .filter(ProgressMetric.learner_id == learner_id)
        .order_by(ProgressMetric.created_at.asc())
        .all()
    )
    user = db.query(User).filter(User.id == learner_id).first()
    scores = _skill_scores(db, learner_id)
    ordered = sorted(scores.items(), key=lambda item: item[1])
    weakest = ordered[0][0] if ordered else "reading"
    strongest = ordered[-1][0] if ordered else "reading"
    recommended = weakest
    if scores.get("vocabulary", 0) >= 75 and _progress_change(metrics, "vocabulary") >= 8:
        recommended = "vocabulary"
    elif scores.get("speaking", 0) < 60:
        recommended = "speaking"
    elif scores.get("reading", 0) < 70:
        recommended = "reading"
    overall_progress = round(_avg([metric.task_score for metric in metrics]))
    current_level = _level_from_score(overall_progress)
    focus = recommended.title()
    tasks = _build_tasks(weakest, strongest, recommended, current_level)
    completed_tasks = [
        LearningPathTask(title=f"Completed {skill.title()} Session", completed=True)
        for skill, score in scores.items()
        if score >= 70
    ]
    weekly_tasks = [
        LearningPathTask(title=f"Practice {skill.title()}", completed=skill != recommended and score >= 70)
        for skill, score in scores.items()
    ]
    practice_count = db.query(func.count(PracticeAttempt.id)).filter(PracticeAttempt.learner_id == learner_id).scalar() or 0
    return LearningPathResponse(
        current_level=current_level,
        overall_progress=overall_progress,
        current_focus=focus,
        recommended_practice=recommended.title(),
        next_milestone=_milestone_for_level(current_level),
        tasks=tasks,
        weak_skills=[skill.title() for skill, score in ordered[:2]],
        strong_skills=[skill.title() for skill, score in sorted(scores.items(), key=lambda item: item[1], reverse=True)[:2]],
        learning_timeline=_timeline(metrics),
        skill_roadmap=_roadmap(scores, recommended),
        weekly_tasks=weekly_tasks,
        completed_tasks=completed_tasks,
        progress_bar=min(100, overall_progress),
        today_recommendation=f"Focus on {recommended.title()} to improve your path.",
    )


def update_learning_path(db: Session, learner_id: int) -> LearningPathResponse:
    return get_learning_path(db=db, learner_id=learner_id)
