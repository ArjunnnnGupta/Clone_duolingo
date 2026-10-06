from fastapi import APIRouter

from app.deps import CurrentUser, DbSession
from app.schemas.path import PathResponse
from app.services import path

router = APIRouter()


@router.get("/path")
def get_path(db: DbSession, user: CurrentUser) -> PathResponse:
    return path.get_path(db, user)
