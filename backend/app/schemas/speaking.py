from pydantic import BaseModel, Field


class SpeakingSubmission(BaseModel):
    learner_id: int = Field(gt=0)
    transcript: str = Field(min_length=1)


class PronunciationResult(BaseModel):
    score: int
    fluency: int
    confidence: int
    pronunciation: int
    comments: list[str]


class SpeakingEvaluation(BaseModel):
    grammar_score: int
    vocabulary_score: int
    fluency_score: int
    pronunciation_score: int
    confidence_score: int

    grammar_feedback: str
    vocabulary_feedback: str
    pronunciation_feedback: str
    fluency_feedback: str
    overall_feedback: str
    suggestions: list[str] = Field(default_factory=list)


class SpeakingResponse(BaseModel):
    attempt_id: int
    transcript: str
    pronunciation: PronunciationResult
    evaluation: SpeakingEvaluation
    coach_message: str
