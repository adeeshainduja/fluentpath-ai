from sqlalchemy.orm import Session

from app.models.practice_attempt import PracticeAttempt

from app.schemas.practice_submission import (
    PracticeSubmissionResponse,
)

from app.services.gemini_service import (
    evaluate_english,
)


def evaluate_practice(
    db: Session,
    attempt_id: int,
) -> PracticeSubmissionResponse:

    attempt = (
        db.query(PracticeAttempt)
        .filter(PracticeAttempt.id == attempt_id)
        .first()
    )

    if attempt is None:
        raise ValueError("Practice attempt not found")

    result = evaluate_english(attempt.text)

    return PracticeSubmissionResponse(
        score=result.score,
        feedback=result.feedback,
        grammar_score=result.grammar_score,
        vocabulary_score=result.vocabulary_score,
        fluency_score=result.fluency_score,
        pronunciation_score=None,
        suggestions=result.suggestions,
    )
