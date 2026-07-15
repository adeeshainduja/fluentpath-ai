from typing import List, Literal

from pydantic import BaseModel


class RoadmapItem(BaseModel):
    id: int
    title: str
    skill: str
    difficulty: str
    estimated_minutes: int
    status: Literal["completed", "current", "locked"]


class CurrentStage(BaseModel):
    id: int
    title: str
    skill: str
    difficulty: str
    estimated_minutes: int


class Badge(BaseModel):
    id: int
    title: str
    description: str
    earned: bool


class LearningPathResponse(BaseModel):
    overall_progress: int

    streak: int

    coach_message: str

    current_stage: CurrentStage

    roadmap: List[RoadmapItem]

    badges: List[Badge]