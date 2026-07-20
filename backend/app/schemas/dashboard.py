from datetime import datetime

from pydantic import BaseModel, Field


class DashboardSkillScore(BaseModel):
    skill: str
    score: float


class DashboardWeeklyProgress(BaseModel):
    completed: int
    target: int
    percentage: float


class DashboardPracticeItem(BaseModel):
    task_id: int | None = None
    title: str | None = None
    practice_type: str | None = None
    target_skill: str | None = None
    score: float | None = None
    created_at: datetime


class DashboardAchievement(BaseModel):
    title: str
    description: str | None = None
    earned: bool = True
    icon: str = "award"


class DashboardResponse(BaseModel):
    learner_name: str
    total_practices: int
    average_score: float
    reading_score: float
    listening_score: float
    speaking_score: float
    writing_score: float
    vocabulary_score: float
    daily_streak: int
    weekly_goal_progress: DashboardWeeklyProgress
    completed_practices_this_week: int
    achievements: list[DashboardAchievement] = Field(default_factory=list)
    latest_practice: DashboardPracticeItem | None = None
    ai_recommendation_summary: str | None = None
    skill_scores: list[DashboardSkillScore] = Field(default_factory=list)
    summary: dict | None = None
    skill_progress: list[dict] = Field(default_factory=list)
    learning_timeline: list[dict] = Field(default_factory=list)
    practice_history: list[dict] = Field(default_factory=list)
    recommendations: dict | None = None
    error_statistics: dict | None = None
    trend_analytics: dict | None = None
    weak_skills: list[dict] = Field(default_factory=list)
    daily_missions: list[dict] = Field(default_factory=list)
    achievement_badges: list[dict] = Field(default_factory=list)
