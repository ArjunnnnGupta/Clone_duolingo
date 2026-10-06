"""Lesson history: one attempt per lesson run, one answer row per submitted check."""

from datetime import datetime
from typing import Any

from sqlalchemy import CheckConstraint, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, sql_in_list
from app.models.content import Exercise, Lesson
from app.models.learner import User

ATTEMPT_MODES = ("learn", "practice")
ATTEMPT_STATUSES = ("in_progress", "completed", "failed", "abandoned")


class LessonAttempt(Base):
    __tablename__ = "lesson_attempts"
    __table_args__ = (
        CheckConstraint(f"mode IN ({sql_in_list(ATTEMPT_MODES)})", name="mode_valid"),
        CheckConstraint(f"status IN ({sql_in_list(ATTEMPT_STATUSES)})", name="status_valid"),
        # Serves "find this user's in-progress attempt" on every lesson start.
        Index("ix_lesson_attempts_user_id_status", "user_id", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    mode: Mapped[str]
    status: Mapped[str] = mapped_column(default="in_progress")
    mistakes: Mapped[int] = mapped_column(default=0)
    xp_earned: Mapped[int] = mapped_column(default=0)
    started_at: Mapped[datetime]
    finished_at: Mapped[datetime | None]

    user: Mapped[User] = relationship(back_populates="attempts")
    lesson: Mapped[Lesson] = relationship()
    answers: Mapped[list["AttemptAnswer"]] = relationship(
        back_populates="attempt",
        order_by="AttemptAnswer.id",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class AttemptAnswer(Base):
    __tablename__ = "attempt_answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    attempt_id: Mapped[int] = mapped_column(
        ForeignKey("lesson_attempts.id", ondelete="CASCADE"), index=True
    )
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"))
    submitted: Mapped[dict[str, Any]]
    is_correct: Mapped[bool]
    answered_at: Mapped[datetime]

    attempt: Mapped[LessonAttempt] = relationship(back_populates="answers")
    exercise: Mapped[Exercise] = relationship()
