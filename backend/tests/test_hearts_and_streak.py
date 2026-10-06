from datetime import date, datetime, timedelta

import pytest

from app.errors import AppError
from app.models import UserStats
from app.models.learner import MAX_HEARTS
from app.services import hearts, streak

NOW = datetime(2026, 10, 7, 12, 0)
REGEN = timedelta(minutes=30)  # the default HEART_REGEN_MINUTES
TODAY = date(2026, 10, 7)


def make_stats(**overrides: object) -> UserStats:
    values: dict[str, object] = {
        "hearts": 2,
        "hearts_updated_at": NOW,
        "gems": 500,
        "current_streak": 3,
        "longest_streak": 3,
        "last_active_date": TODAY - timedelta(days=1),
    }
    values.update(overrides)
    return UserStats(**values)


def test_regen_adds_one_heart_per_interval_and_keeps_the_remainder() -> None:
    stats = make_stats(hearts_updated_at=NOW - 2 * REGEN - timedelta(minutes=10))
    assert hearts.apply_regen(stats, NOW)
    assert stats.hearts == 4
    # The 10 minutes already spent toward the next heart are not thrown away.
    assert hearts.next_heart_at(stats) == NOW + timedelta(minutes=20)


def test_regen_caps_at_the_maximum() -> None:
    stats = make_stats(hearts=4, hearts_updated_at=NOW - 10 * REGEN)
    hearts.apply_regen(stats, NOW)
    assert stats.hearts == MAX_HEARTS and hearts.next_heart_at(stats) is None


def test_no_regen_before_a_full_interval() -> None:
    stats = make_stats(hearts_updated_at=NOW - REGEN + timedelta(seconds=1))
    assert not hearts.apply_regen(stats, NOW) and stats.hearts == 2


def test_losing_the_first_heart_starts_the_countdown() -> None:
    stats = make_stats(hearts=MAX_HEARTS, hearts_updated_at=NOW - timedelta(days=3))
    hearts.lose_heart(stats, NOW)
    assert stats.hearts == MAX_HEARTS - 1 and stats.hearts_updated_at == NOW


def test_refill_spends_gems() -> None:
    stats = make_stats(hearts=0, gems=400)
    hearts.refill(stats, NOW)
    assert (stats.hearts, stats.gems) == (MAX_HEARTS, 400 - hearts.REFILL_COST_GEMS)


@pytest.mark.parametrize(
    ("hearts_left", "gems", "code"),
    [(0, hearts.REFILL_COST_GEMS - 1, "NOT_ENOUGH_GEMS"), (MAX_HEARTS, 1000, "HEARTS_FULL")],
)
def test_refill_refusals(hearts_left: int, gems: int, code: str) -> None:
    with pytest.raises(AppError) as raised:
        hearts.refill(make_stats(hearts=hearts_left, gems=gems), NOW)
    assert raised.value.code == code


def test_streak_extends_after_yesterday() -> None:
    stats = make_stats()
    result = streak.record_lesson_day(stats, TODAY)
    assert (result.count, result.extended) == (4, True)
    assert stats.longest_streak == 4 and stats.last_active_date == TODAY


def test_streak_keeps_on_a_second_lesson_the_same_day() -> None:
    stats = make_stats(last_active_date=TODAY)
    result = streak.record_lesson_day(stats, TODAY)
    assert (result.count, result.extended) == (3, False)


def test_streak_restarts_after_a_missed_day_and_keeps_the_record() -> None:
    stats = make_stats(
        current_streak=8, longest_streak=8, last_active_date=TODAY - timedelta(days=2)
    )
    result = streak.record_lesson_day(stats, TODAY)
    assert (result.count, stats.longest_streak) == (1, 8)


def test_streak_expires_on_read_only_after_a_full_missed_day() -> None:
    alive = make_stats(last_active_date=TODAY - timedelta(days=1))
    assert not streak.expire_if_broken(alive, TODAY) and alive.current_streak == 3
    broken = make_stats(last_active_date=TODAY - timedelta(days=2))
    assert streak.expire_if_broken(broken, TODAY) and broken.current_streak == 0
