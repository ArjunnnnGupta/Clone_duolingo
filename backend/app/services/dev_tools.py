"""Dev tools for demos and testing: simulate days passing and restore the seed state."""

from typing import cast

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app.models import AppSetting, User
from app.schemas.me import MeResponse
from app.seed.run import reset_database
from app.services import clock, profile


def advance_day(db: Session, user: User, days: int) -> MeResponse:
    """Move the simulated clock forward; streaks, regen and the week all follow it."""
    setting = db.get(AppSetting, clock.DAY_OFFSET_KEY)
    if setting is None:
        setting = AppSetting(key=clock.DAY_OFFSET_KEY, value="0")
        db.add(setting)
    setting.value = str(int(setting.value) + days)
    # One commit saves the new offset together with the regen/expiry it triggers.
    return profile.commit_and_get_me(db, user)


def reset(db: Session, user: User) -> MeResponse:
    """Drop, recreate and reseed every table, then return the fresh learner's view."""
    user_id = user.id
    # Request sessions are always bound to the app's engine, never to a single connection.
    engine = cast(Engine, db.get_bind())
    # Close first so the learner below is re-read from the reseeded tables. The session keeps
    # objects after a commit (expire_on_commit=False), so without this it would hand back the
    # pre-reset learner from its cache, e.g. a streak of 0 where the fresh seed has 6.
    db.close()
    reset_database(engine)
    fresh_user = db.get_one(User, user_id)
    return profile.get_me(db, fresh_user)
