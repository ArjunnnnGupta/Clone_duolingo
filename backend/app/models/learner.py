"""Learner state: identity, counters, per-skill progress, daily activity, achievements."""

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, sql_in_list
from app.models.content import Course, Skill

if TYPE_CHECKING:
    from app.models.history import LessonAttempt

DAILY_GOAL_OPTIONS = (10, 20, 30, 50)
DEFAULT_DAILY_GOAL_XP = 20
DEFAULT_TIMEZONE = "Asia/Kolkata"
MAX_HEARTS = 5
ACHIEVEMENT_METRICS = ("total_xp", "streak", "lessons", "skills", "perfect_lessons")


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            f"daily_goal_xp IN ({sql_in_list(DAILY_GOAL_OPTIONS)})", name="daily_goal_xp_valid"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    display_name: Mapped[str]
    avatar_color: Mapped[str]
    timezone: Mapped[str] = mapped_column(default=DEFAULT_TIMEZONE, server_default=DEFAULT_TIMEZONE)
    daily_goal_xp: Mapped[int] = mapped_column(
        default=DEFAULT_DAILY_GOAL_XP, server_default=text(str(DEFAULT_DAILY_GOAL_XP))
    )
    current_course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    created_at: Mapped[datetime]

    current_course: Mapped[Course] = relationship()
    stats: Mapped["UserStats"] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )
    skill_progress: Mapped[list["UserSkillProgress"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )
    daily_activity: Mapped[list["DailyActivity"]] = relationship(
        back_populates="user",
        order_by="DailyActivity.activity_date",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    achievements: Mapped[list["UserAchievement"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )
    attempts: Mapped[list["LessonAttempt"]] = relationship(back_populates="user")


class UserStats(Base):
    """Counters that change every lesson, split from users to keep identity rows cold."""

    __tablename__ = "user_stats"
    __table_args__ = (
        CheckConstraint(f"hearts BETWEEN 0 AND {MAX_HEARTS}", name="hearts_range"),
        CheckConstraint("total_xp >= 0", name="total_xp_non_negative"),
        CheckConstraint("gems >= 0", name="gems_non_negative"),
        CheckConstraint("current_streak >= 0", name="current_streak_non_negative"),
        CheckConstraint("longest_streak >= 0", name="longest_streak_non_negative"),
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    # Denormalized SUM(daily_activity.xp_earned), updated in the same transaction as each award.
    total_xp: Mapped[int] = mapped_column(default=0)
    gems: Mapped[int] = mapped_column(default=0)
    hearts: Mapped[int] = mapped_column(default=MAX_HEARTS)
    # Anchor for lazy regeneration: hearts are recomputed from elapsed time on read.
    hearts_updated_at: Mapped[datetime]
    current_streak: Mapped[int] = mapped_column(default=0)
    longest_streak: Mapped[int] = mapped_column(default=0)
    last_active_date: Mapped[date | None]

    user: Mapped[User] = relationship(back_populates="stats")


class UserSkillProgress(Base):
    __tablename__ = "user_skill_progress"
    __table_args__ = (
        CheckConstraint("lessons_completed >= 0", name="lessons_completed_non_negative"),
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True
    )
    lessons_completed: Mapped[int] = mapped_column(default=0)
    completed_at: Mapped[datetime | None]
    updated_at: Mapped[datetime]

    user: Mapped[User] = relationship(back_populates="skill_progress")
    skill: Mapped[Skill] = relationship()


class DailyActivity(Base):
    __tablename__ = "daily_activity"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    activity_date: Mapped[date] = mapped_column(primary_key=True)
    xp_earned: Mapped[int] = mapped_column(default=0)
    lessons_completed: Mapped[int] = mapped_column(default=0)

    user: Mapped[User] = relationship(back_populates="daily_activity")


class Achievement(Base):
    __tablename__ = "achievements"
    __table_args__ = (
        CheckConstraint(f"metric IN ({sql_in_list(ACHIEVEMENT_METRICS)})", name="metric_valid"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str]
    description: Mapped[str]
    icon: Mapped[str]
    metric: Mapped[str]
    threshold: Mapped[int]


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    achievement_id: Mapped[int] = mapped_column(
        ForeignKey("achievements.id", ondelete="CASCADE"), primary_key=True
    )
    unlocked_at: Mapped[datetime]

    user: Mapped[User] = relationship(back_populates="achievements")
    achievement: Mapped[Achievement] = relationship()


class AppSetting(Base):
    """Key/value store; holds `day_offset` for the simulated clock."""

    __tablename__ = "app_settings"

    key: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str]
