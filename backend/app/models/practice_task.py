from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PracticeTask(Base):
    __tablename__ = "practice_tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    learner_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    target_skill: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    practice_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    difficulty: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    instruction: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    strategy: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )