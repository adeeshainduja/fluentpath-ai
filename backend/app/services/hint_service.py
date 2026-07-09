from sqlalchemy.orm import Session

from app.agents.hint_agent import generate_hint
from app.models.analysis import Analysis
from app.models.practice_attempt import PracticeAttempt
from app.services.correction_state_service import (
    advance_hint_level,
    get_or_create_correction_state,
)


def get_next_hint(
    db: Session,
    attempt_id: int,
    error_index: int,
):

    attempt = (
        db.query(PracticeAttempt)
        .filter(
            PracticeAttempt.id == attempt_id
        )
        .first()
    )

    if attempt is None:
        return None

    analysis = (
        db.query(Analysis)
        .filter(
            Analysis.attempt_id == attempt_id
        )
        .first()
    )

    if analysis is None:
        return {
            "error": "Attempt must be analyzed first"
        }

    errors = analysis.result.get("errors", [])

    if error_index < 0 or error_index >= len(errors):
        return {
            "error": "Invalid error index"
        }

    state = get_or_create_correction_state(
        db=db,
        attempt_id=attempt_id,
        error_index=error_index,
    )

    if state.status == "resolved":
        return {
            "error": "This error has already been resolved"
        }

    if state.status == "needs_review":
        return {
            "error": "Maximum hint level reached"
        }

    # First hint request moves 0 → 1.
    # After failed evaluations, the evaluation flow
    # will already move the level forward.
    if state.current_hint_level == 0:
        state = advance_hint_level(
            db=db,
            state=state,
        )

    selected_error = errors[error_index]

    hint = generate_hint(
        attempt_id=attempt.id,
        original_text=attempt.text,
        error_category=selected_error["category"],
        problem_text=selected_error["problem_text"],
        hint_level=state.current_hint_level,
    )

    return {
        "correction_state_id": state.id,
        "status": state.status,
        "hint_level": state.current_hint_level,
        "hint_result": hint,
    }