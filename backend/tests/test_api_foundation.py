from unittest.mock import AsyncMock, patch

from httpx import ASGITransport, AsyncClient
from sqlalchemy.exc import OperationalError

from app.main import app


async def test_health() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "ragalink-api",
    }


async def test_legacy_health() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "ragalink-api",
    }


async def test_readiness() -> None:
    mock_session = AsyncMock()

    with (
        patch(
            "app.api.v1.health.SessionFactory",
        ) as session_factory,
        patch(
            "app.api.v1.health.redis_client.ping",
            new_callable=AsyncMock,
        ) as redis_ping,
    ):
        session_factory.return_value.__aenter__.return_value = mock_session

        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            response = await client.get("/api/v1/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "service": "ragalink-api",
    }

    redis_ping.assert_awaited_once()


async def test_readiness_returns_503_when_postgres_fails() -> None:
    mock_session = AsyncMock()

    mock_session.execute.side_effect = OperationalError(
        "SELECT 1",
        {},
        Exception("database unavailable"),
    )

    with (
        patch(
            "app.api.v1.health.SessionFactory",
        ) as session_factory,
        patch(
            "app.api.v1.health.redis_client.ping",
            new_callable=AsyncMock,
        ) as redis_ping,
    ):
        session_factory.return_value.__aenter__.return_value = mock_session

        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            response = await client.get("/api/v1/ready")

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "SERVICE_NOT_READY"
    assert "postgres" in response.json()["error"]["details"]["failed_dependencies"]

    redis_ping.assert_awaited_once()


async def test_readiness_returns_503_when_redis_fails() -> None:
    mock_session = AsyncMock()

    with (
        patch(
            "app.api.v1.health.SessionFactory",
        ) as session_factory,
        patch(
            "app.api.v1.health.redis_client.ping",
            new_callable=AsyncMock,
            side_effect=RuntimeError("redis unavailable"),
        ),
    ):
        session_factory.return_value.__aenter__.return_value = mock_session

        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            response = await client.get("/api/v1/ready")

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "SERVICE_NOT_READY"
    assert "redis" in response.json()["error"]["details"]["failed_dependencies"]
