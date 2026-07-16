from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class WritingEvaluation(Base):
    __tablename__ = "writing_evaluations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    attempt_id: Mapped[int | None] = mapped_column(
        ForeignKey("practice_attempts.id"),
        nullable=True,
        index=True,
    )
    submitted_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    result: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


class SpeakingEvaluation(Base):
    __tablename__ = "speaking_evaluations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    speaking_attempt_id: Mapped[int | None] = mapped_column(
        ForeignKey("speaking_attempts.id"),
        nullable=True,
        index=True,
    )
    transcript: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    result: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


class ListeningEvaluation(Base):
    __tablename__ = "listening_evaluations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    prompt: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    response: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    result: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


class VocabularyProgress(Base):
    __tablename__ = "vocabulary_progress"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    word: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )
    mastery_level: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    times_practiced: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    last_practiced_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )


class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    earned_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
