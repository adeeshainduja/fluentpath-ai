from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.hint_service import get_next_hint


router = APIRouter(
    prefix="/api/v1/hints",
    tags=["Hints"],
)


@router.get(
    "/attempts/{attempt_id}/errors/{error_index}/next"
)
def request_next_hint(
    attempt_id: int,
    error_index: int,
    db: Session = Depends(get_db),
):

    result = get_next_hint(
        db=db,
        attempt_id=attempt_id,
        error_index=error_index,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Practice attempt not found",
        )

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )

    return result