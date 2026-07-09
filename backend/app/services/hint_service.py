from sqlalchemy.orm import Session

from app.agents.hint_agent import generate_hint
from app.models.analysis import Analysis
from app.models.practice_attempt import PracticeAttempt


def get_hint(
    db: Session,
    attempt_id: int,
    error_index: int,
    hint_level: int,
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

    if error_index >= len(errors):
        return {
            "error": "Invalid error index"
        }

    selected_error = errors[error_index]

    return generate_hint(
        attempt_id=attempt.id,
        original_text=attempt.text,
        error_category=selected_error["category"],
        problem_text=selected_error["problem_text"],
        hint_level=hint_level,
    )