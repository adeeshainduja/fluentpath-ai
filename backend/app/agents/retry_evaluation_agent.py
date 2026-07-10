import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.schemas.evaluation import RetryEvaluationResult


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


SYSTEM_INSTRUCTIONS = """
You are the Retry Evaluation Agent for FluentPath AI.

Compare a learner's original sentence and retry.

Evaluate only the requested target error category.

Rules:

1. Determine whether the target error was resolved.
2. Determine whether the retry shows improvement.
3. Give short learner-friendly feedback.
4. Do not provide the complete corrected sentence.
5. Do not reveal the final answer.
6. next_action must be one of:
   - complete
   - request_next_hint
   - retry_again
"""


def evaluate_retry(
    original_text: str,
    retry_text: str,
    target_category: str,
) -> RetryEvaluationResult:

    prompt = f"""
Original sentence:
{original_text}

Retry sentence:
{retry_text}

Target error category:
{target_category}

Evaluate whether the learner resolved the target error.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTIONS,
            response_mime_type="application/json",
            response_schema=RetryEvaluationResult,
        ),
    )

    return RetryEvaluationResult.model_validate_json(
        response.text
    )