"""Achievements: measure each metric, unlock newly crossed thresholds, list with progress."""

from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Achievement, LessonAttempt, User, UserAchievement, UserSkillProgress
from app.schemas.me import AchievementOut


def metric_values(db: Session, user: User) -> dict[str, int]:
    """Current value of every metric an achievement can use (see ACHIEVEMENT_METRICS)."""
    # Flush so counts include the attempt and progress the current request just changed.
    db.flush()
    completed_attempts = select(func.count()).where(
        LessonAttempt.user_id == user.id, LessonAttempt.status == "completed"
    )
    completed_skills = select(func.count()).where(
        UserSkillProgress.user_id == user.id, UserSkillProgress.completed_at.is_not(None)
    )
    return {
        "total_xp": user.stats.total_xp,
        "streak": user.stats.current_streak,
        "lessons": db.scalar(completed_attempts) or 0,
        "perfect_lessons": db.scalar(completed_attempts.where(LessonAttempt.mistakes == 0)) or 0,
        "skills": db.scalar(completed_skills) or 0,
    }


def unlock_new(db: Session, user: User, now: datetime) -> list[Achievement]:
    """Award every achievement whose threshold is now met and that the learner lacks."""
    values = metric_values(db, user)
    owned_ids = {owned.achievement_id for owned in user.achievements}
    newly_unlocked = [
        achievement
        for achievement in db.scalars(select(Achievement).order_by(Achievement.id))
        if achievement.id not in owned_ids and values[achievement.metric] >= achievement.threshold
    ]
    for achievement in newly_unlocked:
        db.add(UserAchievement(user=user, achievement=achievement, unlocked_at=now))
    return newly_unlocked


def list_achievements(db: Session, user: User) -> list[AchievementOut]:
    values = metric_values(db, user)
    unlocked_at = {owned.achievement_id: owned.unlocked_at for owned in user.achievements}
    return [
        AchievementOut(
            code=achievement.code,
            title=achievement.title,
            description=achievement.description,
            icon=achievement.icon,
            threshold=achievement.threshold,
            progress=min(values[achievement.metric], achievement.threshold),
            unlocked_at=unlocked_at.get(achievement.id),
        )
        for achievement in db.scalars(select(Achievement).order_by(Achievement.id))
    ]
