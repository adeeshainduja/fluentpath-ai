def build_speaking_feedback(
    pronunciation,
    evaluation,
):
    """
    Merge pronunciation analysis and
    AI evaluation into one response.
    """

    return {
        "pronunciation": pronunciation,
        "evaluation": evaluation,
        "coach_message": (
            "Great effort! "
            "Practice speaking a little slower "
            "and focus on sentence fluency."
        ),
    }