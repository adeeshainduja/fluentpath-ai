from fastapi import APIRouter

from app.schemas.practice import PracticeAttemptCreate


router = APIRouter(
    prefix="/api/v1/practice",
    tags=["Practice"],
)


@router.post("/writing")
def create_writing_attempt(attempt: PracticeAttemptCreate):
    return {
        "text": attempt.text,
        "message": "Practice attempt received successfully",
    }