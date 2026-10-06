"""Demo and testing helpers; main.py only mounts this router when ENABLE_DEV_TOOLS is on."""

from fastapi import APIRouter

from app.deps import CurrentUser, DbSession
from app.schemas.dev import AdvanceDayRequest
from app.schemas.me import MeResponse
from app.services import dev_tools

router = APIRouter()


@router.post("/dev/advance-day")
def advance_day(request: AdvanceDayRequest, db: DbSession, user: CurrentUser) -> MeResponse:
    return dev_tools.advance_day(db, user, request.days)


@router.post("/dev/reset")
def reset(db: DbSession, user: CurrentUser) -> MeResponse:
    return dev_tools.reset(db, user)
