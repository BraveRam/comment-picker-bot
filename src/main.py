import asyncio

from bot import register_handlers
from clients import create_clients
from config import API_ID, API_HASH, BOT_TOKEN, DATABASE_URL
from db import create_pool, ensure_schema

async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing from .env.")
    if not API_ID or not API_HASH:
        raise RuntimeError("API_ID or API_HASH is missing from .env")

    user_client, bot_client = create_clients(API_ID, API_HASH)

    db_pool = None
    if DATABASE_URL:
        db_pool = await create_pool(DATABASE_URL)
        await ensure_schema(db_pool)

    register_handlers(bot_client, user_client, db_pool)

    await user_client.start()
    await bot_client.start(bot_token=BOT_TOKEN)
    print("Bot is running. Send it a public post link.")
    await bot_client.run_until_disconnected()

    if db_pool:
        await db_pool.close()

asyncio.run(main())
