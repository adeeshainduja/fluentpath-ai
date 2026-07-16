from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.auth import (
    ProfileUpdateRequest,
    RegisterRequest,
    UserResponse,
    TokenResponse,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_access_token,
)

from datetime import datetime, UTC


class AuthService:

    @staticmethod
    def register_user(
        db: Session,
        request: RegisterRequest,
    ) -> UserResponse:

        existing_user = (
            db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists.",
            )

        user = User(
            full_name=request.full_name,
            email=request.email,
            password_hash=hash_password(
                request.password
            ),
            role="student",
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return UserResponse.model_validate(user)

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str,
    ) -> TokenResponse:

        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if not user:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not verify_password(
            password,
            user.password_hash,
        ):

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not user.is_active:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive.",
            )

        user.last_login = datetime.now(UTC)

        db.commit()

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )
        refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return TokenResponse(
            access_token=token,
            refresh_token=refresh_token,
            user=UserResponse.model_validate(user),
        )

    @staticmethod
    def refresh(
        db: Session,
        refresh_token: str,
    ) -> TokenResponse:
        payload = decode_access_token(refresh_token)

        if payload is None or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
            )

        user_id = payload.get("sub")

        try:
            parsed_user_id = int(user_id)
        except (TypeError, ValueError) as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
            ) from exc

        user = AuthService.get_user_by_id(
            db=db,
            user_id=parsed_user_id,
        )

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
            )

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )
        new_refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            user=UserResponse.model_validate(user),
        )

    @staticmethod
    def update_profile(
        db: Session,
        user: User,
        request: ProfileUpdateRequest,
    ) -> UserResponse:
        updates = request.model_dump(
            exclude_unset=True,
        )

        for field, value in updates.items():
            setattr(user, field, value)

        db.add(user)
        db.commit()
        db.refresh(user)

        return UserResponse.model_validate(user)

    @staticmethod
    def get_user_by_id(
        db: Session,
        user_id: int,
    ) -> User | None:

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def get_user_by_email(
        db: Session,
        email: str,
    ) -> User | None:

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )
