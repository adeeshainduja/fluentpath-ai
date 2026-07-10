from pydantic import BaseModel


class TaskEvaluationRequest(BaseModel):
    task_instruction: str
    target_skill: str


class TaskEvaluationResult(BaseModel):
    task_completed: bool
    relevant: bool
    sufficient_detail: bool
    target_skill_practiced: bool
    score: int
    feedback: str
    next_action: str