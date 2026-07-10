from sqlalchemy.orm import Session

from app.agents.retry_evaluation_agent import evaluate_retry
from app.models.analysis import Analysis
from app.models.practice_attempt import PracticeAttempt
from app.services.correction_state_service import (
    get_or_create_correction_state,
    record_retry_result,
)


def evaluate_retry_attempt(
    db: Session,
    original_attempt_id: int,
    retry_attempt_id: int,
    error_index: int,
):
    # 1. Get original attempt
    original_attempt = (
        db.query(PracticeAttempt)
        .filter(
            PracticeAttempt.id == original_attempt_id
        )
        .first()
    )

    # 2. Get retry attempt
    retry_attempt = (
        db.query(PracticeAttempt)
        .filter(
            PracticeAttempt.id == retry_attempt_id
        )
        .first()
    )

    # 3. Check attempts exist
    if original_attempt is None or retry_attempt is None:
        return None

    # 4. Get saved analysis of original attempt
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

    # 5. Get detected errors
    errors = original_analysis.result.get(
        "errors",
        [],
    )

    # 6. Validate error index
    if error_index < 0 or error_index >= len(errors):
        return {
            "error": "Invalid error index"
        }

    # 7. Select target error
    target_error = errors[error_index]

    # 8. Evaluate the learner's retry
    evaluation = evaluate_retry(
        original_text=original_attempt.text,
        retry_text=retry_attempt.text,
        target_category=target_error["category"],
    )

    # 9. Get or create correction state
    state = get_or_create_correction_state(
        db=db,
        attempt_id=original_attempt_id,
        error_index=error_index,
    )

    if state is None:
        return {
            "error": "Could not create correction state"
        }

    # 10. Update state using evaluation result
    updated_state = record_retry_result(
        db=db,
        state=state,
        resolved=evaluation.resolved,
    )

    # 11. Return evaluation and updated state
    return {
        "original_attempt_id": original_attempt_id,
        "retry_attempt_id": retry_attempt_id,
        "evaluation": evaluation,
        "correction_state": {
            "status": updated_state.status,
            "current_hint_level": (
                updated_state.current_hint_level
            ),
            "retry_count": updated_state.retry_count,
        },
    }