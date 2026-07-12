from datetime import datetime
from typing import List, Dict, Optional

from pydantic import BaseModel


class DashboardSummary(BaseModel):
    average_score: float
    completed_tasks: int
    pending_tasks: int
    learning_trend: str
    recommended_skill: Optional[str]
    recommended_strategy: Optional[str]


class SkillProgress(BaseModel):
    skill: str
    score: float
    trend: str


class LearningTimeline(BaseModel):
    date: str
    practice_count: int
    average_score: float


class PracticeHistory(BaseModel):
    task_id: int
    task_type: str
    difficulty: str
    status: str
    created_at: datetime


class ErrorStatistics(BaseModel):
    total_errors: int
    error_distribution: Dict[str, int]


class TrendAnalytics(BaseModel):
    trend: str
    average_score: float
    recent_average: float


class Recommendation(BaseModel):
    strategy: str
    priority_skill: Optional[str] = None
    reason: Optional[str] = None


class DashboardResponse(BaseModel):
    summary: DashboardSummary
    skill_progress: List[SkillProgress]
    learning_timeline: List[LearningTimeline]
    practice_history: List[PracticeHistory]
    recommendations: Recommendation
    error_statistics: ErrorStatistics
    trend_analytics: TrendAnalytics