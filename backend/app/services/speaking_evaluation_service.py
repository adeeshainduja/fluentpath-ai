from sqlalchemy.orm import Session

from app.models.error_pattern import ErrorPattern
from app.models.practice_attempt import PracticeAttempt
from app.models.practice_task import PracticeTask
from app.models.progress_metric import ProgressMetric
from app.models.speaking_attempt import SpeakingAttempt
from app.models.evaluation_records import SpeakingEvaluation
from app.services.gemini_service import (
    SpeakingEvaluationResult,
    evaluate_speaking_transcript,
)
from datetime import datetime


def evaluate_speaking(
    transcript: str,
) -> SpeakingEvaluationResult:
    return evaluate_speaking_transcript(
        transcript=transcript,
    )


def save_speaking_attempt(
    db: Session,
    learner_id: int,
    transcript: str,
    evaluation: SpeakingEvaluationResult,
) -> SpeakingAttempt:
    overall_score = round(
        (
            evaluation.grammar_score
            + evaluation.vocabulary_score
            + evaluation.fluency_score
            + evaluation.pronunciation_score
            + evaluation.confidence_score
        )
        / 5
    )

    task = PracticeTask(
        learner_id=learner_id,
        target_skill="speaking",
        practice_type="speaking",
        difficulty="adaptive",
        title="Speaking Practice Session",
        instruction="Recorded microphone speaking practice.",
        status="completed",
        strategy="ai_speaking_feedback",
    )

    db.add(task)
    db.flush()

    practice_attempt = PracticeAttempt(
        learner_id=learner_id,
        task_id=task.id,
        text=transcript,
        practice_type="speaking",
    )

    db.add(practice_attempt)
    db.flush()

    attempt = SpeakingAttempt(
        learner_id=learner_id,
        transcript=transcript,
        grammar_score=evaluation.grammar_score,
        vocabulary_score=evaluation.vocabulary_score,
        fluency_score=evaluation.fluency_score,
        pronunciation_score=(
            evaluation.pronunciation_score
        ),
        confidence_score=evaluation.confidence_score,
        overall_feedback=evaluation.overall_feedback,
    )

    db.add(attempt)
    db.flush()

    db.add(
        SpeakingEvaluation(
            user_id=learner_id,
            speaking_attempt_id=attempt.id,
            transcript=transcript,
            result={
                "grammar_score": evaluation.grammar_score,
                "vocabulary_score": evaluation.vocabulary_score,
                "fluency_score": evaluation.fluency_score,
                "pronunciation_score": (
                    evaluation.pronunciation_score
                ),
                "confidence_score": evaluation.confidence_score,
                "grammar_feedback": evaluation.grammar_feedback,
                "vocabulary_feedback": evaluation.vocabulary_feedback,
                "pronunciation_feedback": (
                    evaluation.pronunciation_feedback
                ),
                "fluency_feedback": evaluation.fluency_feedback,
                "overall_feedback": evaluation.overall_feedback,
                "suggestions": evaluation.suggestions,
            },
        )
    )

    db.add(
        ProgressMetric(
            learner_id=learner_id,
            task_id=task.id,
            attempt_id=practice_attempt.id,
            target_skill="speaking",
            task_score=overall_score,
            grammar_score=evaluation.grammar_score,
            vocabulary_score=evaluation.vocabulary_score,
            fluency_score=evaluation.fluency_score,
            pronunciation_score=(
                evaluation.pronunciation_score
            ),
            response_length=len(transcript.split()),
            relevant=True,
            sufficient_detail=len(transcript.split()) >= 8,
            target_skill_practiced=True,
        )
    )

    _update_speaking_error_patterns(
        db=db,
        learner_id=learner_id,
        evaluation=evaluation,
    )

    db.commit()
    db.refresh(attempt)

    return attempt


def _update_speaking_error_patterns(
    db: Session,
    learner_id: int,
    evaluation: SpeakingEvaluationResult,
) -> None:
    score_map = {
        "grammar": (
            evaluation.grammar_score,
            "speaking_grammar",
        ),
        "vocabulary": (
            evaluation.vocabulary_score,
            "speaking_vocabulary",
        ),
        "fluency": (
            evaluation.fluency_score,
            "speaking_fluency",
        ),
        "pronunciation": (
            evaluation.pronunciation_score,
            "speaking_pronunciation",
        ),
    }

    for category, (
        score,
        error_type,
    ) in score_map.items():
        if score >= 70:
            continue

        pattern = (
            db.query(ErrorPattern)
            .filter(
                ErrorPattern.learner_id == learner_id,
                ErrorPattern.category == category,
            )
            .first()
        )

        if pattern is None:
            pattern = ErrorPattern(
                learner_id=learner_id,
                category=category,
                error_type=error_type,
                occurrence_count=1,
                resolved_count=0,
                status="active",
                last_seen_at=datetime.utcnow(),
            )
            db.add(pattern)
        else:
            pattern.occurrence_count += 1
            pattern.error_type = error_type
            pattern.status = "active"
            pattern.last_seen_at = datetime.utcnow()
