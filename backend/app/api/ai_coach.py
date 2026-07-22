from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.ai_coach import AICoachChatRequest, AICoachChatResponse
from app.services.ai_coach_service import chat_with_coach


router = APIRouter(
    prefix="/api/v1/ai-coach",
    tags=["AI Coach"],
)


@router.post("/chat", response_model=AICoachChatResponse)
def chat(
    payload: AICoachChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return chat_with_coach(
        db=db,
        learner_id=current_user.id,
        message=payload.message,
    )
