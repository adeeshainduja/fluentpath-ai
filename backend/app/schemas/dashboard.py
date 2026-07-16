from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class DashboardSummary(BaseModel):
    average_score: float
    daily_streak: int = 0
    total_practices: int = 0
    completed_tasks: int
    pending_tasks: int
    learning_trend: str
    recommended_skill: Optional[str] = None
    recommended_strategy: Optional[str] = None


class SkillProgress(BaseModel):
    skill: str
    total_attempts: int
    average_score: float
    first_score: int
    latest_score: int
    score_change: int
    trend: str


class LearningTimeline(BaseModel):
    date: str
    practice_count: int
    average_score: float


class PracticeHistory(BaseModel):
    task_id: int | None = None
    title: str | None = None
    target_skill: str | None = None
    practice_type: str | None = None
    difficulty: str | None = None
    status: str | None = None
    strategy: Optional[str] = None
    created_at: datetime


class Recommendation(BaseModel):
    strategy: Optional[str] = None
    priority_skill: Optional[str] = None
    reason: Optional[str] = None


class ErrorDetail(BaseModel):
    error_type: str
    occurrences: int
    resolved: int
    status: str


class ErrorStatistics(BaseModel):
    total_errors: int
    active_errors: int
    resolved_errors: int
    error_distribution: Dict[str, ErrorDetail]


class TrendAnalytics(BaseModel):
    trend: str
    average_score: float
    recent_average: float
    highest_score: int
    lowest_score: int
    total_attempts: int

class WeakSkill(BaseModel):
    skill: str
    score: float
    priority: str
    recommendation: str

class DailyMission(BaseModel):
    skill: str
    target: int
    completed: int
    priority: float


class DashboardResponse(BaseModel):
    summary: DashboardSummary
    skill_progress: List[SkillProgress]
    learning_timeline: List[LearningTimeline]
    practice_history: List[PracticeHistory]
    recommendations: Recommendation
    error_statistics: ErrorStatistics
    trend_analytics: TrendAnalytics
    weak_skills: List[WeakSkill]
    daily_missions: List[DailyMission]
    achievement_badges: list[dict] = []
