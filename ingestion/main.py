import asyncio

from pyrogram import Client
from faststream import FastStream
from faststream.redis import RedisBroker

from shared.core.config import config


broker = RedisBroker(config.redis_url)
faststream_app = FastStream(broker)

bot = Client(
    "silk_fetch",
    api_id=config.telegram_api_id,
    api_hash=config.telegram_api_hash,
    plugins=dict(root="ingestion")
)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(faststream_app.run())
    bot.run()