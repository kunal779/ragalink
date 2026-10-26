from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import get_settings
from app.db.redis import redis_client
from app.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Release application resources during shutdown."""
    try:
        yield
    finally:
        try:
            await redis_client.aclose()
        finally:
            await engine.dispose()


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(health_router, prefix=settings.api_prefix)