from sqlalchemy.orm import Session

from app.agents.learning_plan_agent import (
    create_learning_plan,
)
from app.agents.adaptive_task_agent import (
    generate_adaptive_task,
)

from app.memory.learner_memory import (
    get_learner_weaknesses,
)

from app.models.practice_task import PracticeTask
from app.models.practice_attempt import PracticeAttempt

from app.services.adaptive_priority_service import (
    calculate_adaptive_priorities,
)
from app.services.practice_strategy_service import (
    determine_practice_strategy,
)


# ============================================================
# 1. GENERATE NORMAL PRACTICE TASK
# ============================================================

def generate_and_save_task(
    db: Session,
    learner_id: int,
):
    weaknesses = get_learner_weaknesses(
        db=db,
        learner_id=learner_id,
    )

    plan = create_learning_plan(
        learner_id=learner_id,
        weaknesses=weaknesses,
    )

    if not plan.has_recommendation:
        return {
            "error": (
                "No weaknesses available "
                "for task generation"
            )
        }

    recommendation = plan.recommendation

    task = PracticeTask(
        learner_id=learner_id,
        target_skill=(
            recommendation.priority_category
        ),
        practice_type=(
            recommendation.practice_type
        ),
        difficulty=recommendation.difficulty,
        title=recommendation.title,
        instruction=recommendation.instruction,
        strategy=None,
        status="pending",
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


# ============================================================
# 2. GET ALL TASKS FOR A LEARNER
# ============================================================

def get_learner_tasks(
    db: Session,
    learner_id: int,
):
    return (
        db.query(PracticeTask)
        .filter(
            PracticeTask.learner_id == learner_id
        )
        .order_by(
            PracticeTask.created_at.desc()
        )
        .all()
    )


# ============================================================
# 3. GET ONE PRACTICE TASK
# ============================================================

def get_task(
    db: Session,
    task_id: int,
):
    return (
        db.query(PracticeTask)
        .filter(
            PracticeTask.id == task_id
        )
        .first()
    )


# ============================================================
# 4. SUBMIT TASK ATTEMPT
# ============================================================

def submit_task_attempt(
    db: Session,
    task_id: int,
    text: str,
):
    task = get_task(
        db=db,
        task_id=task_id,
    )

    if task is None:
        return {
            "error": "Practice task not found"
        }

    if task.status == "completed":
        return {
            "error": (
                "This practice task is already completed"
            )
        }

    previous_attempt_count = (
        db.query(PracticeAttempt)
        .filter(
            PracticeAttempt.task_id == task_id
        )
        .count()
    )

    next_attempt_number = (
        previous_attempt_count + 1
    )

    attempt = PracticeAttempt(
        learner_id=task.learner_id,
        task_id=task.id,
        text=text,
        attempt_number=next_attempt_number,
    )

    task.status = "submitted"

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return attempt


# ============================================================
# 5. GET TASK ATTEMPT HISTORY
# ============================================================

def get_task_attempts(
    db: Session,
    task_id: int,
):
    return (
        db.query(PracticeAttempt)
        .filter(
            PracticeAttempt.task_id == task_id
        )
        .order_by(
            PracticeAttempt.attempt_number.asc()
        )
        .all()
    )


# ============================================================
# 6. GENERATE ADAPTIVE PRACTICE TASK
# ============================================================

def generate_adaptive_practice_task(
    db: Session,
    learner_id: int,
):
    # --------------------------------------------------------
    # Step 1: Calculate learner priorities
    # --------------------------------------------------------

    priorities = calculate_adaptive_priorities(
        db=db,
        learner_id=learner_id,
    )

    if not priorities:
        return {
            "error": (
                "Not enough learner data to generate "
                "an adaptive task"
            )
        }

    # --------------------------------------------------------
    # Step 2: Determine practice strategy
    # --------------------------------------------------------

    strategy_result = determine_practice_strategy(
        db=db,
        learner_id=learner_id,
    )

    if "error" in strategy_result:
        return strategy_result

    selected_skill = strategy_result[
        "selected_skill"
    ]

    # --------------------------------------------------------
    # Step 3: Find priority information for selected skill
    # --------------------------------------------------------

    selected_priority = next(
        (
            item
            for item in priorities
            if item["skill"] == selected_skill
        ),
        priorities[0],
    )

    # --------------------------------------------------------
    # Step 4: Generate strategy-aware task
    # --------------------------------------------------------

    generated_task = generate_adaptive_task(
        target_skill=selected_skill,
        priority_score=selected_priority[
            "priority_score"
        ],
        average_score=selected_priority[
            "average_score"
        ],
        latest_score=selected_priority[
            "latest_score"
        ],
        trend=selected_priority["trend"],
        strategy=strategy_result["strategy"],
    )

    # --------------------------------------------------------
    # Step 5: Save generated task
    # --------------------------------------------------------

    task = PracticeTask(
        learner_id=learner_id,
        target_skill=selected_skill,
        practice_type=(
            generated_task.practice_type
        ),
        difficulty=generated_task.difficulty,
        title=generated_task.title,
        instruction=generated_task.instruction,

        # Save why this task was selected
        strategy=strategy_result["strategy"],

        status="pending",
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task