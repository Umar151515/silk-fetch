from redis.asyncio import Redis

from shared.core.config import config


redis_client = Redis.from_url(
    config.redis_url,
    encoding="utf-8",
    decode_responses=True
)