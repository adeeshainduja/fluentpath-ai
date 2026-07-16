from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

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
    db: Session = Depends(get_db),
):

    transcript = request.transcript.strip()

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
        learner_id=request.learner_id,
        transcript=transcript,
        evaluation=evaluation,
    )

    feedback = build_speaking_feedback(
        evaluation,
    )

    return {
        "attempt_id": attempt.id,
        "transcript": transcript,
        **feedback,
    }
