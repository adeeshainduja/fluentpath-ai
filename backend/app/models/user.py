from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    func,
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False, index=True)

    password_hash = Column(String(255), nullable=False)

    profile_photo_url = Column(String(500), nullable=True)

    english_level = Column(
        String(30),
        nullable=False,
        default="Beginner",
    )

    target_goal = Column(
        String(255),
        nullable=False,
        default="Improve English communication",
    )

    daily_goal = Column(
        Integer,
        nullable=False,
        default=15,
    )

    role = Column(
        String(30),
        nullable=False,
        default="student",
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    last_login = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    practice_attempts = relationship(
        "PracticeAttempt",
        back_populates="user",
    )

    speaking_attempts = relationship(
        "SpeakingAttempt",
        back_populates="user",
    )
