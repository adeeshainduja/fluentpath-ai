from sqlalchemy.orm import Session

from app.services.analytics_service import (
    get_overall_score,
    get_skill_scores,
)

from app.services.adaptive_priority_service import (
    calculate_adaptive_priorities,
)

from app.services.streak_service import (
    calculate_learning_streak,
)

from app.services.recommendation_service import (
    get_next_recommended_task,
)


def generate_ai_coach_message(
    db: Session,
    learner_id: int,
) -> str:
    """
    Generate a personalized coaching message
    based on learner performance.
    """

    overall_score = get_overall_score(
        db=db,
        learner_id=learner_id,
    )

    skill_scores = get_skill_scores(
        db=db,
        learner_id=learner_id,
    )

    priorities = calculate_adaptive_priorities(
        db=db,
        learner_id=learner_id,
    )

    streak = calculate_learning_streak(
        db=db,
        learner_id=learner_id,
    )

    recommendation = get_next_recommended_task(
        db=db,
        learner_id=learner_id,
    )

    message = []

    # ------------------------------------------
    # Overall performance
    # ------------------------------------------

    if overall_score >= 85:
        message.append(
            "Excellent work! Your overall performance is outstanding."
        )

    elif overall_score >= 70:
        message.append(
            "Great progress! Keep practicing consistently."
        )

    else:
        message.append(
            "You're making progress. Consistent practice will help you improve."
        )

    # ------------------------------------------
    # Weakest skill
    # ------------------------------------------

    if priorities:

        weakest = priorities[0]["skill"]

        message.append(
            f"Your current focus should be {weakest}."
        )

    # ------------------------------------------
    # Practice streak
    # ------------------------------------------

    if streak > 0:

        message.append(
            f"You currently have a {streak}-day learning streak."
        )

    # ------------------------------------------
    # Recommendation
    # ------------------------------------------

    if recommendation:

        message.append(
            f"Recommended lesson: {recommendation.title}."
        )

    # ------------------------------------------
    # Best skill
    # ------------------------------------------

    best_skill = max(
        skill_scores,
        key=skill_scores.get,
    )

    message.append(
        f"Your strongest skill is {best_skill.title()}."
    )

    return " ".join(message)