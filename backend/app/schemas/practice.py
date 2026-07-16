from pydantic import BaseModel, Field


class PracticeAttemptCreate(BaseModel):
    learner_id: int | None = Field(default=None, gt=0)
    text: str = Field(min_length=1)


class RetryAttemptCreate(BaseModel):
    text: str = Field(min_length=1)


class DetectedError(BaseModel):
    error_type: str
    category: str
    problem_text: str
    explanation: str
    hint: str


class WritingAnalysisResult(BaseModel):
    has_errors: bool
    errors: list[DetectedError]
    instruction: str
