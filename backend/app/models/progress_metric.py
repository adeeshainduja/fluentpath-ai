from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ProgressMetric(Base):
    __tablename__ = "progress_metrics"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    learner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    task_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("practice_tasks.id"),
        nullable=False,
        index=True,
    )

    attempt_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("practice_attempts.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    target_skill: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    task_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    grammar_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    vocabulary_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    fluency_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    pronunciation_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    response_length: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    relevant: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    sufficient_detail: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    target_skill_practiced: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
