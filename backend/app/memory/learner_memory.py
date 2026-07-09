from collections import Counter
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

    # Count how many errors belong to each category
    category_counts = Counter(
        error.category for error in analysis.errors
    )

    # Keep one representative error for each category
    category_errors = {}

    for error in analysis.errors:
        if error.category not in category_errors:
            category_errors[error.category] = error

    for category, count in category_counts.items():

        representative_error = category_errors[category]

        pattern = (
            db.query(ErrorPattern)
            .filter(
                ErrorPattern.learner_id == learner_id,
                ErrorPattern.category == category,
            )
            .first()
        )

        if pattern:
            pattern.occurrence_count += count
            pattern.last_seen_at = datetime.utcnow()

        else:
            pattern = ErrorPattern(
                learner_id=learner_id,
                category=category,
                error_type=representative_error.error_type,
                occurrence_count=count,
                resolved_count=0,
                status="active",
                last_seen_at=datetime.utcnow(),
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