from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from shared.core.database import AsyncSessionLocal
from shared.core.redis import redis_client


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session

async def get_redis() -> Redis:
    return redis_client