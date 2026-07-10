import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.schemas.hint import HintResult


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


SYSTEM_INSTRUCTIONS = """
You are the Hint Agent for FluentPath AI.

Your job is to help an English learner correct their own mistake.

Never immediately provide the full corrected sentence.

Hint levels:

Level 1:
Give a small clue.
Do not explain the full grammar rule.

Level 2:
Explain the relevant grammar or language rule simply.
Still do not provide the full corrected sentence.

Level 3:
Give a stronger hint.
You may provide a short unrelated example or grammatical pattern,
but do not correct the learner's complete original sentence.

Keep feedback short, clear, and encouraging.
"""


def generate_hint(
    attempt_id: int,
    original_text: str,
    error_category: str,
    problem_text: str,
    hint_level: int,
) -> HintResult:

    prompt = f"""
Learner sentence:
{original_text}

Error category:
{error_category}

Problematic text:
{problem_text}

Requested hint level:
{hint_level}

Generate the appropriate hint.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTIONS,
            response_mime_type="application/json",
            response_schema=HintResult,
        ),
    )

    return HintResult.model_validate_json(
        response.text
    )