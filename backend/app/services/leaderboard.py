"""Weekly league table, computed from daily_activity for the current Monday-Sunday week."""

from datetime import timedelta

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from app.models import DailyActivity, User
from app.schemas.leaderboard import LeaderboardEntry, LeaderboardResponse
from app.services import clock


def get_weekly_leaderboard(db: Session, user: User) -> LeaderboardResponse:
    period_start = clock.week_start(clock.user_today(db, user))
    period_end = period_start + timedelta(days=6)
    week_xp = func.coalesce(func.sum(DailyActivity.xp_earned), 0)
    rows = db.execute(
        select(User.id, User.display_name, User.avatar_color, week_xp)
        # The week filter sits in the JOIN, not a WHERE: a WHERE would drop learners with no
        # activity this week (everyone on a Monday) instead of listing them at 0 XP.
        .outerjoin(
            DailyActivity,
            and_(
                DailyActivity.user_id == User.id,
                DailyActivity.activity_date.between(period_start, period_end),
            ),
        )
        .group_by(User.id)
        # Ties go alphabetically by name, so no learner (e.g. the demo, id 1) is favoured.
        .order_by(week_xp.desc(), User.display_name)
    ).all()
    entries = [
        LeaderboardEntry(
            rank=rank,
            user_id=user_id,
            display_name=display_name,
            avatar_color=avatar_color,
            xp=xp,
            is_me=user_id == user.id,
        )
        for rank, (user_id, display_name, avatar_color, xp) in enumerate(rows, start=1)
    ]
    return LeaderboardResponse(period_start=period_start, period_end=period_end, entries=entries)
