from sqlalchemy.orm import Session

from app.agents.retry_evaluation_agent import evaluate_retry
from app.models.analysis import Analysis
from app.models.practice_attempt import PracticeAttempt


def evaluate_retry_attempt(
    db: Session,
    original_attempt_id: int,
    retry_attempt_id: int,
    error_index: int,
):

    original_attempt = (
        db.query(PracticeAttempt)
        .filter(
            PracticeAttempt.id == original_attempt_id
        )
        .first()
    )

    retry_attempt = (
        db.query(PracticeAttempt)
        .filter(
            PracticeAttempt.id == retry_attempt_id
        )
        .first()
    )

    if original_attempt is None or retry_attempt is None:
        return None

    original_analysis = (
        db.query(Analysis)
        .filter(
            Analysis.attempt_id == original_attempt_id
        )
        .first()
    )

    if original_analysis is None:
        return {
            "error": "Original attempt must be analyzed first"
        }

    errors = original_analysis.result.get("errors", [])

    if error_index < 0 or error_index >= len(errors):
        return {
            "error": "Invalid error index"
        }

    target_error = errors[error_index]

    evaluation = evaluate_retry(
        original_text=original_attempt.text,
        retry_text=retry_attempt.text,
        target_category=target_error["category"],
    )

    return {
        "original_attempt_id": original_attempt_id,
        "retry_attempt_id": retry_attempt_id,
        "evaluation": evaluation,
    }