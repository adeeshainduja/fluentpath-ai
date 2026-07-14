from unittest import result

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
    task_id=task.id,
    attempt_id=attempt.id,
    target_skill=task.target_skill,

    task_score=result["overall_score"],

    grammar_score=result["grammar"],
    vocabulary_score=result["vocabulary"],
    fluency_score=result["fluency"],
    pronunciation_score=result["pronunciation"],

    response_length=len(answer),
    relevant=result["relevant"],
    sufficient_detail=result["sufficient_detail"],
    target_skill_practiced=result["target_skill_practiced"],
)

    db.add(metric)
    db.commit()
    db.refresh(metric)

    return metric