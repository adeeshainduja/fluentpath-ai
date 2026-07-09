from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.retry_evaluation_service import (
    evaluate_retry_attempt,
)


router = APIRouter(
    prefix="/api/v1/evaluations",
    tags=["Evaluations"],
)


@router.post(
    "/attempts/{original_attempt_id}/retries/"
    "{retry_attempt_id}"
)
def evaluate_retry(
    original_attempt_id: int,
    retry_attempt_id: int,
    error_index: int = 0,
    db: Session = Depends(get_db),
):

    result = evaluate_retry_attempt(
        db=db,
        original_attempt_id=original_attempt_id,
        retry_attempt_id=retry_attempt_id,
        error_index=error_index,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Original or retry attempt not found",
        )

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )

    return result