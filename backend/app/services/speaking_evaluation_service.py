from sqlalchemy.orm import Session

from app.models.speaking_attempt import SpeakingAttempt
from app.services.gemini_service import (
    SpeakingEvaluationResult,
    evaluate_speaking_transcript,
)


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
    db.commit()
    db.refresh(attempt)

    return attempt
