"""The only place that reads the system time; everything else asks this module."""

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.models import AppSetting, User
from app.models.learner import DEFAULT_TIMEZONE

DAY_OFFSET_KEY = "day_offset"


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


def get_day_offset(db: Session) -> int:
    setting = db.get(AppSetting, DAY_OFFSET_KEY)
    return int(setting.value) if setting else 0


def user_now(db: Session, user: User) -> datetime:
    """The learner's local time, including any simulated days from dev tools.

    Streaks, the daily goal, the leaderboard week and heart regen all read this, so
    advancing the day moves every one of them together.
    """
    return now(user.timezone, get_day_offset(db))


def user_today(db: Session, user: User) -> date:
    return user_now(db, user).date()
