from pydantic import BaseModel, Field


class ListeningQuestion(BaseModel):
    id: int
    question: str
    options: list[str]


class ListeningPracticeResponse(BaseModel):
    practice_id: str
    audio_url: str
    transcript: str
    estimated_minutes: int
    questions: list[ListeningQuestion]


class ListeningSubmissionRequest(BaseModel):
    learner_id: int | None = Field(default=None, gt=0)
    practice_id: str = Field(min_length=1)
    answers: dict[int, str]


class ListeningSubmissionResponse(BaseModel):
    attempt_id: int
    score: int
    correct_answers: dict[int, str]
    explanations: dict[int, str]
    feedback: str
    ai_feedback: str
    user_answers: dict[int, str]
    transcript: str
    audio_url: str
