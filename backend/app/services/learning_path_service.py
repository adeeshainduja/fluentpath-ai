from sqlalchemy.orm import Session

from app.schemas.learning_path import (
    Badge,
    CurrentStage,
    LearningPathResponse,
    RoadmapItem,
)

from app.services.analytics_service import (
    get_overall_score,
)

from app.services.adaptive_priority_service import (
    calculate_adaptive_priorities,
)
from app.services.streak_service import (
    calculate_learning_streak,
)


def get_learning_path(
    db: Session,
    learner_id: int,
) -> LearningPathResponse:
    """
    Generate a personalized learning path
    based on learner analytics.
    """

    # -----------------------------------------
    # Overall Progress
    # -----------------------------------------

    overall_progress = get_overall_score(
        db=db,
        learner_id=learner_id,
    )

    # -----------------------------------------
    # Adaptive Priorities
    # -----------------------------------------

    priorities = calculate_adaptive_priorities(
        db=db,
        learner_id=learner_id,
    )

    # -----------------------------------------
    # Current Lesson
    # -----------------------------------------

    if priorities:

        highest = priorities[0]

        current_stage = CurrentStage(
            id=1,
            title=f"{highest['skill']} Practice",
            skill=highest["skill"],
            difficulty="Intermediate",
            estimated_minutes=20,
        )

    else:

        current_stage = CurrentStage(
            id=1,
            title="Grammar Practice",
            skill="Grammar",
            difficulty="Beginner",
            estimated_minutes=20,
        )

    # -----------------------------------------
    # Learning Roadmap
    # -----------------------------------------

    roadmap = []

    if priorities:

        for index, priority in enumerate(priorities):

            roadmap.append(
                RoadmapItem(
                    id=index + 1,
                    title=f"{priority['skill']} Practice",
                    skill=priority["skill"],
                    difficulty="Intermediate",
                    estimated_minutes=20,
                    status=(
                        "current"
                        if index == 0
                        else "locked"
                    ),
                )
            )

    else:

        roadmap = [
            RoadmapItem(
                id=1,
                title="Grammar Basics",
                skill="Grammar",
                difficulty="Beginner",
                estimated_minutes=15,
                status="current",
            )
        ]

    # -----------------------------------------
    # AI Coach Message
    # -----------------------------------------

    if priorities:

        coach_message = (
            f"Your weakest skill is "
            f"{priorities[0]['skill']}. "
            f"Practice this skill first to improve "
            f"your overall communication score."
        )

    else:

        coach_message = (
            "Welcome to FluentPath AI! "
            "Let's begin your English learning journey."
        )

    # -----------------------------------------
    # Temporary Badges
    # -----------------------------------------

    badges = [
        Badge(
            id=1,
            title="Getting Started",
            description="Complete your first practice.",
            earned=True,
        ),
        Badge(
            id=2,
            title="Grammar Master",
            description="Reach 90% Grammar score.",
            earned=False,
        ),
        Badge(
            id=3,
            title="Vocabulary Explorer",
            description="Complete 20 vocabulary tasks.",
            earned=False,
        ),
        Badge(
            id=4,
            title="7 Day Streak",
            description="Practice for 7 consecutive days.",
            earned=False,
        ),
    ]

    # -----------------------------------------
    # Response
    # -----------------------------------------

    return LearningPathResponse(
        overall_progress=overall_progress,
        streak = calculate_learning_streak(
        db=db,
        learner_id=learner_id,
    )
        coach_message=coach_message,
        current_stage=current_stage,
        roadmap=roadmap,
        badges=badges,
    )