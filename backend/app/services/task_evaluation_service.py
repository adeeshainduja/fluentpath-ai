from sqlalchemy.orm import Session

from app.agents.task_evaluation_agent import (
    evaluate_task_response,
)
from app.models.practice_attempt import PracticeAttempt
from app.models.practice_task import PracticeTask
from app.services.progress_metric_service import (
    save_progress_metric,
)


def evaluate_linked_practice_task(
    db: Session,
    attempt_id: int,
):
    # --------------------------------------------------------
    # 1. Find learner attempt
    # --------------------------------------------------------

    attempt = (
        db.query(PracticeAttempt)
        .filter(
            PracticeAttempt.id == attempt_id
        )
        .first()
    )

    if attempt is None:
        return {
            "error": "Practice attempt not found"
        }

    # --------------------------------------------------------
    # 2. Check task connection
    # --------------------------------------------------------

    if attempt.task_id is None:
        return {
            "error": (
                "This attempt is not linked "
                "to a practice task"
            )
        }

    # --------------------------------------------------------
    # 3. Load linked task
    # --------------------------------------------------------

    task = (
        db.query(PracticeTask)
        .filter(
            PracticeTask.id == attempt.task_id
        )
        .first()
    )

    if task is None:
        return {
            "error": "Linked practice task not found"
        }

    # --------------------------------------------------------
    # 4. Evaluate learner response
    # --------------------------------------------------------

    evaluation = evaluate_task_response(
        task_instruction=task.instruction,
        learner_response=attempt.text,
        target_skill=task.target_skill,
    )

    # --------------------------------------------------------
    # 5. Update task status
    # --------------------------------------------------------

    if evaluation.task_completed:
        task.status = "completed"
    else:
        task.status = "retry_required"

    db.commit()
    db.refresh(task)

    # --------------------------------------------------------
    # 6. Save progress metric
    # --------------------------------------------------------

    progress_metric = save_progress_metric(
        db=db,
        learner_id=attempt.learner_id,
        task_id=task.id,
        attempt_id=attempt.id,
        target_skill=task.target_skill,
        task_score=evaluation.score,
        response_text=attempt.text,
        relevant=evaluation.relevant,
        sufficient_detail=(
            evaluation.sufficient_detail
        ),
        target_skill_practiced=(
            evaluation.target_skill_practiced
        ),
    )

    # --------------------------------------------------------
    # 7. Return complete evaluation result
    # --------------------------------------------------------

    return {
        "attempt_id": attempt.id,
        "task_id": task.id,
        "task_title": task.title,
        "task_instruction": task.instruction,
        "target_skill": task.target_skill,
        "learner_response": attempt.text,
        "task_status": task.status,
        "task_evaluation": evaluation,
        "progress_metric": {
            "id": progress_metric.id,
            "task_score": (
                progress_metric.task_score
            ),
            "response_length": (
                progress_metric.response_length
            ),
            "relevant": (
                progress_metric.relevant
            ),
            "sufficient_detail": (
                progress_metric.sufficient_detail
            ),
            "target_skill_practiced": (
                progress_metric.target_skill_practiced
            ),
        },
    }