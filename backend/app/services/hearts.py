"""Heart rules: lazy regeneration, losing a heart, gem refills and the practice mock.

These work on a UserStats row and never commit; the calling service owns the transaction.
"""

import math
from datetime import datetime, timedelta

from app.config import get_settings
from app.errors import AppError
from app.models import UserStats
from app.models.learner import MAX_HEARTS

REFILL_COST_GEMS = 350


def _regen_interval() -> timedelta:
    return timedelta(minutes=get_settings().heart_regen_minutes)


def apply_regen(stats: UserStats, now: datetime) -> bool:
    """Add the hearts earned since `hearts_updated_at`; returns True if anything changed.

    Regeneration is computed on read instead of by a background job, so a tab left open
    overnight still shows the right count the next time it asks.
    """
    if stats.hearts >= MAX_HEARTS:
        return False
    interval = _regen_interval()
    earned = (now - stats.hearts_updated_at) // interval
    if earned <= 0:
        return False
    if stats.hearts + earned >= MAX_HEARTS:
        stats.hearts = MAX_HEARTS
        stats.hearts_updated_at = now
    else:
        stats.hearts += earned
        # Advance by whole intervals only, so time already counted toward the next heart is kept.
        stats.hearts_updated_at += interval * earned
    return True


def lose_heart(stats: UserStats, now: datetime) -> None:
    """Take one heart; call apply_regen first so the count is current."""
    if stats.hearts == MAX_HEARTS:
        # Hearts only regenerate below the cap, so the countdown starts at the first loss.
        stats.hearts_updated_at = now
    stats.hearts = max(0, stats.hearts - 1)


def next_heart_at(stats: UserStats) -> datetime | None:
    if stats.hearts >= MAX_HEARTS:
        return None
    return stats.hearts_updated_at + _regen_interval()


def seconds_until_next_heart(stats: UserStats, now: datetime) -> int | None:
    """Whole seconds until the next heart, measured on the same clock as `now`.

    Rounded up: truncating would report 0 while a fraction of a second is still left and the
    heart has not regenerated yet, so a client refetching at 0 would get 0 back again.
    """
    next_at = next_heart_at(stats)
    if next_at is None:
        return None
    return max(0, math.ceil((next_at - now).total_seconds()))


def refill(stats: UserStats, now: datetime) -> None:
    """Buy a full set of hearts with gems."""
    if stats.hearts >= MAX_HEARTS:
        raise AppError("HEARTS_FULL", "Your hearts are already full.", 409)
    if stats.gems < REFILL_COST_GEMS:
        raise AppError("NOT_ENOUGH_GEMS", f"A refill costs {REFILL_COST_GEMS} gems.", 409)
    stats.gems -= REFILL_COST_GEMS
    stats.hearts = MAX_HEARTS
    stats.hearts_updated_at = now


def add_practice_heart(stats: UserStats, now: datetime) -> None:
    """Mock of "practice to earn hearts": one free heart, capped at the maximum."""
    stats.hearts = min(MAX_HEARTS, stats.hearts + 1)
    if stats.hearts == MAX_HEARTS:
        stats.hearts_updated_at = now
