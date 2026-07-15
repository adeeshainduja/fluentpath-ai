from pydantic import BaseModel


class SpeakingSubmission(BaseModel):
    learner_id: int
    transcript: str


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
    confidence_score: int

    grammar_feedback: str
    vocabulary_feedback: str
    fluency_feedback: str
    overall_feedback: str


class SpeakingResponse(BaseModel):
    transcript: str
    pronunciation: PronunciationResult
    evaluation: SpeakingEvaluation
    coach_message: str