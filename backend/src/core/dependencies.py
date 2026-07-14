from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.core.database import AsyncSessionLocal


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session