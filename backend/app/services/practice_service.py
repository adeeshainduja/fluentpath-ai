from sqlalchemy.orm import Session

from app.models.practice_attempt import PracticeAttempt
from app.agents.writing_analysis_agent import analyze_writing
from app.schemas.practice import (
    PracticeAttemptCreate,
    RetryAttemptCreate,
)
from app.memory.learner_memory import update_error_memory
from app.models.analysis import Analysis
from app.schemas.practice import WritingAnalysisResult


def create_writing_attempt(
    db: Session,
    attempt: PracticeAttemptCreate,
) -> PracticeAttempt:

    new_attempt = PracticeAttempt(
        learner_id=attempt.learner_id,
        text=attempt.text,
        practice_type="writing",
    )

    db.add(new_attempt)
    db.commit()
    db.refresh(new_attempt)

    return new_attempt


def get_all_attempts(
    db: Session,
) -> list[PracticeAttempt]:

    return (
        db.query(PracticeAttempt)
        .order_by(PracticeAttempt.created_at.desc())
        .all()
    )


def get_attempt_by_id(
    db: Session,
    attempt_id: int,
) -> PracticeAttempt | None:

    return (
        db.query(PracticeAttempt)
        .filter(PracticeAttempt.id == attempt_id)
        .first()
    )

def analyze_attempt(
    db: Session,
    attempt_id: int,
):

    attempt = get_attempt_by_id(
        db=db,
        attempt_id=attempt_id,
    )

    if attempt is None:
        return None

    analysis = analyze_writing(attempt.text)

    return {
        "attempt_id": attempt.id,
        "original_text": attempt.text,
        "analysis": analysis,
    }

def create_retry_attempt(
    db: Session,
    original_attempt_id: int,
    retry_data: RetryAttemptCreate,
):

    original_attempt = get_attempt_by_id(
        db=db,
        attempt_id=original_attempt_id,
    )

    if original_attempt is None:
        return None

    retry_attempt = PracticeAttempt(
        learner_id=original_attempt.learner_id,
        task_id=original_attempt.task_id,
        text=retry_data.text,
        practice_type=original_attempt.practice_type,
        parent_attempt_id=original_attempt.id,
        attempt_number=original_attempt.attempt_number + 1,
    )

    db.add(retry_attempt)
    db.commit()
    db.refresh(retry_attempt)

    original_analysis = analyze_writing(
        original_attempt.text
    )

    retry_analysis = analyze_writing(
        retry_attempt.text
    )

    original_error_count = len(
        original_analysis.errors
    )

    retry_error_count = len(
        retry_analysis.errors
    )

    improved = (
        retry_error_count < original_error_count
    )

    return {
        "original_attempt": {
            "id": original_attempt.id,
            "text": original_attempt.text,
            "error_count": original_error_count,
        },
        "retry_attempt": {
            "id": retry_attempt.id,
            "text": retry_attempt.text,
            "attempt_number": retry_attempt.attempt_number,
            "error_count": retry_error_count,
        },
        "improved": improved,
        "analysis": retry_analysis,
    }

def analyze_attempt(
    db: Session,
    attempt_id: int,
):

    attempt = get_attempt_by_id(
        db=db,
        attempt_id=attempt_id,
    )

    if attempt is None:
        return None

    analysis = analyze_writing(attempt.text)

    memory_updates = update_error_memory(
        db=db,
        learner_id=1,
        analysis=analysis,
    )

    return {
        "attempt_id": attempt.id,
        "original_text": attempt.text,
        "analysis": analysis,
        "memory_updated": len(memory_updates) > 0,
    }

def analyze_attempt(
    db: Session,
    attempt_id: int,
):

    attempt = get_attempt_by_id(
        db=db,
        attempt_id=attempt_id,
    )

    if attempt is None:
        return None

    existing_analysis = (
        db.query(Analysis)
        .filter(Analysis.attempt_id == attempt_id)
        .first()
    )

    if existing_analysis:

        analysis = WritingAnalysisResult(
            **existing_analysis.result
        )

        return {
            "attempt_id": attempt.id,
            "original_text": attempt.text,
            "analysis": analysis,
            "memory_updated": False,
            "source": "stored_analysis",
        }

    analysis = analyze_writing(attempt.text)

    saved_analysis = Analysis(
        attempt_id=attempt.id,
        result=analysis.model_dump(),
    )

    db.add(saved_analysis)

    memory_updates = update_error_memory(
        db=db,
        learner_id=1,
        analysis=analysis,
    )

    db.commit()

    return {
        "attempt_id": attempt.id,
        "original_text": attempt.text,
        "analysis": analysis,
        "memory_updated": len(memory_updates) > 0,
        "source": "new_analysis",
    }
