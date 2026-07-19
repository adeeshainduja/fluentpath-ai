from pydantic import BaseModel, Field


class VocabularyQuestion(BaseModel):
    id: int
    word: str
    question: str
    options: list[str]


class VocabularyPracticeResponse(BaseModel):
    session_id: int = Field(alias="sessionId")
    difficulty: str
    questions: list[VocabularyQuestion]

    class Config:
        populate_by_name = True


class VocabularyAnswer(BaseModel):
    question_id: int = Field(alias="questionId")
    selected_option: str = Field(alias="selectedOption")

    class Config:
        populate_by_name = True


class VocabularySubmissionRequest(BaseModel):
    session_id: int = Field(alias="sessionId", gt=0)
    answers: list[VocabularyAnswer]

    class Config:
        populate_by_name = True


class VocabularySubmissionResponse(BaseModel):
    score: int
    correct_answers: dict[int, str] = Field(alias="correctAnswers")
    explanations: dict[int, str]
    feedback: str

    class Config:
        populate_by_name = True
