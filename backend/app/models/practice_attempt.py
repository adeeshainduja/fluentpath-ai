from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    parent_attempt_id: Mapped[int | None] = mapped_column(
        ForeignKey("practice_attempts.id"),
        nullable=True,
    )

    attempt_number: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    learner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    task_id: Mapped[int | None] = mapped_column(
        ForeignKey("practice_tasks.id"),
        nullable=True,
        index=True,
    )

    user = relationship(
        "User",
        back_populates="practice_attempts",
    )
