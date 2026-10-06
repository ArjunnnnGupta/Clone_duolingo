from fastapi import APIRouter

from app.deps import CurrentUser, DbSession
from app.schemas.me import MeResponse
from app.services import profile

router = APIRouter()


@router.post("/hearts/refill")
def refill_hearts(db: DbSession, user: CurrentUser) -> MeResponse:
    return profile.refill_hearts(db, user)


@router.post("/hearts/practice")
def practice_for_heart(db: DbSession, user: CurrentUser) -> MeResponse:
    """Mock of "practice to earn hearts": grants one free heart."""
    return profile.practice_for_heart(db, user)
