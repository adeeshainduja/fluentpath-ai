from pydantic import BaseModel


class HintResult(BaseModel):
    attempt_id: int
    error_category: str
    hint_level: int
    hint: str
    instruction: str