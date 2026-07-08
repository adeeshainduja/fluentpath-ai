from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.practice_attempt import PracticeAttempt
from app.schemas.practice import PracticeAttemptCreate


router = APIRouter(
    prefix="/api/v1/practice",
    tags=["Practice"],
)


@router.post("/writing")
def create_writing_attempt(
    attempt: PracticeAttemptCreate,
    db: Session = Depends(get_db),
):
    new_attempt = PracticeAttempt(
        text=attempt.text,
        practice_type="writing",
    )

    db.add(new_attempt)
    db.commit()
    db.refresh(new_attempt)

    return {
        "id": new_attempt.id,
        "text": new_attempt.text,
        "practice_type": new_attempt.practice_type,
        "message": "Practice attempt saved successfully",
    }