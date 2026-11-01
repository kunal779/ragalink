from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.redis import redis_client
from app.db.session import SessionFactory

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "ragalink-api",
    }


@router.get("/ready")
async def readiness() -> JSONResponse:
    postgres_ready = False
    redis_ready = False

    try:
        async with SessionFactory() as session:
            await session.execute(text("SELECT 1"))
        postgres_ready = True
    except SQLAlchemyError:
        pass

    try:
        await redis_client.ping()
        redis_ready = True
    except Exception:
        pass

    if not postgres_ready or not redis_ready:
        failed_dependencies = []

        if not postgres_ready:
            failed_dependencies.append("postgres")

        if not redis_ready:
            failed_dependencies.append("redis")

        return JSONResponse(
            status_code=503,
            content={
                "error": {
                    "code": "SERVICE_NOT_READY",
                    "message": "One or more required dependencies are unavailable.",
                    "details": {
                        "failed_dependencies": failed_dependencies,
                    },
                }
            },
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": "ready",
            "service": "ragalink-api",
        },
    )
