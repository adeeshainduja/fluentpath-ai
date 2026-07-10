import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class AdaptiveTaskResult(BaseModel):
    title: str
    instruction: str
    practice_type: str
    difficulty: str


SYSTEM_INSTRUCTIONS = """
You are the Adaptive Task Generation Agent for FluentPath AI.

Create one English communication practice task based on the
learner's highest-priority weakness.

The task must:

1. Focus on the target skill.
2. Require the learner to produce their own English.
3. Be practical and related to real communication.
4. Not provide the correct answer.
5. Not provide a model answer.
6. Be suitable for university students and software-engineering
   job seekers.
7. Use clear and simple task instructions.

practice_type must be exactly one of:
- writing
- speaking
- interview
- scenario

difficulty must be exactly one of:
- beginner
- intermediate
- advanced
"""


def generate_adaptive_task(
    target_skill: str,
    priority_score: float,
    average_score: float | None,
    trend: str,
) -> AdaptiveTaskResult:

    prompt = f"""
Create one personalized English practice task.

Target skill:
{target_skill}

Priority score:
{priority_score}

Current average score:
{average_score}

Performance trend:
{trend}

Create a task that helps the learner actively practice
the target skill.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTIONS,
            response_mime_type="application/json",
            response_schema=AdaptiveTaskResult,
        ),
    )

    return AdaptiveTaskResult.model_validate_json(
        response.text
    )