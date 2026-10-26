from redis.asyncio import Redis

from app.core.config import get_settings

settings = get_settings()

redis_client: Redis = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password.get_secret_value(),
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
    health_check_interval=30,
)