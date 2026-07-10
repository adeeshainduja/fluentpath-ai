from pydantic import BaseModel


class RetryEvaluationResult(BaseModel):
    target_category: str
    resolved: bool
    improved: bool
    feedback: str
    next_action: str