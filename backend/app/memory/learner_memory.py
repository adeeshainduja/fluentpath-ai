from datetime import datetime

from sqlalchemy.orm import Session

from app.models.error_pattern import ErrorPattern
from app.schemas.practice import WritingAnalysisResult


def update_error_memory(
    db: Session,
    learner_id: int,
    analysis: WritingAnalysisResult,
):

    updated_patterns = []

    for error in analysis.errors:

        pattern = (
            db.query(ErrorPattern)
            .filter(
                ErrorPattern.learner_id == learner_id,
                ErrorPattern.category == error.category,
            )
            .first()
        )

        if pattern:
            pattern.occurrence_count += 1
            pattern.last_seen_at = datetime.utcnow()

        else:
            pattern = ErrorPattern(
                learner_id=learner_id,
                category=error.category,
                error_type=error.error_type,
                occurrence_count=1,
                resolved_count=0,
                status="active",
            )

            db.add(pattern)

        updated_patterns.append(pattern)

    db.commit()

    for pattern in updated_patterns:
        db.refresh(pattern)

    return updated_patterns

def get_learner_weaknesses(
    db: Session,
    learner_id: int,
):

    return (
        db.query(ErrorPattern)
        .filter(
            ErrorPattern.learner_id == learner_id
        )
        .order_by(
            ErrorPattern.occurrence_count.desc()
        )
        .all()
    )