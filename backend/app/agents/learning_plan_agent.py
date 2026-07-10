from app.models.error_pattern import ErrorPattern
from app.schemas.learning_plan import (
    LearningPlanResult,
    LearningRecommendation,
)


STATUS_WEIGHTS = {
    "active": 3.0,
    "improving": 1.5,
    "mastered": 0.2,
}


def calculate_priority_score(
    weakness: ErrorPattern,
) -> float:

    occurrence_count = weakness.occurrence_count
    resolved_count = weakness.resolved_count

    unresolved_count = max(
        occurrence_count - resolved_count,
        0,
    )

    if occurrence_count > 0:
        resolution_rate = (
            resolved_count / occurrence_count
        )
    else:
        resolution_rate = 0.0

    status_weight = STATUS_WEIGHTS.get(
        weakness.status,
        1.0,
    )

    score = (
        occurrence_count * 1.0
        + unresolved_count * 2.0
        + status_weight
        - resolution_rate * 5.0
    )

    return round(max(score, 0.0), 2)


def choose_difficulty(
    weakness: ErrorPattern,
) -> str:

    if weakness.status == "mastered":
        return "advanced"

    if weakness.status == "improving":
        return "intermediate"

    return "beginner"


def choose_practice_type(
    weakness: ErrorPattern,
) -> str:

    speaking_categories = {
        "fluency",
        "pronunciation",
        "speaking_pace",
        "hesitation",
    }

    if weakness.category in speaking_categories:
        return "speaking"

    return "writing"


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

    scored_weaknesses = [
        (
            weakness,
            calculate_priority_score(weakness),
        )
        for weakness in weaknesses
    ]

    highest_priority, priority_score = max(
        scored_weaknesses,
        key=lambda item: item[1],
    )

    recommendation = build_recommendation(
        weakness=highest_priority,
        priority_score=priority_score,
    )

    return LearningPlanResult(
        learner_id=learner_id,
        has_recommendation=True,
        recommendation=recommendation,
    )


def build_recommendation(
    weakness: ErrorPattern,
    priority_score: float,
) -> LearningRecommendation:

    difficulty = choose_difficulty(weakness)
    practice_type = choose_practice_type(weakness)

    if weakness.occurrence_count > 0:
        resolution_rate = (
            weakness.resolved_count
            / weakness.occurrence_count
        )
    else:
        resolution_rate = 0.0

    resolution_percentage = round(
        resolution_rate * 100
    )

    if weakness.category == "past_tense":
        return LearningRecommendation(
            priority_category="past_tense",
            priority_score=priority_score,
            practice_type=practice_type,
            difficulty=difficulty,
            title="Past Tense Story Practice",
            instruction=(
                "Write a short paragraph about something "
                "you did yesterday. Focus on describing "
                "completed actions clearly."
            ),
            reason=(
                f"This pattern has appeared "
                f"{weakness.occurrence_count} times, and "
                f"your current resolution rate is "
                f"{resolution_percentage}%."
            ),
        )

    return LearningRecommendation(
        priority_category=weakness.category,
        priority_score=priority_score,
        practice_type=practice_type,
        difficulty=difficulty,
        title=(
            f"{weakness.category.replace('_', ' ').title()} "
            f"Practice"
        ),
        instruction=(
            "Complete a focused practice activity for "
            f"{weakness.category.replace('_', ' ')}."
        ),
        reason=(
            f"This pattern has appeared "
            f"{weakness.occurrence_count} times, with a "
            f"{resolution_percentage}% resolution rate."
        ),
    )