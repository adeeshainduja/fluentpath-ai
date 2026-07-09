from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.hint_service import get_hint


router = APIRouter(
    prefix="/api/v1/hints",
    tags=["Hints"],
)


@router.get(
    "/attempts/{attempt_id}/errors/{error_index}"
)
def request_hint(
    attempt_id: int,
    error_index: int,
    level: int = 1,
    db: Session = Depends(get_db),
):

    if level not in [1, 2, 3]:
        raise HTTPException(
            status_code=400,
            detail="Hint level must be 1, 2, or 3",
        )

    result = get_hint(
        db=db,
        attempt_id=attempt_id,
        error_index=error_index,
        hint_level=level,
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