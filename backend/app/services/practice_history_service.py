from sqlalchemy.orm import Session

from app.models.practice_attempt import PracticeAttempt
from app.models.practice_task import PracticeTask
from app.models.progress_metric import ProgressMetric
from app.models.speaking_attempt import SpeakingAttempt
from app.schemas.practice_history import (
    PracticeHistoryItem,
    PracticeHistoryResponse,
    PracticeHistorySummary,
    PracticeHistoryType,
)


def _average_score(
    scores: list[int],
) -> float | None:
    if not scores:
        return None

    return round(
        sum(scores) / len(scores),
        2,
    )


def _speaking_overall_score(
    attempt: SpeakingAttempt,
) -> int:
    scores = [
        attempt.grammar_score,
        attempt.vocabulary_score,
        attempt.fluency_score,
        attempt.pronunciation_score,
        attempt.confidence_score,
    ]

    return round(
        sum(scores) / len(scores)
    )


def _get_practice_attempt_items(
    db: Session,
    learner_id: int,
) -> list[PracticeHistoryItem]:
    rows = (
        db.query(
            PracticeAttempt,
            PracticeTask,
            ProgressMetric,
        )
        .outerjoin(
            PracticeTask,
            PracticeAttempt.task_id == PracticeTask.id,
        )
        .outerjoin(
            ProgressMetric,
            PracticeAttempt.id == ProgressMetric.attempt_id,
        )
        .filter(
            PracticeAttempt.learner_id == learner_id,
            PracticeAttempt.practice_type != "speaking",
        )
        .all()
    )

    items: list[PracticeHistoryItem] = []

    for attempt, task, metric in rows:
        practice_type = attempt.practice_type

        if task is not None:
            practice_type = task.practice_type

        items.append(
            PracticeHistoryItem(
                record_id=f"practice-{attempt.id}",
                source="practice_attempt",
                attempt_id=attempt.id,
                learner_id=attempt.learner_id,
                practice_type=practice_type,
                task_id=attempt.task_id,
                task_title=(
                    task.title
                    if task is not None
                    else None
                ),
                target_skill=(
                    task.target_skill
                    if task is not None
                    else (
                        metric.target_skill
                        if metric is not None
                        else None
                    )
                ),
                difficulty=(
                    task.difficulty
                    if task is not None
                    else None
                ),
                status=(
                    task.status
                    if task is not None
                    else None
                ),
                strategy=(
                    task.strategy
                    if task is not None
                    else None
                ),
                attempt_number=attempt.attempt_number,
                submitted_text=attempt.text,
                score=(
                    metric.task_score
                    if metric is not None
                    else None
                ),
                grammar_score=(
                    metric.grammar_score
                    if metric is not None
                    else None
                ),
                vocabulary_score=(
                    metric.vocabulary_score
                    if metric is not None
                    else None
                ),
                fluency_score=(
                    metric.fluency_score
                    if metric is not None
                    else None
                ),
                pronunciation_score=(
                    metric.pronunciation_score
                    if metric is not None
                    else None
                ),
                confidence_score=None,
                feedback=None,
                has_evaluation=metric is not None,
                created_at=attempt.created_at,
            )
        )

    return items


def _get_speaking_attempt_items(
    db: Session,
    learner_id: int,
) -> list[PracticeHistoryItem]:
    attempts = (
        db.query(SpeakingAttempt)
        .filter(
            SpeakingAttempt.learner_id == learner_id,
        )
        .all()
    )

    return [
        PracticeHistoryItem(
            record_id=f"speaking-{attempt.id}",
            source="speaking_attempt",
            attempt_id=attempt.id,
            learner_id=attempt.learner_id,
            practice_type="speaking",
            submitted_text=attempt.transcript,
            score=_speaking_overall_score(attempt),
            grammar_score=attempt.grammar_score,
            vocabulary_score=attempt.vocabulary_score,
            fluency_score=attempt.fluency_score,
            pronunciation_score=attempt.pronunciation_score,
            confidence_score=attempt.confidence_score,
            feedback=attempt.overall_feedback,
            has_evaluation=True,
            created_at=attempt.created_at,
        )
        for attempt in attempts
    ]


def _filter_by_type(
    items: list[PracticeHistoryItem],
    practice_type: PracticeHistoryType,
) -> list[PracticeHistoryItem]:
    if practice_type == "all":
        return items

    if practice_type == "writing":
        return [
            item
            for item in items
            if item.source == "practice_attempt"
        ]

    return [
        item
        for item in items
        if item.practice_type == practice_type
    ]


def get_practice_history_items(
    db: Session,
    learner_id: int,
    practice_type: PracticeHistoryType = "all",
) -> list[PracticeHistoryItem]:
    items = [
        *_get_practice_attempt_items(
            db=db,
            learner_id=learner_id,
        ),
        *_get_speaking_attempt_items(
            db=db,
            learner_id=learner_id,
        ),
    ]

    filtered_items = _filter_by_type(
        items=items,
        practice_type=practice_type,
    )

    return sorted(
        filtered_items,
        key=lambda item: item.created_at,
        reverse=True,
    )


def get_practice_history(
    db: Session,
    learner_id: int,
    limit: int = 20,
    offset: int = 0,
    practice_type: PracticeHistoryType = "all",
) -> PracticeHistoryResponse:
    items = get_practice_history_items(
        db=db,
        learner_id=learner_id,
        practice_type=practice_type,
    )

    return PracticeHistoryResponse(
        learner_id=learner_id,
        total=len(items),
        limit=limit,
        offset=offset,
        items=items[
            offset: offset + limit
        ],
    )


def get_practice_history_summary(
    db: Session,
    learner_id: int,
    practice_type: PracticeHistoryType = "all",
) -> PracticeHistorySummary:
    items = get_practice_history_items(
        db=db,
        learner_id=learner_id,
        practice_type=practice_type,
    )

    scores = [
        item.score
        for item in items
        if item.score is not None
    ]

    latest_score = next(
        (
            item.score
            for item in items
            if item.score is not None
        ),
        None,
    )

    return PracticeHistorySummary(
        learner_id=learner_id,
        total_practices=len(items),
        writing_practices=len(
            [
                item
                for item in items
                if item.source == "practice_attempt"
            ]
        ),
        speaking_practices=len(
            [
                item
                for item in items
                if item.practice_type == "speaking"
            ]
        ),
        evaluated_practices=len(scores),
        average_score=_average_score(scores),
        best_score=(
            max(scores)
            if scores
            else None
        ),
        latest_score=latest_score,
        latest_practice_at=(
            items[0].created_at
            if items
            else None
        ),
    )
