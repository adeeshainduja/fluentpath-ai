from sqlalchemy.orm import Session

from app.models.practice_task import PracticeTask
from app.services.adaptive_priority_service import (
    calculate_adaptive_priorities,
)
from app.services.analytics_service import (
    get_skill_progress,
)


def determine_practice_strategy(
    db: Session,
    learner_id: int,
):
    priorities = calculate_adaptive_priorities(
        db=db,
        learner_id=learner_id,
    )

    if not priorities:
        return {
            "error": "Not enough learner data"
        }

    skill_progress = get_skill_progress(
        db=db,
        learner_id=learner_id,
    )

    progress_by_skill = {
        item["skill"]: item
        for item in skill_progress
    }

    top_priority = priorities[0]
    target_skill = top_priority["skill"]

    skill_data = progress_by_skill.get(
        target_skill,
        {},
    )

    latest_score = skill_data.get(
        "latest_score"
    )

    trend = skill_data.get(
        "trend",
        "unknown",
    )

    recent_tasks = (
        db.query(PracticeTask)
        .filter(
            PracticeTask.learner_id == learner_id
        )
        .order_by(
            PracticeTask.created_at.desc()
        )
        .limit(3)
        .all()
    )

    recent_target_count = sum(
        1
        for task in recent_tasks
        if task.target_skill == target_skill
    )

    strategy = "reinforce"
    reason = (
        "The highest-priority skill still needs practice."
    )

    selected_skill = target_skill

    if (
        latest_score is not None
        and latest_score >= 85
        and trend == "improving"
    ):
        strategy = "increase_difficulty"
        reason = (
            "The learner is performing strongly and "
            "improving in this skill."
        )

    elif recent_target_count >= 2 and len(priorities) > 1:
        strategy = "rotate_skill"
        selected_skill = priorities[1]["skill"]
        reason = (
            "The learner recently practiced the same "
            "skill multiple times, so another priority "
            "skill is selected temporarily."
        )

    elif (
        latest_score is not None
        and latest_score < 50
    ):
        strategy = "guided_reinforcement"
        reason = (
            "The latest performance is low, so the learner "
            "needs simpler focused practice."
        )

    elif trend == "declining":
        strategy = "review"
        reason = (
            "Performance is declining, so review practice "
            "is recommended before increasing difficulty."
        )

    return {
        "selected_skill": selected_skill,
        "strategy": strategy,
        "reason": reason,
        "latest_score": latest_score,
        "trend": trend,
        "recent_target_count": recent_target_count,
    }