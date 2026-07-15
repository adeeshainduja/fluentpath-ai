from sqlalchemy.orm import Session

from app.services.progress_metric_service import (
    update_progress_metrics,
)

from app.services.error_memory_service import (
    update_error_memory,
)

from app.services.adaptive_priority_service import (
    calculate_adaptive_priorities,
)


def update_learner_profile(
    db: Session,
    learner_id: int,
    attempt_id: int,
):
    """
    Update all learner analytics after
    completing a practice attempt.
    """

    update_progress_metrics(
        db=db,
        learner_id=learner_id,
        attempt_id=attempt_id,
    )

    update_error_memory(
        db=db,
        learner_id=learner_id,
        attempt_id=attempt_id,
    )

    calculate_adaptive_priorities(
        db=db,
        learner_id=learner_id,
    )
    