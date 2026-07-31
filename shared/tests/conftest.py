import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from typing import AsyncGenerator
from redis.asyncio import Redis

from shared.core.database import Base
from shared.core.config import config


@pytest.fixture(scope="session")
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(config.test_database_url, echo=config.debug)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()

@pytest.fixture
async def db_session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    TestingSessionLocal = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False 
    )

    async with test_engine.connect() as connection:
        transaction = await connection.begin()

        async with TestingSessionLocal(
            bind=connection,
            join_transaction_mode="create_savepoint",
        ) as session:
            yield session

        await transaction.rollback()

@pytest.fixture
async def redis_client() -> AsyncGenerator[Redis, None]:
    redis_client = Redis.from_url(
        config.test_redis_url,
        encoding="utf-8",
        decode_responses=True
    )
    await redis_client.flushall()

    yield redis_client

    await redis_client.aclose()