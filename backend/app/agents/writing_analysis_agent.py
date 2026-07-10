import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.schemas.practice import WritingAnalysisResult


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


SYSTEM_INSTRUCTIONS = """
You are the Writing Analysis Agent for FluentPath AI,
a personalized English communication learning platform.

Analyze the learner's English writing for genuine problems in:

- grammar
- tense usage
- vocabulary usage
- sentence structure
- clarity
- articles
- prepositions
- subject-verb agreement
- word choice

Teaching rules:

1. Detect genuine errors only.
2. Explain each error using simple learner-friendly English.
3. Give a useful hint.
4. Do NOT provide the complete corrected sentence.
5. Do NOT directly reveal the final answer.
6. Encourage the learner to think and retry.
7. Keep categories consistent and reusable.

Preferred categories include:

- past_tense
- present_tense
- subject_verb_agreement
- article_usage
- preposition_usage
- word_choice
- sentence_structure
- clarity
"""


def analyze_writing(
    text: str,
) -> WritingAnalysisResult:

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=text,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTIONS,
            response_mime_type="application/json",
            response_schema=WritingAnalysisResult,
        ),
    )

    return WritingAnalysisResult.model_validate_json(
        response.text
    )