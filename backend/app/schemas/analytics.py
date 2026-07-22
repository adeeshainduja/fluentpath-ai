from datetime import datetime

from pydantic import BaseModel, Field


class AnalyticsPeriodPoint(BaseModel):
    period: str
    average_score: float
    practice_count: int


class AnalyticsDatePoint(BaseModel):
    date: str
    score: float


class AnalyticsChartPoint(BaseModel):
    label: str
    value: float


class AnalyticsSkillTrend(BaseModel):
    skill: str
    total_attempts: int
    average_score: float
    first_score: float
    latest_score: float
    score_change: float
    trend: str


class AnalyticsPracticeDistribution(BaseModel):
    practice_type: str
    count: int
    percentage: float


class AnalyticsResponse(BaseModel):
    overall_performance: float
    average_score: float
    total_practices: int
    practice_minutes: int
    weekly_progress: float
    monthly_progress: float
    reading_accuracy: float
    listening_accuracy: float
    speaking_accuracy: float
    writing_accuracy: float
    vocabulary_accuracy: float
    daily_streak: int
    weakest_skill: str
    strongest_skill: str
    practice_distribution: list[AnalyticsPracticeDistribution] = Field(default_factory=list)
    recent_improvement: float
    skill_trend: list[AnalyticsSkillTrend] = Field(default_factory=list)
    weekly_score_trend: list[AnalyticsPeriodPoint] = Field(default_factory=list)
    monthly_score_trend: list[AnalyticsPeriodPoint] = Field(default_factory=list)
    practice_type_distribution: list[AnalyticsPracticeDistribution] = Field(default_factory=list)
    skill_comparison: list[AnalyticsChartPoint] = Field(default_factory=list)
    progress_timeline: list[AnalyticsDatePoint] = Field(default_factory=list)
    daily_activity: list[AnalyticsDatePoint] = Field(default_factory=list)
    recent_attempts: list[dict] = Field(default_factory=list)
    insights: list[str] = Field(default_factory=list)
    summary: dict | None = None
