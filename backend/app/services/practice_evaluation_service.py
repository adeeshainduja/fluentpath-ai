from app.schemas.practice_submission import (
    PracticeSubmissionResponse,
)

from app.services.gemini_service import (
    evaluate_english,
)


def evaluate_practice(answer: str):

    result = evaluate_english(answer)

    return PracticeSubmissionResponse(
        score=result["score"],
        feedback=result["feedback"],
        grammar_score=result["grammar_score"],
        vocabulary_score=result["vocabulary_score"],
        fluency_score=result["fluency_score"],
        pronunciation_score=None,
        suggestions=result["suggestions"],
    )