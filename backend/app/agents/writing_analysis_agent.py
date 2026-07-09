from app.schemas.practice import (
    DetectedError,
    WritingAnalysisResult,
)


def analyze_writing(text: str) -> WritingAnalysisResult:

    errors = []

    normalized_text = text.lower().strip()

    if "yesterday i go" in normalized_text:

        errors.append(
            DetectedError(
                error_type="grammar",
                category="past_tense",
                problem_text="go",
                explanation=(
                    "The sentence describes an action "
                    "that happened in the past."
                ),
                hint=(
                    "Think about the past form "
                    "of the verb 'go'."
                ),
            )
        )

    if errors:

        return WritingAnalysisResult(
            has_errors=True,
            errors=errors,
            instruction="Try writing the sentence again.",
        )

    return WritingAnalysisResult(
        has_errors=False,
        errors=[],
        instruction="Good attempt. No known error was detected.",
    )