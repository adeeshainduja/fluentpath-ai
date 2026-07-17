from pydantic import BaseModel, Field


class ReadingQuestion(BaseModel):
    id: int
    question: str
    options: list[str]


class ReadingPassage(BaseModel):
    title: str
    text: str


class ReadingPracticeResponse(BaseModel):
    passage_id: str
    passage: ReadingPassage
    estimated_minutes: int
    questions: list[ReadingQuestion]


class ReadingSubmissionRequest(BaseModel):
    learner_id: int | None = Field(default=None, gt=0)
    passage_id: str = Field(min_length=1)
    answers: dict[int, str]


class ReadingSubmissionResponse(BaseModel):
    attempt_id: int
    score: int
    correct_answers: dict[int, str]
    explanations: dict[int, str]
    feedback: str
    user_answers: dict[int, str]
