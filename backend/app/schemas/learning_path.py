from typing import Literal

from pydantic import BaseModel, Field


class LearningPathTask(BaseModel):
    title: str
    completed: bool


class LearningPathResponse(BaseModel):
    current_level: str
    overall_progress: int
    current_focus: str
    recommended_practice: str
    next_milestone: str
    tasks: list[LearningPathTask] = Field(default_factory=list)
    weak_skills: list[str] = Field(default_factory=list)
    strong_skills: list[str] = Field(default_factory=list)
    learning_timeline: list[dict] = Field(default_factory=list)
    skill_roadmap: list[dict] = Field(default_factory=list)
    weekly_tasks: list[LearningPathTask] = Field(default_factory=list)
    completed_tasks: list[LearningPathTask] = Field(default_factory=list)
    progress_bar: int = 0
    today_recommendation: str = ""


class LearningPathUpdateResponse(BaseModel):
    status: Literal["updated"] = "updated"
    path: LearningPathResponse
