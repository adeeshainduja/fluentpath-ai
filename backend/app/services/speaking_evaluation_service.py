from app.services.gemini_service import evaluate_text


def evaluate_speaking(
    transcript: str,
):
    """
    Evaluate spoken English using Gemini.
    """

    prompt = f"""
Evaluate this spoken English.

Transcript:

{transcript}

Return:

Grammar Score
Vocabulary Score
Fluency Score
Confidence Score

Grammar Feedback
Vocabulary Feedback
Fluency Feedback
Overall Feedback
"""

    return evaluate_text(prompt)