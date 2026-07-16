from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str | None = Field(
        default=None,
        min_length=8,
        max_length=128,
    )

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(
        cls,
        confirm_password: str | None,
        info,
    ):
        if (
            confirm_password is not None
            and confirm_password != info.data.get("password")
        ):
            raise ValueError("Passwords do not match.")

        return confirm_password


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)


class RefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=1)


class ProfileUpdateRequest(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    profile_photo_url: str | None = Field(
        default=None,
        max_length=500,
    )
    english_level: str | None = Field(
        default=None,
        max_length=30,
    )
    target_goal: str | None = Field(
        default=None,
        max_length=255,
    )
    daily_goal: int | None = Field(
        default=None,
        ge=1,
        le=240,
    )


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    profile_photo_url: str | None = None
    english_level: str
    target_goal: str
    daily_goal: int
    role: str
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse
