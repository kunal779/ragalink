import httpx
import pytest

from app.api import health
from app.main import app


async def request_api(path: str) -> httpx.Response:
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        return await client.get(path)


@pytest.mark.asyncio
async def test_liveness_endpoint() -> None:
    response = await request_api("/api/v1/health/live")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "ragalink-api",
    }


@pytest.mark.asyncio
async def test_readiness_when_dependencies_are_available(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def available() -> bool:
        return True

    monkeypatch.setattr(health, "check_postgres", available)
    monkeypatch.setattr(health, "check_redis", available)

    response = await request_api("/api/v1/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "service": "ragalink-api",
        "checks": {
            "postgres": "ok",
            "redis": "ok",
        },
    }


@pytest.mark.asyncio
async def test_readiness_when_postgres_is_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def unavailable() -> bool:
        return False

    async def available() -> bool:
        return True

    monkeypatch.setattr(health, "check_postgres", unavailable)
    monkeypatch.setattr(health, "check_redis", available)

    response = await request_api("/api/v1/health/ready")

    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"
    assert response.json()["checks"]["postgres"] == "unavailable"
    assert response.json()["checks"]["redis"] == "ok"