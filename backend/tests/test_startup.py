"""The startup safeguard: creates missing tables, seeds an empty database once, never reseeds."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, func, inspect, select
from sqlalchemy.orm import Session

from app.db import create_db_engine
from app.main import create_app
from app.models import Base, Exercise, User
from app.seed.run import DEMO_USER_ID
from app.seed.startup import prepare_database

STARTUP_LOGGER = "app.seed.startup"


@pytest.fixture
def empty_engine(tmp_path: Path) -> Engine:
    """A database file that does not exist yet, like a fresh deploy volume."""
    return create_db_engine(f"sqlite:///{tmp_path / 'fresh.db'}")


def count(engine: Engine, model: type[Base]) -> int:
    with Session(engine) as db:
        return db.scalar(select(func.count()).select_from(model)) or 0


def test_fresh_database_gets_schema_and_seed(
    empty_engine: Engine, caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level("INFO", logger=STARTUP_LOGGER):
        prepare_database(empty_engine, should_seed=True)

    assert set(inspect(empty_engine).get_table_names()) == set(Base.metadata.tables)
    assert (count(empty_engine, User), count(empty_engine, Exercise)) == (15, 288)
    with Session(empty_engine) as db:
        assert db.get_one(User, DEMO_USER_ID).stats.total_xp == 115
    assert "created schema" in caplog.text and "seeded demo data" in caplog.text


def test_restart_never_reseeds_or_touches_existing_data(
    empty_engine: Engine, caplog: pytest.LogCaptureFixture
) -> None:
    prepare_database(empty_engine, should_seed=True)
    with Session(empty_engine) as db:
        db.get_one(User, DEMO_USER_ID).display_name = "Changed Between Starts"
        db.commit()

    with caplog.at_level("INFO", logger=STARTUP_LOGGER):
        prepare_database(empty_engine, should_seed=True)

    assert count(empty_engine, User) == 15  # not duplicated
    with Session(empty_engine) as db:
        assert db.get_one(User, DEMO_USER_ID).display_name == "Changed Between Starts"
    assert "schema already present" in caplog.text
    assert "already seeded (15 users); leaving data untouched" in caplog.text


def test_existing_schema_with_no_users_is_seeded(empty_engine: Engine) -> None:
    Base.metadata.create_all(empty_engine)
    prepare_database(empty_engine, should_seed=True)
    assert count(empty_engine, User) == 15


def test_seeding_can_be_switched_off(
    empty_engine: Engine, caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level("INFO", logger=STARTUP_LOGGER):
        prepare_database(empty_engine, should_seed=False)
    assert set(inspect(empty_engine).get_table_names()) == set(Base.metadata.tables)
    assert count(empty_engine, User) == 0
    assert "SEED_ON_STARTUP is off" in caplog.text


def test_app_startup_runs_the_safeguard(empty_engine: Engine) -> None:
    with TestClient(create_app(empty_engine)):
        pass
    assert count(empty_engine, User) == 15
