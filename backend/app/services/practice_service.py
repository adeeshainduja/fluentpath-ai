from sqlalchemy.orm import Session

from app.models.practice_attempt import PracticeAttempt
from app.schemas.practice import PracticeAttemptCreate


def create_writing_attempt(
    db: Session,
    attempt: PracticeAttemptCreate,
) -> PracticeAttempt:

    new_attempt = PracticeAttempt(
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