import asyncpg

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS bot_users (
    telegram_id BIGINT PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""

async def create_pool(dsn: str):
    return await asyncpg.create_pool(dsn)

async def ensure_schema(pool):
    async with pool.acquire() as conn:
        await conn.execute(CREATE_TABLE_SQL)

async def insert_user(pool, telegram_id, username, first_name, last_name):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO bot_users (telegram_id, username, first_name, last_name)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (telegram_id) DO NOTHING
            """,
            telegram_id,
            username,
            first_name,
            last_name,
        )

async def list_user_ids(pool):
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT telegram_id FROM bot_users")
        return [row["telegram_id"] for row in rows]
