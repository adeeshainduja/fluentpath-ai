from pydantic import BaseModel


class AdaptivePracticeRecommendation(BaseModel):
    recommendedPractice: str
    difficulty: str
    reason: str
    estimatedTime: str
    priority: str
