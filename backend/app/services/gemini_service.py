import os
from typing import TypeVar

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field, ValidationError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

load_dotenv()

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash",
)

T = TypeVar("T", bound=BaseModel)


class GeminiConfigurationError(RuntimeError):
    """Raised when Gemini cannot be configured safely."""


class GeminiServiceError(RuntimeError):
    """Raised when Gemini fails after retryable attempts."""


class GeminiResponseError(GeminiServiceError):
    """Raised when Gemini returns an invalid structured response."""


class _RetryableGeminiError(RuntimeError):
    """Internal retry marker for transient Gemini failures."""


class WritingEvaluationResult(BaseModel):
    score: int = Field(ge=0, le=100)
    grammar_score: int = Field(ge=0, le=100)
    vocabulary_score: int = Field(ge=0, le=100)
    fluency_score: int = Field(ge=0, le=100)
    feedback: str = Field(min_length=1)
    suggestions: list[str] = Field(default_factory=list)


class SpeakingEvaluationResult(BaseModel):
    grammar_score: int = Field(ge=0, le=100)
    vocabulary_score: int = Field(ge=0, le=100)
    fluency_score: int = Field(ge=0, le=100)
    pronunciation_score: int = Field(ge=0, le=100)
    confidence_score: int = Field(ge=0, le=100)

    grammar_feedback: str = Field(min_length=1)
    vocabulary_feedback: str = Field(min_length=1)
    pronunciation_feedback: str = Field(min_length=1)
    fluency_feedback: str = Field(min_length=1)
    overall_feedback: str = Field(min_length=1)
    coach_message: str = Field(min_length=1)
    suggestions: list[str] = Field(default_factory=list)


def _get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise GeminiConfigurationError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(api_key=api_key)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(
        multiplier=1,
        min=1,
        max=8,
    ),
    retry=retry_if_exception_type(
        _RetryableGeminiError
    ),
    reraise=True,
)
def _generate_structured_content(
    *,
    prompt: str,
    system_instruction: str,
    response_schema: type[T],
) -> T:
    try:
        response = _get_client().models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=response_schema,
            ),
        )
    except GeminiConfigurationError:
        raise
    except Exception as exc:
        raise _RetryableGeminiError(
            "Gemini request failed."
        ) from exc

    try:
        return response_schema.model_validate_json(
            response.text
        )
    except (ValidationError, ValueError, TypeError) as exc:
        raise _RetryableGeminiError(
            "Gemini returned invalid JSON."
        ) from exc


def generate_structured_content(
    *,
    prompt: str,
    system_instruction: str,
    response_schema: type[T],
) -> T:
    try:
        return _generate_structured_content(
            prompt=prompt,
            system_instruction=system_instruction,
            response_schema=response_schema,
        )
    except GeminiConfigurationError:
        raise
    except _RetryableGeminiError as exc:
        raise GeminiResponseError(
            "Gemini did not return a valid response."
        ) from exc


def evaluate_english(
    answer: str,
) -> WritingEvaluationResult:
    prompt = f"""
Evaluate this learner writing sample.

Learner writing:
{answer}

Assess grammar, vocabulary, fluency, clarity, and sentence control.
Give learner-friendly feedback and specific next-step suggestions.
Use scores from 0 to 100.
"""

    return generate_structured_content(
        prompt=prompt,
        system_instruction=(
            "You are FluentPath AI's writing evaluation agent. "
            "Return only valid JSON matching the provided schema. "
            "Do not invent facts about the learner. "
            "Base every score and suggestion on the submitted text."
        ),
        response_schema=WritingEvaluationResult,
    )


def evaluate_speaking_transcript(
    transcript: str,
) -> SpeakingEvaluationResult:
    prompt = f"""
Evaluate this spoken-English transcript.

Transcript:
{transcript}

Assess grammar, vocabulary range, spoken fluency, pronunciation cues
visible from the transcript, confidence, pauses or hesitation markers,
and overall communicative clarity.

Use scores from 0 to 100. Explain why the learner received the feedback.
"""

    return generate_structured_content(
        prompt=prompt,
        system_instruction=(
            "You are FluentPath AI's speaking evaluation agent. "
            "Return only valid JSON matching the provided schema. "
            "If pronunciation cannot be fully known from the transcript, "
            "score only transcript-visible speaking cues and say that in "
            "the pronunciation feedback. Do not use placeholder feedback."
        ),
        response_schema=SpeakingEvaluationResult,
    )
