"""Course content: course -> unit -> skill -> lesson -> exercise."""

from typing import Any

from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, sql_in_list

EXERCISE_TYPES = ("multiple_choice", "translate", "match_pairs", "fill_blank", "type_answer")
DEFAULT_LESSON_XP = 10


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str]
    learning_language: Mapped[str]
    from_language: Mapped[str]

    units: Mapped[list["Unit"]] = relationship(
        back_populates="course",
        order_by="Unit.position",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Unit(Base):
    __tablename__ = "units"
    __table_args__ = (UniqueConstraint("course_id", "position"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"))
    position: Mapped[int]
    title: Mapped[str]
    description: Mapped[str]
    color: Mapped[str]

    course: Mapped[Course] = relationship(back_populates="units")
    skills: Mapped[list["Skill"]] = relationship(
        back_populates="unit",
        order_by="Skill.position",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Skill(Base):
    __tablename__ = "skills"
    __table_args__ = (UniqueConstraint("unit_id", "position"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id", ondelete="CASCADE"))
    position: Mapped[int]
    title: Mapped[str]
    icon: Mapped[str]

    unit: Mapped[Unit] = relationship(back_populates="skills")
    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="skill",
        order_by="Lesson.position",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Lesson(Base):
    __tablename__ = "lessons"
    __table_args__ = (
        UniqueConstraint("skill_id", "position"),
        CheckConstraint("xp_reward > 0", name="xp_reward_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id", ondelete="CASCADE"))
    position: Mapped[int]
    xp_reward: Mapped[int] = mapped_column(
        default=DEFAULT_LESSON_XP, server_default=text(str(DEFAULT_LESSON_XP))
    )

    skill: Mapped[Skill] = relationship(back_populates="lessons")
    exercises: Mapped[list["Exercise"]] = relationship(
        back_populates="lesson",
        order_by="Exercise.position",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Exercise(Base):
    __tablename__ = "exercises"
    __table_args__ = (
        UniqueConstraint("lesson_id", "position"),
        CheckConstraint(f"type IN ({sql_in_list(EXERCISE_TYPES)})", name="type_valid"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"))
    position: Mapped[int]
    type: Mapped[str]
    prompt: Mapped[str]
    # Type-specific shapes, validated by the Pydantic exercise union. Nothing queries inside them.
    payload: Mapped[dict[str, Any]]
    # Kept apart from payload so the answer is never serialized to the client by accident.
    solution: Mapped[dict[str, Any]]

    lesson: Mapped[Lesson] = relationship(back_populates="exercises")
