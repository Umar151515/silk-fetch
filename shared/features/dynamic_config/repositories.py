import json
from typing import overload, Literal, Any

from redis.asyncio import Redis
from fastapi import Depends

from shared.features.dynamic_config.models import DynamicConfigEnum
from shared.core.dependencies import get_redis


class DynamicConfigRepository:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    @overload
    async def get_config(self, key: Literal[DynamicConfigEnum.TARGET_CHANNEL]) -> str: ...

    async def get_config(self, key: DynamicConfigEnum) -> Any:
        raw_value = await self.redis_client.get(key.key)
        
        if raw_value is None:
            return key.value

        try:
            return json.loads(raw_value)
        except (json.JSONDecodeError, TypeError):
            return key.value

    @overload
    async def set_config(self, key: Literal[DynamicConfigEnum.TARGET_CHANNEL], value: str): ...

    async def set_config(self, key: DynamicConfigEnum, value: Any):
        serialized_value = json.dumps(value)
        await self.redis_client.set(key.key, serialized_value)


def get_dynamic_config_repository(
        redis_client: Redis = Depends(get_redis)
    ) -> DynamicConfigRepository:
    return DynamicConfigRepository(redis_client)