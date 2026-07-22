from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.services.gemini_service import (
    GeminiConfigurationError,
    GeminiResponseError,
    generate_structured_content,
)
from app.services.analytics_service import get_user_analytics
from app.services.learning_path_service import get_learning_path
from app.services.practice_history_service import get_practice_history_items
from app.memory.learner_memory import get_learner_weaknesses


class GeneratedMCQ(BaseModel):
    id: int
    question: str
    options: list[str]
    answer: str
    explanation: str


class GeneratedReading(BaseModel):
    passage_id: str
    title: str
    passage: str
    estimated_minutes: int = Field(ge=1, le=60)
    questions: list[GeneratedMCQ]


class GeneratedListening(BaseModel):
    practice_id: str
    transcript: str
    audio_url: str
    estimated_minutes: int = Field(ge=1, le=60)
    questions: list[GeneratedMCQ]


class GeneratedVocabularyQuestion(BaseModel):
    id: int
    word: str
    question: str
    options: list[str]
    answer: str
    explanation: str
    example_sentence: str | None = None


class GeneratedVocabulary(BaseModel):
    session_id: int
    difficulty: str
    questions: list[GeneratedVocabularyQuestion]


class GeneratedSpeaking(BaseModel):
    topic: str
    follow_up_questions: list[str]
    pronunciation_feedback: str
    fluency_feedback: str
    grammar_feedback: str
    coach_message: str


class GeneratedWriting(BaseModel):
    prompt: str
    evaluation: str
    grammar_feedback: str
    vocabulary_feedback: str
    coherence_feedback: str


def _build_context(db: Session, learner_id: int) -> dict[str, Any]:
    analytics = get_user_analytics(db=db, learner_id=learner_id)
    learning_path = get_learning_path(db=db, learner_id=learner_id)
    weaknesses = [item.category for item in get_learner_weaknesses(db=db, learner_id=learner_id)[:5]]
    history = get_practice_history_items(db=db, learner_id=learner_id)[:5]
    return {
        "current_level": learning_path.current_level,
        "weak_skills": learning_path.weak_skills or weaknesses,
        "strong_skills": learning_path.strong_skills,
        "current_goal": learning_path.current_focus,
        "learning_path": learning_path.model_dump(),
        "analytics": analytics,
        "practice_history": [
            {
                "practice_type": item.practice_type,
                "target_skill": item.target_skill,
                "score": item.score,
                "title": item.title,
                "date": item.completed_date.isoformat(),
            }
            for item in history
        ],
    }


def _fallback_reading() -> dict:
    return {
        "passage_id": "fallback-reading-01",
        "title": "A Community Project",
        "passage": (
            "Mina and her class organized a weekend cleanup in the park. "
            "They collected bottles, planted flowers, and wrote signs to remind visitors to keep the area clean. "
            "By the end of the afternoon, the park looked brighter and the students felt proud of their work."
        ),
        "estimated_minutes": 8,
        "questions": [
            {
                "id": 1,
                "question": "What did Mina and her class organize?",
                "options": [
                    "A weekend cleanup in the park",
                    "A science fair at school",
                    "A concert downtown",
                    "A cooking competition",
                ],
                "answer": "A weekend cleanup in the park",
                "explanation": "The passage says they organized a weekend cleanup in the park.",
            },
            {
                "id": 2,
                "question": "What did they collect?",
                "options": [
                    "Bottles",
                    "Books",
                    "Leaves only",
                    "Tickets",
                ],
                "answer": "Bottles",
                "explanation": "The students collected bottles during the cleanup.",
            },
            {
                "id": 3,
                "question": "What did they plant?",
                "options": [
                    "Flowers",
                    "Trees",
                    "Corn",
                    "Grass",
                ],
                "answer": "Flowers",
                "explanation": "They planted flowers in the park.",
            },
            {
                "id": 4,
                "question": "Why did they write signs?",
                "options": [
                    "To remind visitors to keep the area clean",
                    "To advertise a sale",
                    "To invite people to lunch",
                    "To explain park rules for parking",
                ],
                "answer": "To remind visitors to keep the area clean",
                "explanation": "The signs were meant to remind visitors to keep the area clean.",
            },
            {
                "id": 5,
                "question": "How did the students feel?",
                "options": [
                    "Proud",
                    "Tired and upset",
                    "Confused",
                    "Bored",
                ],
                "answer": "Proud",
                "explanation": "They felt proud of their work at the end of the afternoon.",
            },
        ],
    }


