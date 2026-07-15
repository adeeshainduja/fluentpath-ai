from datetime import timedelta

from sqlalchemy.orm import Session

from app.models.practice_attempt import (
    PracticeAttempt,
)


def calculate_learning_streak(
    db: Session,
    learner_id: int,
) -> int:
    """
    Calculate the learner's current
    consecutive learning streak.
    """

    attempts = (
        db.query(PracticeAttempt)
        .filter(
            PracticeAttempt.learner_id == learner_id
        )
        .order_by(
            PracticeAttempt.created_at.desc()
        )
        .all()
    )

    if not attempts:
        return 0

    practice_days = []

    for attempt in attempts:

        day = attempt.created_at.date()

        if day not in practice_days:
            practice_days.append(day)

    streak = 1

    current_day = practice_days[0]

    for next_day in practice_days[1:]:

        if current_day - next_day == timedelta(days=1):

            streak += 1
            current_day = next_day

        else:
            break

    return streak