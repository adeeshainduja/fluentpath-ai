from sqlalchemy.orm import Session

from app.models.practice_attempt import PracticeAttempt
from app.schemas.practice import PracticeAttemptCreate
from app.agents.writing_analysis_agent import analyze_writing


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