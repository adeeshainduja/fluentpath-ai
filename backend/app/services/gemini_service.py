import os
import json
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def evaluate_english(answer: str):
    prompt = f"""
You are an English communication coach.

Evaluate the student's answer.

Student Answer:
{answer}

Return ONLY valid JSON.

{{
    "score": 0,
    "grammar_score": 0,
    "vocabulary_score": 0,
    "fluency_score": 0,
    "feedback": "",
    "suggestions": []
}}
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)