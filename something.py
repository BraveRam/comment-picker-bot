import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

async def main():
    async with TelegramClient(StringSession(), api_id, api_hash) as client:
        print(client.session.save())

asyncio.run(main())
