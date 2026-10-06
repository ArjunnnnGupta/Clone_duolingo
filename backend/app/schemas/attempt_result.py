"""What finalizing a lesson produced; stored as JSON on lesson_attempts.result."""

from pydantic import BaseModel


class StreakResult(BaseModel):
    count: int
    extended: bool


class DailyGoalResult(BaseModel):
    today_xp: int
    goal_xp: int
    just_met: bool


class AchievementUnlock(BaseModel):
    code: str
    title: str
    icon: str


class AttemptResult(BaseModel):
    xp_earned: int
    # Whole percent: exercises / (exercises + mistakes), so a flawless lesson is 100.
    accuracy: int
    mistakes: int
    duration_s: int
    streak: StreakResult
    daily_goal: DailyGoalResult
    skill_completed: bool
    achievements_unlocked: list[AchievementUnlock]
