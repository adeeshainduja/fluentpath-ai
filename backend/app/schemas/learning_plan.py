from pydantic import BaseModel


class LearningRecommendation(BaseModel):
    priority_category: str
    practice_type: str
    difficulty: str
    title: str
    instruction: str
    reason: str


class LearningPlanResult(BaseModel):
    learner_id: int
    has_recommendation: bool
    recommendation: LearningRecommendation | None