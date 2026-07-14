from pydantic import BaseModel


class PracticeSubmissionResponse(BaseModel):
    score: int
    feedback: str

    grammar_score: int
    vocabulary_score: int
    fluency_score: int
    pronunciation_score: int | None = None

    suggestions: list[str]