from app.schemas.practice_submission import (
    PracticeSubmissionResponse,
)


def evaluate_practice(answer: str) -> PracticeSubmissionResponse:
    """
    Temporary AI evaluation.
    Later this will call Gemini/OpenAI.
    """

    word_count = len(answer.split())

    score = min(100, word_count * 2)

    return PracticeSubmissionResponse(
        score=score,
        feedback="Good attempt. Continue improving sentence structure.",
        grammar_score=80,
        vocabulary_score=78,
        fluency_score=82,
        pronunciation_score=None,
    )