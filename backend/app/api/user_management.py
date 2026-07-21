from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    ProfileUpdateRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.schemas.practice_history import PracticeHistoryResponse
from app.services.auth_service import AuthService
from app.services.practice_history_service import get_practice_history


router = APIRouter(
    prefix="/api/v1",
    tags=["User Management"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    return AuthService.register_user(
        db=db,
        request=request,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    return AuthService.login(
        db=db,
        email=request.email,
        password=request.password,
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh(
    request: RefreshRequest,
    db: Session = Depends(get_db),
):
    return AuthService.refresh(
        db=db,
        refresh_token=request.refresh_token,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.put(
    "/profile",
    response_model=UserResponse,
)
def update_profile(
    request: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return AuthService.update_profile(
        db=db,
        user=current_user,
        request=request,
    )


@router.get(
    "/history",
    response_model=PracticeHistoryResponse,
)
def history(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
    ),
    type: str = Query(default="all"),
    sort: str = Query(default="newest"),
    search: str | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_practice_history(
        db=db,
        learner_id=current_user.id,
        page=page,
        limit=limit,
        practice_type=type,  # compatibility endpoint
        sort=sort,
        search=search,
    )
