from pydantic import BaseModel


class PracticeAttemptCreate(BaseModel):
    text: str


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

class RetryAttemptCreate(BaseModel):
    text: str