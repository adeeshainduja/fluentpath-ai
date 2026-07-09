from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.models.correction_state import CorrectionState


def get_or_create_correction_state(
    db: Session,
    attempt_id: int,
    error_index: int,
):

    state = (
        db.query(CorrectionState)
        .filter(
            CorrectionState.attempt_id == attempt_id,
            CorrectionState.error_index == error_index,
        )
        .first()
    )

    if state:
        return state

    analysis = (
        db.query(Analysis)
        .filter(
            Analysis.attempt_id == attempt_id
        )
        .first()
    )

    if analysis is None:
        return None

    errors = analysis.result.get("errors", [])

    if error_index < 0 or error_index >= len(errors):
        return None

    target_error = errors[error_index]

    state = CorrectionState(
        attempt_id=attempt_id,
        error_index=error_index,
        target_category=target_error["category"],
        current_hint_level=0,
        retry_count=0,
        status="active",
    )

    db.add(state)
    db.commit()
    db.refresh(state)

    return state

def advance_hint_level(
    db: Session,
    state: CorrectionState,
):

    if state.current_hint_level < 3:
        state.current_hint_level += 1

    db.commit()
    db.refresh(state)

    return state

def record_retry_result(
    db: Session,
    state: CorrectionState,
    resolved: bool,
):

    state.retry_count += 1

    if resolved:
        state.status = "resolved"

    elif state.current_hint_level < 3:
        state.current_hint_level += 1

    else:
        state.status = "needs_review"

    db.commit()
    db.refresh(state)

    return state