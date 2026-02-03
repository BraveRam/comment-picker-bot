from telethon import TelegramClient
from config import USER_SESSION_STRING
from telethon.sessions import StringSession

def create_clients(api_id: int, api_hash: str):
    user_client = TelegramClient(StringSession(USER_SESSION_STRING), api_id, api_hash)
    bot_client = TelegramClient("bot_session", api_id, api_hash)
    return user_client, bot_client
