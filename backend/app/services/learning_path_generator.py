from sqlalchemy.orm import Session

from app.schemas.learning_path import (
    Badge,
    CurrentStage,
    LearningPathResponse,
    RoadmapItem,
)

from app.services.analytics_service import (
    get_skill_progress,
)

from app.services.adaptive_priority_service import (
    calculate_adaptive_priorities,
)


def generate_learning_path(
    db: Session,
    learner_id: int,
) -> LearningPathResponse:
    """
    Generate a personalized learning path for a learner.

    This service combines:
        - Progress Metrics
        - Adaptive Priorities
        - Practice Recommendations
        - AI Coach
        - Learning Roadmap
    """

    # -----------------------------------------
    # 1. Learner Analytics
    # -----------------------------------------

    skill_progress = get_skill_progress(
        db=db,
        learner_id=learner_id,
    )

    # -----------------------------------------
    # 2. Adaptive Priorities
    # -----------------------------------------

    priorities = calculate_adaptive_priorities(
        db=db,
        learner_id=learner_id,
    )

    # -----------------------------------------
    # 3. Overall Progress
    # -----------------------------------------

    if skill_progress:
        overall_progress = int(
            sum(item.average_score for item in skill_progress)
            / len(skill_progress)
        )
    else:
        overall_progress = 0

    # -----------------------------------------
    # 4. Current Lesson
    # -----------------------------------------

    if priorities:

        highest = priorities[0]

        current_stage = CurrentStage(
            id=highest.id,
            title=f"{highest.category.title()} Practice",
            skill=highest.category.title(),
            difficulty="Intermediate",
            estimated_minutes=20,
        )

    else:

        current_stage = CurrentStage(
            id=1,
            title="Grammar Practice",
            skill="Grammar",
            difficulty="Beginner",
            estimated_minutes=15,
        )

    # -----------------------------------------
    # 5. Roadmap
    # -----------------------------------------

    roadmap = []

    for index, priority in enumerate(priorities):

        roadmap.append(
            RoadmapItem(
                id=index + 1,
                title=f"{priority.category.title()} Practice",
                skill=priority.category.title(),
                difficulty="Intermediate",
                estimated_minutes=20,
                status=(
                    "current"
                    if index == 0
                    else "locked"
                ),
            )
        )

    if not roadmap:

        roadmap.append(
            RoadmapItem(
                id=1,
                title="Grammar Basics",
                skill="Grammar",
                difficulty="Beginner",
                estimated_minutes=15,
                status="current",
            )
        )

    # -----------------------------------------
    # 6. Badges
    # -----------------------------------------

    badges = [
        Badge(
            id=1,
            title="Getting Started",
            description="Completed your first lesson.",
            earned=True,
        ),
        Badge(
            id=2,
            title="Consistent Learner",
            description="Practice for 7 consecutive days.",
            earned=False,
        ),
    ]

    # -----------------------------------------
    # 7. AI Coach
    # -----------------------------------------

    if priorities:

        coach_message = (
            f"Your weakest skill is "
            f"{priorities[0].category.title()}. "
            f"Complete today's lesson to improve "
            f"your overall communication skills."
        )

    else:

        coach_message = (
            "Welcome to FluentPath AI! "
            "Let's begin your learning journey."
        )

    # -----------------------------------------
    # 8. Return Response
    # -----------------------------------------

    return LearningPathResponse(
        overall_progress=overall_progress,
        streak=5,
        coach_message=coach_message,
        current_stage=current_stage,
        roadmap=roadmap,
        badges=badges,
    )