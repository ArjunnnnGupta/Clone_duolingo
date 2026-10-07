"""The learner's top-bar data, profile and settings."""

import datetime as dt

from pydantic import BaseModel, Field, field_validator

from app.models.learner import DAILY_GOAL_OPTIONS


class UserOut(BaseModel):
    id: int
    username: str
    display_name: str
    avatar_color: str
    daily_goal_xp: int
    joined_at: dt.date


class StatsOut(BaseModel):
    total_xp: int
    gems: int
    hearts: int
    max_hearts: int
    next_heart_at: dt.datetime | None
    # What the browser counts down: next_heart_at is learner-local wall time (and shifted by the
    # dev-tools day offset), so it cannot be compared with the browser's own clock.
    seconds_until_next_heart: int | None
    refill_cost_gems: int
    current_streak: int
    longest_streak: int
    streak_active_today: bool


class DailyOut(BaseModel):
    goal_xp: int
    today_xp: int


class DayActivityOut(BaseModel):
    date: dt.date
    is_active: bool  # at least one lesson finished that day


class MeResponse(BaseModel):
    user: UserOut
    stats: StatsOut
    daily: DailyOut
    recent_days: list[DayActivityOut]  # the last 7 days, oldest first, ending today


class AchievementOut(BaseModel):
    code: str
    title: str
    description: str
    icon: str
    threshold: int
    progress: int  # current metric value, capped at the threshold
    unlocked_at: dt.datetime | None


class CourseProgressOut(BaseModel):
    skills_completed: int
    skills_total: int


class DayXp(BaseModel):
    date: dt.date
    xp: int


class ProfileResponse(BaseModel):
    user: UserOut
    stats: StatsOut
    achievements: list[AchievementOut]
    course_progress: CourseProgressOut
    week_xp: list[DayXp]


class SettingsUpdate(BaseModel):
    daily_goal_xp: int | None = None
    display_name: str | None = Field(default=None, min_length=1, max_length=40)

    @field_validator("display_name", mode="before")
    @classmethod
    def _strip_display_name(cls, name: object) -> object:
        # Before the length check, so a name of only spaces is rejected instead of saved.
        return name.strip() if isinstance(name, str) else name

    @field_validator("daily_goal_xp")
    @classmethod
    def _goal_is_an_option(cls, goal: int | None) -> int | None:
        if goal is not None and goal not in DAILY_GOAL_OPTIONS:
            raise ValueError(f"daily_goal_xp must be one of {DAILY_GOAL_OPTIONS}")
        return goal
