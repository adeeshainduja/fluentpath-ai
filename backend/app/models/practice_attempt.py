from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PracticeAttempt(Base):
    __tablename__ = "practice_attempts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    text: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    practice_type: Mapped[str] = mapped_column(
        String(50),
        default="writing",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )