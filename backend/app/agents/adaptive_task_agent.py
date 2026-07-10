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
You are the Strategy-Aware Task Generation Agent
for FluentPath AI.

Create one personalized English communication practice task.

The task must adapt to:

1. Target skill
2. Practice strategy
3. Latest learner score
4. Performance trend

Strategy behavior:

guided_reinforcement:
- Create a simple and focused task.
- Reduce task complexity.
- Practice one clear skill.
- Give clear instructions.
- Do not give the answer.

reinforce:
- Create normal targeted practice.
- Focus clearly on the selected skill.

review:
- Create a review task using familiar language.
- Help the learner practice the skill again in context.

rotate_skill:
- Create an engaging task with a different real-life context.
- Avoid making it feel like repetitive drilling.

increase_difficulty:
- Create a more challenging task.
- Require longer answers, explanation, reasoning,
  storytelling, or structured communication.

Important rules:

- The learner must produce their own English.
- Do not provide a model answer.
- Do not correct the learner in advance.
- Do not provide the target sentences.
- Make tasks useful for university students and
  software-engineering job seekers.
- Keep instructions clear.

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
    latest_score: float | None,
    trend: str,
    strategy: str,
) -> AdaptiveTaskResult:

    prompt = f"""
Create one personalized English practice task.

Target skill:
{target_skill}

Priority score:
{priority_score}

Average score:
{average_score}

Latest score:
{latest_score}

Performance trend:
{trend}

Practice strategy:
{strategy}

Generate a task that follows the strategy and helps
the learner actively practice the target skill.
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