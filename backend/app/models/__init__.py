"""Importing this package registers all 14 tables on Base.metadata."""

from app.models.base import Base
from app.models.content import Course, Exercise, Lesson, Skill, Unit
from app.models.history import AttemptAnswer, LessonAttempt
from app.models.learner import (
    Achievement,
    AppSetting,
    DailyActivity,
    User,
    UserAchievement,
    UserSkillProgress,
    UserStats,
)

__all__ = [
    "Achievement",
    "AppSetting",
    "AttemptAnswer",
    "Base",
    "Course",
    "DailyActivity",
    "Exercise",
    "Lesson",
    "LessonAttempt",
    "Skill",
    "Unit",
    "User",
    "UserAchievement",
    "UserSkillProgress",
    "UserStats",
]