def _fallback_listening() -> dict:
    return {
        "practice_id": "fallback-listening-01",
        "audio_url": "/audio/listening-sample.mp3",
        "transcript": (
            "Good evening everyone. The town meeting will begin at 6 p.m. in Hall B. "
            "Please bring your notes. After the meeting, speakers can ask questions."
        ),
        "estimated_minutes": 7,
        "questions": [
            {
                "id": 1,
                "question": "When will the meeting begin?",
                "options": ["6 p.m.", "5 p.m.", "7 p.m.", "8 p.m."],
                "answer": "6 p.m.",
                "explanation": "The transcript says the meeting begins at 6 p.m.",
            },
            {
                "id": 2,
                "question": "Where will it take place?",
                "options": ["Hall B", "Hall A", "Room 10", "The lobby"],
                "answer": "Hall B",
                "explanation": "The transcript names Hall B as the location.",
            },
            {
                "id": 3,
                "question": "What should people bring?",
                "options": ["Their notes", "A laptop", "A camera", "A snack"],
                "answer": "Their notes",
                "explanation": "People are asked to bring their notes.",
            },
            {
                "id": 4,
                "question": "What happens after the meeting?",
                "options": ["Speakers can ask questions", "A concert starts", "A movie plays", "The hall closes"],
                "answer": "Speakers can ask questions",
                "explanation": "The transcript says speakers can ask questions after the meeting.",
            },
            {
                "id": 5,
                "question": "Who is the audience?",
                "options": ["Town residents", "Only teachers", "Only children", "Only tourists"],
                "answer": "Town residents",
                "explanation": "The meeting is a town meeting, so the audience is town residents.",
            },
        ],
    }


def _fallback_vocabulary() -> dict:
    return {
        "sessionId": 2,
        "difficulty": "Intermediate",
        "questions": [
            {
                "id": 1,
                "word": "Adapt",
                "question": "Choose the correct meaning.",
                "options": ["Adjust to a new situation", "Break into pieces", "Become silent", "Move very quickly"],
                "answer": "Adjust to a new situation",
                "explanation": "Adapt means to adjust to new conditions.",
            },
            {
                "id": 2,
                "word": "Benefit",
                "question": "Choose the correct meaning.",
                "options": ["A helpful result", "A loud sound", "A small animal", "A closed road"],
                "answer": "A helpful result",
                "explanation": "Benefit means a helpful result or advantage.",
            },
            {
                "id": 3,
                "word": "Carefully",
                "question": "Choose the correct meaning.",
                "options": ["With attention", "Without stopping", "In a noisy way", "Very late"],
                "answer": "With attention",
                "explanation": "Carefully means with attention and caution.",
            },
            {
                "id": 4,
                "word": "Support",
                "question": "Choose the correct meaning.",
                "options": ["Help or assistance", "A long journey", "A sudden mistake", "A hidden room"],
                "answer": "Help or assistance",
                "explanation": "Support means help or assistance.",
            },
        ],
    }


def generate_reading_content(db: Session, learner_id: int) -> dict:
    context = _build_context(db, learner_id)
    prompt = json.dumps(
        {
            "task": "Generate personalized reading practice",
            "context": context,
            "requirements": {
                "title": "string",
                "passage": "string",
                "estimated_minutes": "integer",
                "questions": [
                    {
                        "id": 1,
                        "question": "string",
                        "options": ["string", "string", "string", "string"],
                        "answer": "string",
                        "explanation": "string",
                    }
                ],
            },
        }
    )
    try:
        result = generate_structured_content(
            prompt=prompt,
            system_instruction=(
                "You are FluentPath AI's reading content generator. "
                "Return structured JSON only. "
                "Personalize the passage using the learner context. "
                "Keep the language level aligned to the current level. "
                "Include exactly 5 multiple-choice questions with explanations."
            ),
            response_schema=GeneratedReading,
        )
        return result.model_dump()
    except (GeminiConfigurationError, GeminiResponseError):
        return _fallback_reading()


