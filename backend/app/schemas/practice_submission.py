from pydantic import BaseModel


class PracticeSubmissionRequest(BaseModel):
    answer: str


class PracticeSubmissionResponse(BaseModel):
    score: float
    feedback: str
    grammar_score: float
    vocabulary_score: float
    fluency_score: float
    pronunciation_score: float | None = None
    suggestions: list[str] = []