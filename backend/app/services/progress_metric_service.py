from sqlalchemy.orm import Session

from app.models.progress_metric import ProgressMetric


def save_progress_metric(
    db: Session,
    learner_id: int,
    task_id: int,
    attempt_id: int,
    target_skill: str,
    evaluation,
):
    metric = ProgressMetric(
        learner_id=learner_id,
        task_id=task_id,
        attempt_id=attempt_id,
        target_skill=target_skill,
        task_score=evaluation.score,
        response_length=0,
        relevant=evaluation.relevant,
        sufficient_detail=evaluation.sufficient_detail,
        target_skill_practiced=evaluation.target_skill_practiced,
    )

    db.add(metric)
    db.commit()
    db.refresh(metric)

    return metric