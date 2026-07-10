from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.practice_strategy_service import (
    determine_practice_strategy,
)


router = APIRouter(
    prefix="/api/v1/practice-strategies",
    tags=["Practice Strategies"],
)


@router.get("/learners/{learner_id}/next")
def get_next_strategy(
    learner_id: int,
    db: Session = Depends(get_db),
):
    result = determine_practice_strategy(
        db=db,
        learner_id=learner_id,
    )

    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )

    return {
        "learner_id": learner_id,
        "strategy": result,
    }