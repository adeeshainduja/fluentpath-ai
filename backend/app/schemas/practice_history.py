from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


PracticeHistoryType = Literal[
    "all",
    "writing",
    "speaking",
]


class PracticeHistoryItem(BaseModel):
    record_id: str
    source: Literal[
        "practice_attempt",
        "speaking_attempt",
    ]

    attempt_id: int
    learner_id: int
    practice_type: str

    task_id: int | None = None
    task_title: str | None = None
    target_skill: str | None = None
    difficulty: str | None = None
    status: str | None = None
    strategy: str | None = None

    attempt_number: int | None = None
    submitted_text: str

    score: int | None = None
    grammar_score: int | None = None
    vocabulary_score: int | None = None
    fluency_score: int | None = None
    pronunciation_score: int | None = None
    confidence_score: int | None = None

    feedback: str | None = None
    has_evaluation: bool
    created_at: datetime


class PracticeHistorySummary(BaseModel):
    learner_id: int
    total_practices: int
    writing_practices: int
    speaking_practices: int
    evaluated_practices: int
    average_score: float | None = None
    best_score: int | None = None
    latest_score: int | None = None
    latest_practice_at: datetime | None = None


class PracticeHistoryResponse(BaseModel):
    learner_id: int
    total: int
    limit: int = Field(ge=1, le=100)
    offset: int = Field(ge=0)
    items: list[PracticeHistoryItem]


class PracticeHistoryDetailResponse(BaseModel):
    summary: PracticeHistorySummary
    history: PracticeHistoryResponse
