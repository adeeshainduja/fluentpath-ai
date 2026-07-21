import json
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.evaluation_records import (
    ListeningEvaluation,
    VocabularyProgress,
    WritingEvaluation,
)
from app.models.practice_attempt import PracticeAttempt
from app.models.practice_task import PracticeTask
from app.models.progress_metric import ProgressMetric
from app.models.speaking_attempt import SpeakingAttempt
from app.schemas.practice_history import (
    PracticeHistoryDetail,
    PracticeHistoryDetailResponse,
    PracticeHistoryItem,
    PracticeHistoryResponse,
    PracticeHistoryType,
)


def _safe_json_loads(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    try:
        loaded = json.loads(value)
        return loaded if isinstance(loaded, dict) else {"value": loaded}
    except json.JSONDecodeError:
        return {"raw": value}


def _build_feedback_summary(detail: dict[str, Any]) -> str | None:
    for key in ("feedback", "ai_feedback", "overall_feedback"):
        value = detail.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return None


def _summarize_strengths(answers: dict[int, str], correct_answers: dict[int, str]) -> list[str]:
    if not answers or not correct_answers:
        return []
    correct_count = sum(1 for qid, answer in answers.items() if correct_answers.get(qid) == answer)
    if correct_count == len(correct_answers):
        return ["Answered every question correctly."]
    if correct_count >= max(1, len(correct_answers) - 1):
        return ["Strong accuracy on the main ideas."]
    return ["Good persistence and completion."]


def _summarize_weaknesses(answers: dict[int, str], correct_answers: dict[int, str]) -> list[str]:
    if not answers or not correct_answers:
        return []
    incorrect = [
        qid for qid, answer in answers.items() if correct_answers.get(qid) != answer
    ]
    if not incorrect:
        return ["No major weaknesses identified."]
    return [f"Review question {incorrect[0]} and the related explanation."]


def _build_item(
    practice_type: str,
    attempt_id: int,
    title: str,
    created_at: datetime,
    score: int | None,
    duration: int | None,
    difficulty: str | None,
    feedback_summary: str | None,
    status: str,
    target_skill: str | None,
) -> PracticeHistoryItem:
    return PracticeHistoryItem(
        attempt_id=attempt_id,
        practice_type=practice_type,
        title=title,
        completed_date=created_at,
        score=score,
        duration=duration,
        difficulty=difficulty,
        feedback_summary=feedback_summary,
        status=status,
        target_skill=target_skill,
    )


def get_practice_history_items(
    db: Session,
    learner_id: int,
    practice_type: PracticeHistoryType = "all",
    sort: str = "newest",
    search: str | None = None,
) -> list[PracticeHistoryItem]:
    attempts = (
        db.query(PracticeAttempt, PracticeTask, ProgressMetric)
        .outerjoin(PracticeTask, PracticeAttempt.task_id == PracticeTask.id)
        .outerjoin(ProgressMetric, PracticeAttempt.id == ProgressMetric.attempt_id)
        .filter(PracticeAttempt.learner_id == learner_id)
        .all()
    )

    items: list[PracticeHistoryItem] = []

    for attempt, task, metric in attempts:
        payload = _safe_json_loads(attempt.text)
        task_title = task.title if task else payload.get("passage_title") or payload.get("practice_title")
        p_type = (task.practice_type if task else attempt.practice_type) or attempt.practice_type
        if practice_type != "all" and p_type != practice_type:
            continue
        if search and search.lower() not in f"{task_title or ''} {p_type}".lower():
            continue
        score = metric.task_score if metric else payload.get("score")
        feedback_summary = payload.get("feedback") or payload.get("ai_feedback")
        items.append(
            _build_item(
                practice_type=p_type,
                attempt_id=attempt.id,
                title=task_title or p_type.title(),
                created_at=attempt.created_at,
                score=int(score) if score is not None else None,
                duration=payload.get("duration") or payload.get("duration_seconds"),
                difficulty=task.difficulty if task else payload.get("difficulty"),
                feedback_summary=feedback_summary,
                status=task.status if task else "completed",
                target_skill=task.target_skill if task else payload.get("target_skill"),
            )
        )

        if task and task.practice_type == "vocabulary":
            _ = db.query(VocabularyProgress).filter(VocabularyProgress.user_id == learner_id).all()

    speaking_attempts = db.query(SpeakingAttempt).filter(SpeakingAttempt.learner_id == learner_id).all()
    for attempt in speaking_attempts:
        if practice_type != "all" and practice_type != "speaking":
            continue
        if search and search.lower() not in f"speaking {attempt.overall_feedback}".lower():
            continue
        items.append(
            _build_item(
                practice_type="speaking",
                attempt_id=attempt.id,
                title="Speaking Practice",
                created_at=attempt.created_at,
                score=round((attempt.grammar_score + attempt.vocabulary_score + attempt.fluency_score + attempt.pronunciation_score + attempt.confidence_score) / 5),
                duration=None,
                difficulty="intermediate",
                feedback_summary=attempt.overall_feedback,
                status="completed",
                target_skill="speaking",
            )
        )

    if sort == "oldest":
        items.sort(key=lambda item: item.completed_date)
    elif sort == "score_asc":
        items.sort(key=lambda item: (item.score is None, item.score or 0))
    elif sort == "score_desc":
        items.sort(key=lambda item: (item.score is None, -(item.score or 0)))
    else:
        items.sort(key=lambda item: item.completed_date, reverse=True)

    return items


def get_practice_history(
    db: Session,
    learner_id: int,
    page: int = 1,
    limit: int = 20,
    practice_type: PracticeHistoryType = "all",
    sort: str = "newest",
    search: str | None = None,
) -> PracticeHistoryResponse:
    items = get_practice_history_items(
        db=db,
        learner_id=learner_id,
        practice_type=practice_type,
        sort=sort,
        search=search,
    )
    start = (page - 1) * limit
    return PracticeHistoryResponse(
        total=len(items),
        page=page,
        limit=limit,
        items=items[start : start + limit],
    )


def get_practice_history_detail(
    db: Session,
    learner_id: int,
    attempt_id: int,
) -> PracticeHistoryDetailResponse | None:
    attempt = db.query(PracticeAttempt).filter(PracticeAttempt.id == attempt_id, PracticeAttempt.learner_id == learner_id).first()
    if attempt:
        task = db.query(PracticeTask).filter(PracticeTask.id == attempt.task_id).first() if attempt.task_id else None
        payload = _safe_json_loads(attempt.text)
        metric = db.query(ProgressMetric).filter(ProgressMetric.attempt_id == attempt.id).first()
        correct_answers = payload.get("correct_answers") or {}
        user_answers = payload.get("answers") or payload.get("user_answers") or {}
        detail = PracticeHistoryDetail(
            attempt_id=attempt.id,
            practice_type=task.practice_type if task else attempt.practice_type,
            title=task.title if task else payload.get("passage_title") or payload.get("practice_title") or "Practice",
            completed_date=attempt.created_at,
            score=metric.task_score if metric else payload.get("score"),
            duration=payload.get("duration") or payload.get("duration_seconds"),
            difficulty=task.difficulty if task else payload.get("difficulty"),
            status=task.status if task else "completed",
            original_practice=payload,
            learner_answers=user_answers,
            correct_answers=correct_answers or None,
            explanations=payload.get("explanations"),
            ai_feedback=_build_feedback_summary(payload),
            feedback_summary=_build_feedback_summary(payload),
            weaknesses=_summarize_weaknesses(user_answers, correct_answers),
            strengths=_summarize_strengths(user_answers, correct_answers),
            completion_time=attempt.created_at,
            suggestions=payload.get("suggestions", []),
        )
        return PracticeHistoryDetailResponse(history=detail)

    speaking_attempt = db.query(SpeakingAttempt).filter(SpeakingAttempt.id == attempt_id, SpeakingAttempt.learner_id == learner_id).first()
    if not speaking_attempt:
        return None

    detail = PracticeHistoryDetail(
        attempt_id=speaking_attempt.id,
        practice_type="speaking",
        title="Speaking Practice",
        completed_date=speaking_attempt.created_at,
        score=round((speaking_attempt.grammar_score + speaking_attempt.vocabulary_score + speaking_attempt.fluency_score + speaking_attempt.pronunciation_score + speaking_attempt.confidence_score) / 5),
        duration=None,
        difficulty="intermediate",
        status="completed",
        original_practice={"transcript": speaking_attempt.transcript},
        learner_answers={"transcript": speaking_attempt.transcript},
        correct_answers=None,
        explanations=None,
        ai_feedback=speaking_attempt.overall_feedback,
        feedback_summary=speaking_attempt.overall_feedback,
        weaknesses=[],
        strengths=[],
        completion_time=speaking_attempt.created_at,
        suggestions=[],
    )
    return PracticeHistoryDetailResponse(history=detail)


def get_practice_history_summary(
    db: Session,
    learner_id: int,
    practice_type: PracticeHistoryType = "all",
) -> dict:
    items = get_practice_history_items(db=db, learner_id=learner_id, practice_type=practice_type)
    scores = [item.score for item in items if item.score is not None]
    return {
        "learner_id": learner_id,
        "total_practices": len(items),
        "writing_practices": len([item for item in items if item.practice_type == "writing"]),
        "speaking_practices": len([item for item in items if item.practice_type == "speaking"]),
        "evaluated_practices": len(scores),
        "average_score": round(sum(scores) / len(scores), 2) if scores else None,
        "best_score": max(scores) if scores else None,
        "latest_score": items[0].score if items else None,
        "latest_practice_at": items[0].completed_date if items else None,
    }
