from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.database import Base


class SpeakingAttempt(Base):
    __tablename__ = "speaking_attempts"

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

    transcript: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    grammar_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    vocabulary_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    fluency_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    pronunciation_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    confidence_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    overall_feedback: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    user = relationship(
        "User",
        back_populates="speaking_attempts",
    )
