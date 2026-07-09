from app.models.error_pattern import ErrorPattern
from app.schemas.learning_plan import (
    LearningPlanResult,
    LearningRecommendation,
)


def create_learning_plan(
    learner_id: int,
    weaknesses: list[ErrorPattern],
) -> LearningPlanResult:

    if not weaknesses:
        return LearningPlanResult(
            learner_id=learner_id,
            has_recommendation=False,
            recommendation=None,
        )

    highest_priority = max(
        weaknesses,
        key=lambda weakness: weakness.occurrence_count,
    )

    recommendation = build_recommendation(
        highest_priority
    )

    return LearningPlanResult(
        learner_id=learner_id,
        has_recommendation=True,
        recommendation=recommendation,
    )


def build_recommendation(
    weakness: ErrorPattern,
) -> LearningRecommendation:

    if weakness.category == "past_tense":

        return LearningRecommendation(
            priority_category="past_tense",
            practice_type="writing",
            difficulty="beginner",
            title="Past Tense Story Practice",
            instruction=(
                "Write 5 sentences about what you did yesterday."
            ),
            reason=(
                f"Past-tense errors have appeared "
                f"{weakness.occurrence_count} times."
            ),
        )

    return LearningRecommendation(
        priority_category=weakness.category,
        practice_type="writing",
        difficulty="beginner",
        title="Targeted English Practice",
        instruction=(
            f"Complete a short practice activity focused on "
            f"{weakness.category.replace('_', ' ')}."
        ),
        reason=(
            f"This error pattern has appeared "
            f"{weakness.occurrence_count} times."
        ),
    )