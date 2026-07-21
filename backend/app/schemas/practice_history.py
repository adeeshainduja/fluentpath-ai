from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


PracticeHistoryType = Literal[
    "all",
    "reading",
    "listening",
    "writing",
    "speaking",
    "vocabulary",
]

PracticeHistorySort = Literal["newest", "oldest", "score_desc", "score_asc"]


class PracticeHistoryItem(BaseModel):
    attempt_id: int
    practice_type: str
    title: str
    completed_date: datetime
    score: int | None = None
    duration: int | None = None
    difficulty: str | None = None
    feedback_summary: str | None = None
    status: str
    target_skill: str | None = None


class PracticeHistoryDetail(BaseModel):
    attempt_id: int
    practice_type: str
    title: str
    completed_date: datetime
    score: int | None = None
    duration: int | None = None
    difficulty: str | None = None
    status: str
    original_practice: dict
    learner_answers: dict
    correct_answers: dict | None = None
    explanations: dict | None = None
    ai_feedback: str | None = None
    feedback_summary: str | None = None
    weaknesses: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    completion_time: datetime | None = None
    suggestions: list[str] = Field(default_factory=list)


class PracticeHistoryResponse(BaseModel):
    total: int
    page: int
    limit: int = Field(ge=1, le=100)
    items: list[PracticeHistoryItem]


class PracticeHistoryDetailResponse(BaseModel):
    history: PracticeHistoryDetail


class PracticeHistoryExportResponse(BaseModel):
    total: int
    items: list[PracticeHistoryItem]
