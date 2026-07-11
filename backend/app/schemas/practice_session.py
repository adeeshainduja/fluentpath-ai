from pydantic import BaseModel, Field


class SessionResponseSubmission(BaseModel):
    task_id: int

    text: str = Field(
        min_length=1,
        max_length=5000,
    )