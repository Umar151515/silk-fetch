import asyncio

from pyrogram import Client, filters, idle
from pyrogram.types import Message


app = Client("myapp")

@app.on_message(filters.text & filters.private & filters.me)
async def echo(client: Client, message: Message):
    await message.forward("me")

async def main():
    await app.start()

    async for message in app.get_chat_members(TARGET_CHANNEL):
        message: Message
        print(message.text)

    await idle()

    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())



