from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CorrectionState(Base):
    __tablename__ = "correction_states"

    __table_args__ = (
        UniqueConstraint(
            "attempt_id",
            "error_index",
            name="uq_attempt_error_state",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    attempt_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("practice_attempts.id"),
        nullable=False,
        index=True,
    )

    error_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    target_category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    current_hint_level: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    retry_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="active",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )