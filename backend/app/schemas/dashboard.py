from pydantic import BaseModel


class DashboardSummary(BaseModel):
    overall_score: float
    average_score: float
    completed_tasks: int
    pending_tasks: int
    learning_trend: str
    recommended_skill: str
    recommended_strategy: str