
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import get_dashboard_data

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
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