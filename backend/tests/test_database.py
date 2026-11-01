from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import get_settings


async def test_database_connection() -> None:
    settings = get_settings()

    database_url = (
        f"postgresql+asyncpg://{settings.postgres_user}:"
        f"{settings.postgres_password.get_secret_value()}@"
        f"{settings.postgres_host}:{settings.postgres_port}/"
        f"{settings.postgres_db}"
    )

    engine = create_async_engine(
        database_url,
        pool_pre_ping=True,
        connect_args={"timeout": 3},
    )

    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))
            assert result.scalar_one() == 1
    finally:
        await engine.dispose()


async def test_postgis_extension() -> None:
    settings = get_settings()

    database_url = (
        f"postgresql+asyncpg://{settings.postgres_user}:"
        f"{settings.postgres_password.get_secret_value()}@"
        f"{settings.postgres_host}:{settings.postgres_port}/"
        f"{settings.postgres_db}"
    )

    engine = create_async_engine(
        database_url,
        pool_pre_ping=True,
        connect_args={"timeout": 3},
    )

    try:
        async with engine.connect() as connection:
            result = await connection.execute(
                text(
                    "SELECT extname "
                    "FROM pg_extension "
                    "WHERE extname = 'postgis'"
                )
            )
            assert result.scalar_one_or_none() == "postgis"
    finally:
        await engine.dispose()
