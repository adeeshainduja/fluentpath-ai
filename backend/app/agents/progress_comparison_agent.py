import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.schemas.progress_comparison import (
    ProgressComparisonResult,
)


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


SYSTEM_INSTRUCTIONS = """
You are the Progress Comparison Agent for FluentPath AI.

Your job is to compare two learner responses to the same
English practice task and explain the learner's movement.

Evaluate:

1. Overall improvement
2. Relevance improvement
3. Detail improvement
4. Target skill improvement
5. Remaining learning focus

Important rules:

- Focus on movement between attempts.
- Do not rewrite the learner's complete answer.
- Do not give the perfect answer.
- Keep feedback clear and encouraging.
- Be specific about what changed.
- previous_score and current_score must be integers from 0 to 100.
- score_change must equal current_score minus previous_score.

next_action must be exactly one of:

- continue_practice
- retry_task
- increase_difficulty
- review_target_skill
"""


def compare_attempt_progress(
    task_instruction: str,
    target_skill: str,
    previous_response: str,
    current_response: str,
) -> ProgressComparisonResult:

    prompt = f"""
Practice task:
{task_instruction}

Target skill:
{target_skill}

Previous learner response:
{previous_response}

Current learner response:
{current_response}

Compare the learner's progress between the two attempts.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTIONS,
            response_mime_type="application/json",
            response_schema=ProgressComparisonResult,
        ),
    )

    return ProgressComparisonResult.model_validate_json(
        response.text
    )