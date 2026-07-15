from sqlalchemy.orm import Session

from app.schemas.learning_path import (
    LearningPathResponse,
    CurrentStage,
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

from app.services.badge_service import (
    calculate_badges,
)

from app.services.recommendation_service import (
    get_next_recommended_task,
)

from app.services.roadmap_service import (
    generate_learning_roadmap,
)

from app.services.ai_coach_service import (
    generate_ai_coach_message,
)


def get_learning_path(
    db: Session,
    learner_id: int,
) -> LearningPathResponse:
    """
    Generate a personalized learning path
    for the learner.
    """

    # -------------------------------------------------
    # Overall Progress
    # -------------------------------------------------

    overall_progress = get_overall_score(
        db=db,
        learner_id=learner_id,
    )

    # -------------------------------------------------
    # Current Learning Streak
    # -------------------------------------------------

    streak = calculate_learning_streak(
        db=db,
        learner_id=learner_id,
    )

    # -------------------------------------------------
    # Adaptive Priorities
    # -------------------------------------------------

    priorities = calculate_adaptive_priorities(
        db=db,
        learner_id=learner_id,
    )

    # -------------------------------------------------
    # Recommended Lesson
    # -------------------------------------------------

    recommended_task = get_next_recommended_task(
        db=db,
        learner_id=learner_id,
    )

    # -------------------------------------------------
    # Current Stage
    # -------------------------------------------------

    if recommended_task:

        current_stage = CurrentStage(
            id=recommended_task.id,
            title=recommended_task.title,
            skill=recommended_task.target_skill,
            difficulty=recommended_task.difficulty,
            estimated_minutes=20,
        )

    elif priorities:

        current_stage = CurrentStage(
            id=1,
            title=f"{priorities[0]['skill']} Practice",
            skill=priorities[0]["skill"],
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

    # -------------------------------------------------
    # Personalized Roadmap
    # -------------------------------------------------

    roadmap = generate_learning_roadmap(
        db=db,
        learner_id=learner_id,
    )

    # -------------------------------------------------
    # Achievement Badges
    # -------------------------------------------------

    badges = calculate_badges(
        db=db,
        learner_id=learner_id,
    )

    # -------------------------------------------------
    # AI Coach Message
    # -------------------------------------------------

    coach_message = generate_ai_coach_message(
        db=db,
        learner_id=learner_id,
    )

    # -------------------------------------------------
    # Response
    # -------------------------------------------------

    return LearningPathResponse(
        overall_progress=overall_progress,
        streak=streak,
        coach_message=coach_message,
        current_stage=current_stage,
        roadmap=roadmap,
        badges=badges,
    )