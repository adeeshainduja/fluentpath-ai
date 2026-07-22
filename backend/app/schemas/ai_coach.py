from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.learning_path import LearningPathResponse


class AICoachChatRequest(BaseModel):
    message: str = Field(min_length=1)


class AICoachChatMessage(BaseModel):
    role: str
    message: str
    summary: str | None = None
    current_focus: str | None = None
    previous_recommendation: str | None = None
    created_at: datetime


class AICoachLearnerSummary(BaseModel):
    current_level: str
    overall_progress: int
    current_focus: str
    recommended_practice: str
    weak_skills: list[str] = Field(default_factory=list)
    strong_skills: list[str] = Field(default_factory=list)
    recent_practices: list[dict] = Field(default_factory=list)
    average_score: float


class AICoachNextAction(BaseModel):
    title: str
    description: str


class AICoachChatResponse(BaseModel):
    reply: str
    conversation_history: list[AICoachChatMessage] = Field(default_factory=list)
    suggested_questions: list[str] = Field(default_factory=list)
    current_learner_summary: AICoachLearnerSummary
    recommended_next_action: AICoachNextAction
    weak_skills: list[str] = Field(default_factory=list)
    strong_skills: list[str] = Field(default_factory=list)
    current_learning_path: LearningPathResponse
