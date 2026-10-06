from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings
from app.db import create_db_engine
from app.deps import get_db
from app.main import create_app
from app.models import User
from app.seed.run import DEMO_USER_ID, reset_database


@pytest.fixture
def engine(tmp_path: Path) -> Iterator[Engine]:
    """A freshly seeded database in a temp file, one per test.

    A file rather than in-memory SQLite: the API tests run requests on other threads, and
    an in-memory database is private to the thread that opened it.
    """
    test_engine = create_db_engine(f"sqlite:///{tmp_path / 'test.db'}")
    reset_database(test_engine)
    yield test_engine
    test_engine.dispose()


@pytest.fixture
def seeded_db(engine: Engine) -> Iterator[Session]:
    # Matches the app's SessionLocal, so objects stay readable after a service commits.
    with Session(engine, expire_on_commit=False) as session:
        yield session


@pytest.fixture
def demo_user(seeded_db: Session) -> User:
    return seeded_db.get_one(User, DEMO_USER_ID)


@pytest.fixture
def client(engine: Engine, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    """The real app with its database swapped for the seeded temp file.

    Dev tools are switched on here explicitly, so the tests never depend on a local .env.
    """
    monkeypatch.setenv("ENABLE_DEV_TOOLS", "true")
    get_settings.cache_clear()
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)

    def get_test_db() -> Iterator[Session]:
        with session_factory() as session:
            yield session

    app = create_app()
    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as test_client:
        yield test_client
    get_settings.cache_clear()
