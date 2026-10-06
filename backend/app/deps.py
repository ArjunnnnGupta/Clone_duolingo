"""FastAPI dependencies shared by every router."""

from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import SessionLocal
from app.errors import AppError
from app.models import User


def get_db() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session


DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(db: DbSession) -> User:
    """The one demo learner; there is no login, so every request acts as this user."""
    user = db.get(User, get_settings().default_user_id)
    if user is None:
        raise AppError("NOT_FOUND", "The demo learner does not exist; run the seed.", 404)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
