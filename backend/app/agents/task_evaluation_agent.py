import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.schemas.task_evaluation import (
    TaskEvaluationResult,
)


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


SYSTEM_INSTRUCTIONS = """
You are the Task Evaluation Agent for FluentPath AI.

Evaluate whether an English learner's response successfully
completes the assigned practice task.

Evaluate:

1. Task completion
2. Relevance to the task
3. Sufficient detail
4. Whether the target language skill was practiced

Important rules:

- Do not evaluate grammar correctness here.
- Do not rewrite the learner's answer.
- Do not provide a complete replacement answer.
- Give short and clear learner-friendly feedback.

The score must be an integer from 0 to 100.

next_action must be exactly one of:

- complete
- retry_task
- add_more_detail
- focus_on_target_skill
"""


def evaluate_task_response(
    task_instruction: str,
    learner_response: str,
    target_skill: str,
) -> TaskEvaluationResult:

    prompt = f"""
Practice task:
{task_instruction}

Target skill:
{target_skill}

Learner response:
{learner_response}

Evaluate whether the learner completed the task.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTIONS,
            response_mime_type="application/json",
            response_schema=TaskEvaluationResult,
        ),
    )

    return TaskEvaluationResult.model_validate_json(
        response.text
    )