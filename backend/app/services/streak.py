"""Streak rules: extend, keep or restart on a finished lesson; expire on read."""

from datetime import date, timedelta

from app.models import UserStats
from app.schemas.attempt_result import StreakResult


def expire_if_broken(stats: UserStats, today: date) -> bool:
    """Zero the streak once a whole day has passed with no lesson; True if it changed.

    A streak survives until the end of the day after the last active day, so missing
    only today does not break it yet.
    """
    if stats.current_streak == 0 or stats.last_active_date is None:
        return False
    if stats.last_active_date >= today - timedelta(days=1):
        return False
    stats.current_streak = 0
    return True


def is_active_today(stats: UserStats, today: date) -> bool:
    return stats.last_active_date == today


def record_lesson_day(stats: UserStats, today: date) -> StreakResult:
    """Count today toward the streak; `extended` is True only on the day's first lesson."""
    if stats.last_active_date == today:
        return StreakResult(count=stats.current_streak, extended=False)
    if stats.last_active_date == today - timedelta(days=1):
        stats.current_streak += 1
    else:
        stats.current_streak = 1
    stats.longest_streak = max(stats.longest_streak, stats.current_streak)
    stats.last_active_date = today
    return StreakResult(count=stats.current_streak, extended=True)
