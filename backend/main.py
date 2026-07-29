from contextlib import asynccontextmanager

from pyrogram import Client
from fastapi import FastAPI

from shared.core.config import config
from backend.api import router


bot = Client(
    "silk_fetch",
    api_id=config.telegram_api_id,
    api_hash=config.telegram_api_hash,
    plugins=dict(root="backend/src/ingestion")
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.start()

    yield {"tg_bot": bot}

    await bot.stop()

app = FastAPI(lifespan=lifespan)
app.include_router(router)