from pydantic import BaseModel


class PracticeAttemptCreate(BaseModel):
    text: str