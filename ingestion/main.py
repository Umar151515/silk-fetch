from pyrogram import Client
from faststream import FastStream, ContextRepo
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

@broker.on_startup
async def start_bot(context: ContextRepo):
    await bot.start()
    context.set_global("bot", bot)

@broker.on_shutdown
async def stop_bot():
    await bot.stop()