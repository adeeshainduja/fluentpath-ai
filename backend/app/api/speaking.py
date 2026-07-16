from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_optional_current_user
from app.models.user import User

from app.schemas.speaking import (
    SpeakingSubmission,
    SpeakingResponse,
)

from app.services.speaking_evaluation_service import (
    evaluate_speaking,
    save_speaking_attempt,
)

from app.services.speaking_feedback_service import (
    build_speaking_feedback,
)
from app.services.gemini_service import (
    GeminiConfigurationError,
    GeminiServiceError,
)

router = APIRouter(
    prefix="/api/v1/speaking",
    tags=["Speaking"],
)


@router.post(
    "/evaluate",
    response_model=SpeakingResponse,
)
def evaluate(
    request: SpeakingSubmission,
    current_user: User | None = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
):

    transcript = request.transcript.strip()
    learner_id = (
        current_user.id
        if current_user is not None
        else request.learner_id
    )

    if learner_id is None:
        raise HTTPException(
            status_code=400,
            detail="learner_id is required.",
        )

    try:
        evaluation = evaluate_speaking(
            transcript,
        )
    except GeminiConfigurationError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc
    except GeminiServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    attempt = save_speaking_attempt(
        db=db,
        learner_id=learner_id,
        transcript=transcript,
        evaluation=evaluation,
    )

    feedback = build_speaking_feedback(
        evaluation,
    )
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

    return {
        "attempt_id": attempt.id,
        "transcript": transcript,
        "score": overall_score,
        **feedback,
    }
