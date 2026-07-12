from sqlalchemy.orm import Session

from app.models.progress_metric import ProgressMetric


def save_progress_metric(
    db: Session,
    learner_id: int,
    task_id: int,
    attempt_id: int,
    target_skill: str,
    task_score: int,
    response_text: str,
    relevant: bool,
    sufficient_detail: bool,
    target_skill_practiced: bool,
):
    """
    Save learner performance after a task evaluation.
    """

    metric = ProgressMetric(
        learner_id=learner_id,
        task_id=task_id,
        attempt_id=attempt_id,
        target_skill=target_skill,
        task_score=task_score,
        response_length=len(response_text),
        relevant=relevant,
        sufficient_detail=sufficient_detail,
        target_skill_practiced=target_skill_practiced,
    )

    db.add(metric)
    db.commit()
    db.refresh(metric)

    return metric