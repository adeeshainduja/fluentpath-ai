from app.schemas.learning_path import (
    Badge,
    CurrentStage,
    LearningPathResponse,
    RoadmapItem,
)


def get_learning_path(learner_id: int) -> LearningPathResponse:
    """
    Returns the personalized learning path for a learner.
    Currently returns mock data.
    """

    roadmap = [
        RoadmapItem(
            id=1,
            title="Grammar Basics",
            skill="Grammar",
            difficulty="Beginner",
            estimated_minutes=15,
            status="completed",
        ),
        RoadmapItem(
            id=2,
            title="Vocabulary Builder",
            skill="Vocabulary",
            difficulty="Beginner",
            estimated_minutes=20,
            status="completed",
        ),
        RoadmapItem(
            id=3,
            title="Sentence Construction",
            skill="Grammar",
            difficulty="Intermediate",
            estimated_minutes=20,
            status="completed",
        ),
        RoadmapItem(
            id=4,
            title="Business Email Writing",
            skill="Writing",
            difficulty="Intermediate",
            estimated_minutes=25,
            status="current",
        ),
        RoadmapItem(
            id=5,
            title="Listening Skills",
            skill="Listening",
            difficulty="Intermediate",
            estimated_minutes=20,
            status="locked",
        ),
        RoadmapItem(
            id=6,
            title="Speaking Confidence",
            skill="Speaking",
            difficulty="Advanced",
            estimated_minutes=30,
            status="locked",
        ),
        RoadmapItem(
            id=7,
            title="Mock Interview",
            skill="Interview",
            difficulty="Advanced",
            estimated_minutes=40,
            status="locked",
        ),
    ]

    badges = [
        Badge(
            id=1,
            title="Grammar Master",
            description="Completed Grammar Module",
            earned=True,
        ),
        Badge(
            id=2,
            title="Vocabulary Explorer",
            description="Learned 100 new words",
            earned=True,
        ),
        Badge(
            id=3,
            title="7 Day Streak",
            description="Practiced for 7 consecutive days",
            earned=True,
        ),
        Badge(
            id=4,
            title="Interview Ready",
            description="Complete all interview lessons",
            earned=False,
        ),
    ]

    current_stage = CurrentStage(
        id=4,
        title="Business Email Writing",
        skill="Writing",
        difficulty="Intermediate",
        estimated_minutes=25,
    )

    return LearningPathResponse(
        overall_progress=72,
        streak=5,
        coach_message=(
            "Great progress! Your grammar has improved by 12%. "
            "Vocabulary is now your weakest skill. "
            "Continue with Business Email Writing."
        ),
        current_stage=current_stage,
        roadmap=roadmap,
        badges=badges,
    )