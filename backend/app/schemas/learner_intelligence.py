from pydantic import BaseModel, Field


class SkillAverage(BaseModel):
    skill: str
    average_score: float
    attempts: int
    latest_score: int | None = None
    trend: str


class ScoreTrendPoint(BaseModel):
    date: str
    score: int
    practice_type: str
    skill: str | None = None


class PracticeFrequency(BaseModel):
    total_practices: int
    active_days: int
    practices_last_7_days: int
    practices_last_30_days: int
    average_practices_per_active_day: float
    current_streak: int


class LearnerPerformanceAnalysis(BaseModel):
    learner_id: int
    average_scores_by_skill: list[SkillAverage]
    speaking_trend: list[ScoreTrendPoint]
    writing_trend: list[ScoreTrendPoint]
    practice_frequency: PracticeFrequency
    improvement_rate: float | None = None
    consistency: float | None = None
    consistency_label: str


class WeaknessInsight(BaseModel):
    skill: str
    category: str
    score: float | None = None
    evidence: str
    severity: str
    priority: int = Field(ge=0, le=100)


class LearnerWeaknesses(BaseModel):
    learner_id: int
    grammar_topics: list[WeaknessInsight]
    vocabulary_weaknesses: list[WeaknessInsight]
    pronunciation_weaknesses: list[WeaknessInsight]
    fluency_weaknesses: list[WeaknessInsight]
    confidence_weaknesses: list[WeaknessInsight]


class StrengthInsight(BaseModel):
    skill: str
    category: str
    score: float
    evidence: str
    consistency: float | None = None


class LearnerStrengths(BaseModel):
    learner_id: int
    highest_performing_skills: list[StrengthInsight]
    most_improved_skills: list[StrengthInsight]
    consistent_strengths: list[StrengthInsight]


class LearnerRecommendation(BaseModel):
    recommendation: str
    reason: str
    affected_skill: str
    confidence: float = Field(ge=0, le=1)
    priority: int = Field(ge=0, le=100)
    suggested_practice_type: str


class LearnerRecommendations(BaseModel):
    learner_id: int
    recommendations: list[LearnerRecommendation]


class LearningGoal(BaseModel):
    goal: str
    target_skill: str
    reason: str
    suggested_practice_type: str
    priority: int = Field(ge=0, le=100)
    success_metric: str


class AdaptiveLearningPath(BaseModel):
    learner_id: int
    current_level: str
    progress: float | None = None
    current_focus: str | None = None
    current_goal: str | None = None
    recommended_practice: LearnerRecommendation | None = None
    completed_skills: list[str]
    remaining_skills: list[str]
    goals: list[LearningGoal]


class DashboardInsights(BaseModel):
    learner_id: int
    current_level: str
    current_focus: str | None = None
    todays_recommendation: LearnerRecommendation | None = None
    strongest_skill: str | None = None
    weakest_skill: str | None = None
    practice_streak: int
    weekly_improvement: float | None = None
    ai_insight: str


class LearnerIntelligenceResponse(BaseModel):
    performance: LearnerPerformanceAnalysis
    weaknesses: LearnerWeaknesses
    strengths: LearnerStrengths
    recommendations: LearnerRecommendations
    learning_path: AdaptiveLearningPath
    dashboard_insights: DashboardInsights
