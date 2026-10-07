"""The learner's own view: top-bar stats, profile page, settings, and the heart actions
whose response is that same view."""

from datetime import date, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import InstrumentedAttribute, Session

from app.models import DailyActivity, Skill, Unit, User, UserSkillProgress
from app.models.learner import MAX_HEARTS
from app.schemas.me import (
    AchievementOut,
    CourseProgressOut,
    DailyOut,
    DayActivityOut,
    DayXp,
    MeResponse,
    ProfileResponse,
    SettingsUpdate,
    StatsOut,
    UserOut,
)
from app.services import achievements, clock, hearts, lesson_engine, streak

PROFILE_CHART_DAYS = 7


def get_me(db: Session, user: User) -> MeResponse:
    """Top-bar data, with heart regen and streak expiry applied (and saved) on read."""
    now = _refresh_on_read(db, user)
    return _me_response(db, user, now)


def get_profile(db: Session, user: User) -> ProfileResponse:
    now = _refresh_on_read(db, user)
    return ProfileResponse(
        user=_user_out(user),
        stats=_stats_out(user, now),
        achievements=achievements.list_achievements(db, user),
        course_progress=_course_progress(db, user),
        week_xp=_recent_xp(db, user, now.date()),
    )


def list_achievements(db: Session, user: User) -> list[AchievementOut]:
    # Refresh first: the streak badge's progress must not show a streak that already broke.
    _refresh_on_read(db, user)
    return achievements.list_achievements(db, user)


def update_settings(db: Session, user: User, update: SettingsUpdate) -> MeResponse:
    if update.daily_goal_xp is not None:
        user.daily_goal_xp = update.daily_goal_xp
    if update.display_name is not None:
        user.display_name = update.display_name
    return commit_and_get_me(db, user)


def refill_hearts(db: Session, user: User) -> MeResponse:
    """Spend gems on full hearts and reopen the lesson that ran out of them."""
    now = clock.user_now(db, user)
    # Regen first, so a learner whose hearts already refilled is not charged gems.
    hearts.apply_regen(user.stats, now)
    hearts.refill(user.stats, now)
    lesson_engine.reopen_failed_attempt(db, user)
    return commit_and_get_me(db, user)


def practice_for_heart(db: Session, user: User) -> MeResponse:
    now = clock.user_now(db, user)
    hearts.apply_regen(user.stats, now)
    hearts.add_practice_heart(user.stats, now)
    return commit_and_get_me(db, user)


def commit_and_get_me(db: Session, user: User) -> MeResponse:
    """End a request that changed the learner: apply the lazy rules, commit once, respond."""
    now = clock.user_now(db, user)
    _apply_lazy_rules(user, now)
    db.commit()
    return _me_response(db, user, now)


def _refresh_on_read(db: Session, user: User) -> datetime:
    """Apply the lazy rules for a read, committing only if they changed something."""
    now = clock.user_now(db, user)
    if _apply_lazy_rules(user, now):
        db.commit()
    return now


def _apply_lazy_rules(user: User, now: datetime) -> bool:
    """Rules computed on read rather than by a background job; True if anything changed."""
    has_regenerated = hearts.apply_regen(user.stats, now)
    has_expired = streak.expire_if_broken(user.stats, now.date())
    return has_regenerated or has_expired


def _me_response(db: Session, user: User, now: datetime) -> MeResponse:
    today = now.date()
    today_activity = db.get(DailyActivity, (user.id, today))
    return MeResponse(
        user=_user_out(user),
        stats=_stats_out(user, now),
        daily=DailyOut(
            goal_xp=user.daily_goal_xp,
            today_xp=today_activity.xp_earned if today_activity else 0,
        ),
        recent_days=_recent_days(db, user, today),
    )


def _user_out(user: User) -> UserOut:
    return UserOut(
        id=user.id,
        username=user.username,
        display_name=user.display_name,
        avatar_color=user.avatar_color,
        daily_goal_xp=user.daily_goal_xp,
    )


def _stats_out(user: User, now: datetime) -> StatsOut:
    stats = user.stats
    return StatsOut(
        total_xp=stats.total_xp,
        gems=stats.gems,
        hearts=stats.hearts,
        max_hearts=MAX_HEARTS,
        next_heart_at=hearts.next_heart_at(stats),
        seconds_until_next_heart=hearts.seconds_until_next_heart(stats, now),
        refill_cost_gems=hearts.REFILL_COST_GEMS,
        current_streak=stats.current_streak,
        longest_streak=stats.longest_streak,
        streak_active_today=streak.is_active_today(stats, now.date()),
    )


def _course_progress(db: Session, user: User) -> CourseProgressOut:
    in_course = Skill.unit.has(Unit.course_id == user.current_course_id)
    skills_total = db.scalar(select(func.count()).select_from(Skill).where(in_course)) or 0
    skills_completed = db.scalar(
        select(func.count())
        .select_from(UserSkillProgress)
        .join(Skill)
        .where(
            UserSkillProgress.user_id == user.id,
            UserSkillProgress.completed_at.is_not(None),
            in_course,
        )
    )
    return CourseProgressOut(skills_completed=skills_completed or 0, skills_total=skills_total)


def _recent_days(db: Session, user: User, today: date) -> list[DayActivityOut]:
    """Which of the last 7 days had a finished lesson, for the streak week strip."""
    lessons_by_day = _recent_activity(db, user, today, DailyActivity.lessons_completed)
    return [
        DayActivityOut(date=day, is_active=lessons_by_day.get(day, 0) > 0)
        for day in _last_days(today)
    ]


def _recent_xp(db: Session, user: User, today: date) -> list[DayXp]:
    """XP for each of the last 7 days ending today, with 0 for days without a lesson."""
    xp_by_day = _recent_activity(db, user, today, DailyActivity.xp_earned)
    return [DayXp(date=day, xp=xp_by_day.get(day, 0)) for day in _last_days(today)]


def _last_days(today: date) -> list[date]:
    """The last 7 days, oldest first, ending today."""
    first_day = today - timedelta(days=PROFILE_CHART_DAYS - 1)
    return [first_day + timedelta(days=offset) for offset in range(PROFILE_CHART_DAYS)]


def _recent_activity(
    db: Session, user: User, today: date, column: InstrumentedAttribute[int]
) -> dict[date, int]:
    """One daily_activity column for the last 7 days, keyed by date (days without a row omitted)."""
    first_day = today - timedelta(days=PROFILE_CHART_DAYS - 1)
    rows = db.execute(
        select(DailyActivity.activity_date, column).where(
            DailyActivity.user_id == user.id,
            DailyActivity.activity_date.between(first_day, today),
        )
    ).all()
    return {activity_date: value for activity_date, value in rows}
