"""The only place that reads the system time; everything else asks this module."""

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from app.models.learner import DEFAULT_TIMEZONE


def now(timezone: str = DEFAULT_TIMEZONE, day_offset: int = 0) -> datetime:
    """Local wall-clock time shifted by the dev-tools day offset.

    Naive on purpose: SQLite stores naive datetimes, so every column holds learner-local time.
    """
    local_now = datetime.now(ZoneInfo(timezone)).replace(tzinfo=None)
    return local_now + timedelta(days=day_offset)


def today(timezone: str = DEFAULT_TIMEZONE, day_offset: int = 0) -> date:
    return now(timezone, day_offset).date()


def week_start(day: date) -> date:
    """Leaderboard weeks run Monday to Sunday."""
    return day - timedelta(days=day.weekday())
