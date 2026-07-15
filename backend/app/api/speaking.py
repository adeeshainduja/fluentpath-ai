from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.speaking import (
    SpeakingSubmission,
    SpeakingResponse,
)

from app.services.speech_to_text_service import (
    transcribe_audio,
)

from app.services.pronunciation_service import (
    analyze_pronunciation,
)

from app.services.speaking_evaluation_service import (
    evaluate_speaking,
)

from app.services.speaking_feedback_service import (
    build_speaking_feedback,
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

    transcript = request.transcript

    pronunciation = analyze_pronunciation(
        transcript,
    )

    evaluation = evaluate_speaking(
        transcript,
    )

    feedback = build_speaking_feedback(
        pronunciation,
        evaluation,
    )

    return {
        "transcript": transcript,
        **feedback,
    }