def generate_listening_content(db: Session, learner_id: int) -> dict:
    context = _build_context(db, learner_id)
    prompt = json.dumps(
        {
            "task": "Generate personalized listening practice",
            "context": context,
            "requirements": {
                "transcript": "string",
                "audio_url": "string",
                "estimated_minutes": "integer",
                "questions": [
                    {
                        "id": 1,
                        "question": "string",
                        "options": ["string", "string", "string", "string"],
                        "answer": "string",
                        "explanation": "string",
                    }
                ],
            },
        }
    )
    try:
        result = generate_structured_content(
            prompt=prompt,
            system_instruction=(
                "You are FluentPath AI's listening content generator. "
                "Return structured JSON only. "
                "Create a short transcript and 5 questions with explanations. "
                "Match difficulty to the learner context."
            ),
            response_schema=GeneratedListening,
        )
        return result.model_dump()
    except (GeminiConfigurationError, GeminiResponseError):
        return _fallback_listening()


def generate_vocabulary_content(db: Session, learner_id: int) -> dict:
    context = _build_context(db, learner_id)
    prompt = json.dumps(
        {
            "task": "Generate personalized vocabulary practice",
            "context": context,
            "requirements": {
                "difficulty": "string",
                "questions": [
                    {
                        "id": 1,
                        "word": "string",
                        "question": "string",
                        "options": ["string", "string", "string", "string"],
                        "answer": "string",
                        "explanation": "string",
                        "example_sentence": "string",
                    }
                ],
            },
        }
    )
    try:
        result = generate_structured_content(
            prompt=prompt,
            system_instruction=(
                "You are FluentPath AI's vocabulary generator. "
                "Return structured JSON only. "
                "Create 4 vocabulary items with distractors and example sentences. "
                "Use learner weaknesses to choose words."
            ),
            response_schema=GeneratedVocabulary,
        )
        return result.model_dump(by_alias=True)
    except (GeminiConfigurationError, GeminiResponseError):
        return _fallback_vocabulary()


def generate_speaking_content(db: Session, learner_id: int) -> dict:
    context = _build_context(db, learner_id)
    prompt = json.dumps(
        {
            "task": "Generate personalized speaking prompt",
            "context": context,
            "requirements": {
                "topic": "string",
                "follow_up_questions": ["string"],
                "pronunciation_feedback": "string",
                "fluency_feedback": "string",
                "grammar_feedback": "string",
                "coach_message": "string",
            },
        }
    )
    try:
        result = generate_structured_content(
            prompt=prompt,
            system_instruction=(
                "You are FluentPath AI's speaking prompt generator. "
                "Return structured JSON only. "
                "Choose a topic that fits the learner's current weakness and level. "
                "Provide concise follow-up questions and feedback targets."
            ),
            response_schema=GeneratedSpeaking,
        )
        return result.model_dump()
    except (GeminiConfigurationError, GeminiResponseError):
        return {
            "topic": "Describe a recent learning success.",
            "follow_up_questions": [
                "What helped you succeed?",
                "What would you improve next time?",
            ],
            "pronunciation_feedback": "Focus on clear stress and pacing.",
            "fluency_feedback": "Try to speak in longer connected phrases.",
            "grammar_feedback": "Use complete sentences and past tense accurately.",
            "coach_message": "Short daily speaking practice will help you improve quickly.",
        }


def generate_writing_content(db: Session, learner_id: int) -> dict:
    context = _build_context(db, learner_id)
    prompt = json.dumps(
        {
            "task": "Generate personalized writing prompt and evaluation guidance",
            "context": context,
            "requirements": {
                "prompt": "string",
                "evaluation": "string",
                "grammar_feedback": "string",
                "vocabulary_feedback": "string",
                "coherence_feedback": "string",
            },
        }
    )
    try:
        result = generate_structured_content(
            prompt=prompt,
            system_instruction=(
                "You are FluentPath AI's writing content generator. "
                "Return structured JSON only. "
                "Generate a writing prompt and concise feedback criteria. "
                "Align the task to the learner's weaknesses."
            ),
            response_schema=GeneratedWriting,
        )
        return result.model_dump()
    except (GeminiConfigurationError, GeminiResponseError):
        return {
            "prompt": "Write a short paragraph about a goal you want to achieve this month.",
            "evaluation": "Focus on clarity, organization, and accurate sentence structure.",
            "grammar_feedback": "Use correct verb tenses and sentence endings.",
            "vocabulary_feedback": "Include a few descriptive words and avoid repeating the same terms.",
            "coherence_feedback": "Connect your ideas with simple transition words.",
        }
