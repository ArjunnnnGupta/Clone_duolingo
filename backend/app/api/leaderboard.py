from typing import Literal

from fastapi import APIRouter

from app.deps import CurrentUser, DbSession
from app.schemas.leaderboard import LeaderboardResponse
from app.services import leaderboard

router = APIRouter()


@router.get("/leaderboard")
def get_leaderboard(
    db: DbSession, user: CurrentUser, period: Literal["week"] = "week"
) -> LeaderboardResponse:
    # Only the weekly league exists; `period` keeps the URL from the API plan.
    return leaderboard.get_weekly_leaderboard(db, user)
