from app.schemas.practice_submission import (
    PracticeSubmissionResponse,
)


def evaluate_practice(answer: str) -> PracticeSubmissionResponse:
    """
    Temporary AI evaluation.

    Later this will use Gemini to evaluate
    grammar, vocabulary, fluency, etc.
    """

    word_count = len(answer.split())

    score = min(100, word_count * 2)

    if score >= 80:
        feedback = "Excellent work! Your answer is detailed and well structured."
    elif score >= 60:
        feedback = "Good job. Try using richer vocabulary and longer sentences."
    elif score >= 40:
        feedback = "Fair attempt. Improve grammar and sentence structure."
    else:
        feedback = "Try writing a more complete answer."

    return PracticeSubmissionResponse(
        score=score,
        feedback=feedback,
        grammar_score=80,
        vocabulary_score=78,
        fluency_score=82,
        pronunciation_score=None,
    )