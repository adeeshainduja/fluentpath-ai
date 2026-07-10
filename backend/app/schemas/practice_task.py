from pydantic import BaseModel


class PracticeTaskCreate(BaseModel):
    learner_id: int


class PracticeTaskSubmission(BaseModel):
    text: str


class PracticeTaskResponse(BaseModel):
    id: int
    learner_id: int
    target_skill: str
    practice_type: str
    difficulty: str
    title: str
    instruction: str
    strategy: str | None = None
    status: str

    model_config = {
        "from_attributes": True
    }