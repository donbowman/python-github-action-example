from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api import router
from .config import Settings, get_settings
from .db import create_db_engine, create_session_factory


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the FastAPI application.

    Passing settings explicitly keeps tests independent of the environment.
    """
    settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        engine = create_db_engine(settings.database_url)
        app.state.engine = engine
        app.state.session_factory = create_session_factory(engine)
        yield
        engine.dispose()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )
    app.include_router(router)
    return app


app = create_app()
