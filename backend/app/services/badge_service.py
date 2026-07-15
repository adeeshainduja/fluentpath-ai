from sqlalchemy.orm import Session

from app.schemas.learning_path import Badge

from app.services.analytics_service import (
    get_skill_scores,
)

from app.services.streak_service import (
    calculate_learning_streak,
)

from app.models.practice_attempt import (
    PracticeAttempt,
)


def calculate_badges(
    db: Session,
    learner_id: int,
):
    """
    Calculate learner achievement badges.
    """

    badges = []

    skill_scores = get_skill_scores(
        db=db,
        learner_id=learner_id,
    )

    streak = calculate_learning_streak(
        db=db,
        learner_id=learner_id,
    )

    total_attempts = (
        db.query(PracticeAttempt)
        .filter(
            PracticeAttempt.learner_id == learner_id
        )
        .count()
    )

    # ----------------------------------------
    # Getting Started
    # ----------------------------------------

    badges.append(
        Badge(
            id=1,
            title="Getting Started",
            description="Complete your first practice.",
            earned=total_attempts >= 1,
        )
    )

    # ----------------------------------------
    # Grammar Master
    # ----------------------------------------

    badges.append(
        Badge(
            id=2,
            title="Grammar Master",
            description="Reach 90% Grammar score.",
            earned=skill_scores["grammar"] >= 90,
        )
    )

    # ----------------------------------------
    # Vocabulary Explorer
    # ----------------------------------------

    badges.append(
        Badge(
            id=3,
            title="Vocabulary Explorer",
            description="Reach 90% Vocabulary score.",
            earned=skill_scores["vocabulary"] >= 90,
        )
    )

    # ----------------------------------------
    # Fluency Expert
    # ----------------------------------------

    badges.append(
        Badge(
            id=4,
            title="Fluency Expert",
            description="Reach 90% Fluency score.",
            earned=skill_scores["fluency"] >= 90,
        )
    )

    # ----------------------------------------
    # Pronunciation Pro
    # ----------------------------------------

    badges.append(
        Badge(
            id=5,
            title="Pronunciation Pro",
            description="Reach 90% Pronunciation score.",
            earned=skill_scores["pronunciation"] >= 90,
        )
    )

    # ----------------------------------------
    # 7 Day Streak
    # ----------------------------------------

    badges.append(
        Badge(
            id=6,
            title="7 Day Streak",
            description="Practice for 7 consecutive days.",
            earned=streak >= 7,
        )
    )

    # ----------------------------------------
    # Consistent Learner
    # ----------------------------------------

    badges.append(
        Badge(
            id=7,
            title="Consistent Learner",
            description="Complete 50 practice sessions.",
            earned=total_attempts >= 50,
        )
    )

    return badges