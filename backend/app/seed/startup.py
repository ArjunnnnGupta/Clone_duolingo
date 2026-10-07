"""Startup safeguard: make sure the schema and the demo data exist, without ever wiping data.

Runs on every app start (see main.py). Unlike `python -m app.seed.run`, which drops and rebuilds
everything, this only creates what is missing, so a restart or redeploy keeps all progress.
"""

import logging

from sqlalchemy import Engine, func, inspect, select
from sqlalchemy.orm import Session

from app.models import Base, Exercise, User
from app.seed.run import seed_database

logger = logging.getLogger(__name__)


def prepare_database(target_engine: Engine, *, should_seed: bool) -> None:
    """Create missing tables; seed the demo data only if there are no users yet."""
    _create_missing_tables(target_engine)
    if not should_seed:
        logger.info("Database: SEED_ON_STARTUP is off; not checking seed data")
        return

    user_count = _count(target_engine, User)
    if user_count > 0:
        logger.info("Database: already seeded (%d users); leaving data untouched", user_count)
        return

    try:
        # One transaction, as in reset_database: a failed seed leaves nothing half-written.
        with Session(target_engine) as db, db.begin():
            seed_database(db)
    except Exception:
        logger.exception(
            "Database: users table is empty but seeding failed and was rolled back. "
            "If content rows are left over from an earlier partial setup, reset the database "
            "with `python -m app.seed.run`."
        )
        raise
    logger.info(
        "Database: users table was empty; seeded demo data (%d users, %d exercises)",
        _count(target_engine, User),
        _count(target_engine, Exercise),
    )


def _create_missing_tables(target_engine: Engine) -> None:
    expected = set(Base.metadata.tables)
    existing = set(inspect(target_engine).get_table_names()) & expected
    # create_all only issues CREATE TABLE for tables that do not exist; it never alters or drops.
    Base.metadata.create_all(target_engine)
    if not existing:
        logger.info("Database: created schema (%d tables)", len(expected))
    elif existing != expected:
        logger.info("Database: created missing tables: %s", ", ".join(sorted(expected - existing)))
    else:
        logger.info("Database: schema already present (%d tables)", len(expected))


def _count(target_engine: Engine, model: type[Base]) -> int:
    with Session(target_engine) as db:
        return db.scalar(select(func.count()).select_from(model)) or 0
