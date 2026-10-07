import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Engine

from app.api import dev, health, hearts, leaderboard, lessons, me, path
from app.config import get_settings
from app.db import engine as default_engine
from app.errors import AppError, app_error_handler, validation_error_handler
from app.seed.startup import prepare_database


def create_app(db_engine: Engine | None = None) -> FastAPI:
    """Build the app; `db_engine` lets tests run startup against their own database."""
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        # Uvicorn configures only its own loggers; without this the startup report below would
        # never reach stdout (and so never reach the hosting platform's logs).
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
        prepare_database(db_engine or default_engine, should_seed=settings.seed_on_startup)
        yield

    app = FastAPI(title="Duolingo Clone API", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    for router in (health, me, path, lessons, hearts, leaderboard):
        app.include_router(router.router, prefix="/api")
    if settings.enable_dev_tools:
        app.include_router(dev.router, prefix="/api")
    return app


app = create_app()
