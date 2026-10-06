from fastapi import APIRouter

from app.deps import CurrentUser, DbSession
from app.schemas.me import AchievementOut, MeResponse, ProfileResponse, SettingsUpdate
from app.services import profile

router = APIRouter()


@router.get("/me")
def get_me(db: DbSession, user: CurrentUser) -> MeResponse:
    return profile.get_me(db, user)


@router.get("/me/profile")
def get_profile(db: DbSession, user: CurrentUser) -> ProfileResponse:
    return profile.get_profile(db, user)


@router.patch("/me/settings")
def update_settings(update: SettingsUpdate, db: DbSession, user: CurrentUser) -> MeResponse:
    return profile.update_settings(db, user, update)


@router.get("/achievements")
def list_achievements(db: DbSession, user: CurrentUser) -> list[AchievementOut]:
    return profile.list_achievements(db, user)
