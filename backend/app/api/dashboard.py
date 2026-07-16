
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import get_dashboard_data

router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "",
    response_model=DashboardResponse,
)
def current_user_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_dashboard_data(
        db=db,
        learner_id=current_user.id,
    )


@router.get(
    "/{learner_id}",
    response_model=DashboardResponse,
)
def dashboard(
    learner_id: int,
    db: Session = Depends(get_db),
):
    return get_dashboard_data(
        db=db,
        learner_id=learner_id,
    )
