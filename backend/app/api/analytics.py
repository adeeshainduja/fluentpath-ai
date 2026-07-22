from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.analytics import AnalyticsResponse
from app.models.user import User
from app.services.analytics_service import get_user_analytics


router = APIRouter(
    prefix="/api/v1/analytics",
    tags=["Analytics"],
)


@router.get("", response_model=AnalyticsResponse)
def current_user_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_user_analytics(
        db=db,
        learner_id=current_user.id,
    )
