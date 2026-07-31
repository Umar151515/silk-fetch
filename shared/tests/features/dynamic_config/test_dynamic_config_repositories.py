import asyncio

from redis.asyncio import Redis

from shared.features.dynamic_config.models import DynamicConfigEnum
from shared.features.dynamic_config.repositories import DynamicConfigRepository


async def test_set_and_get_user_success(redis_client: Redis):
    repo = DynamicConfigRepository(redis_client)
    new_target_channel = "silkroadcargo2"

    assert await repo.get_config(DynamicConfigEnum.TARGET_CHANNEL) == DynamicConfigEnum.TARGET_CHANNEL.value

    await repo.set_config(DynamicConfigEnum.TARGET_CHANNEL, new_target_channel)

    assert await repo.get_config(DynamicConfigEnum.TARGET_CHANNEL) == new_target_channel