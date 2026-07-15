import os
import json
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def evaluate_text(prompt: str):
    """
    Generic Gemini evaluator.
    Returns parsed JSON if possible,
    otherwise returns raw text.
    """

    response = model.generate_content(prompt)

    text = response.text.strip()

    if text.startswith("```"):
        text = (
            text.replace("```json", "")
            .replace("```", "")
            .strip()
        )

    try:
        return json.loads(text)
    except Exception:
        return {
            "response": text
        }


def evaluate_english(answer: str):
    """
    Writing evaluation.
    """

    prompt = f"""
You are an English communication coach.

Evaluate the student's answer.

Student Answer:
{answer}

Return ONLY valid JSON.

{{
    "score":0,
    "grammar_score":0,
    "vocabulary_score":0,
    "fluency_score":0,
    "feedback":"",
    "suggestions":[]
}}
"""

    return evaluate_text(prompt)