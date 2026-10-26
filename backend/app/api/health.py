import asyncio
import logging
from typing import Literal

from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from sqlalchemy import text

from app.db.redis import redis_client
from app.db.session import engine

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])


class HealthCheckResponse(BaseModel):
    status: Literal["ok"]
    service: str


class ReadinessCheckResponse(BaseModel):
    status: Literal["ready", "not_ready"]
    service: str
    checks: dict[str, Literal["ok", "unavailable"]]


@router.get(
    "/health/live",
    response_model=HealthCheckResponse,
    summary="Check whether the API process is alive",
)
async def liveness_check() -> HealthCheckResponse:
    return HealthCheckResponse(
        status="ok",
        service="ragalink-api",
    )


async def check_postgres() -> bool:
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return True
    except Exception:
        logger.warning("Readiness check failed: PostgreSQL unavailable")
        return False


async def check_redis() -> bool:
    try:
        return bool(await redis_client.ping())
    except Exception:
        logger.warning("Readiness check failed: Redis unavailable")
        return False


@router.get(
    "/health/ready",
    response_model=ReadinessCheckResponse,
    summary="Check whether required dependencies are available",
)
async def readiness_check(
    response: Response,
) -> ReadinessCheckResponse:
    postgres_ok, redis_ok = await asyncio.gather(
        check_postgres(),
        check_redis(),
    )

    postgres_status: Literal["ok", "unavailable"] = (
        "ok" if postgres_ok else "unavailable"
    )
    redis_status: Literal["ok", "unavailable"] = (
        "ok" if redis_ok else "unavailable"
    )

    checks: dict[str, Literal["ok", "unavailable"]] = {
        "postgres": postgres_status,
        "redis": redis_status,
    }

    ready = postgres_ok and redis_ok

    if not ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    readiness_status: Literal["ready", "not_ready"] = (
        "ready" if ready else "not_ready"
    )

    return ReadinessCheckResponse(
        status=readiness_status,
        service="ragalink-api",
        checks=checks,
    )