from app.services.gemini_service import SpeakingEvaluationResult


def build_speaking_feedback(
    evaluation: SpeakingEvaluationResult,
):
    return {
        "pronunciation": {
            "score": evaluation.pronunciation_score,
            "fluency": evaluation.fluency_score,
            "confidence": evaluation.confidence_score,
            "pronunciation": (
                evaluation.pronunciation_score
            ),
            "comments": [
                evaluation.pronunciation_feedback,
            ],
        },
        "evaluation": {
            "grammar_score": evaluation.grammar_score,
            "vocabulary_score": (
                evaluation.vocabulary_score
            ),
            "fluency_score": evaluation.fluency_score,
            "pronunciation_score": (
                evaluation.pronunciation_score
            ),
            "confidence_score": (
                evaluation.confidence_score
            ),
            "grammar_feedback": (
                evaluation.grammar_feedback
            ),
            "vocabulary_feedback": (
                evaluation.vocabulary_feedback
            ),
            "pronunciation_feedback": (
                evaluation.pronunciation_feedback
            ),
            "fluency_feedback": (
                evaluation.fluency_feedback
            ),
            "overall_feedback": (
                evaluation.overall_feedback
            ),
            "suggestions": evaluation.suggestions,
        },
        "coach_message": evaluation.coach_message,
    }
