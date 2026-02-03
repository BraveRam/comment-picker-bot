import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID") or 0)
API_HASH = os.getenv("API_HASH") or ""
BOT_TOKEN = os.getenv("BOT_TOKEN") or ""
DATABASE_URL = os.getenv("DATABASE_URL") or ""
ADMIN_ID = int(os.getenv("ADMIN_ID") or 0)
USER_SESSION_STRING = os.getenv("USER_SESSION_STRING") or ""

MAX_COMMENTS = 100
STATE_TTL_SECONDS = 10 * 60
WINNER_TEXT_LEN = 50
LINK_COOLDOWN_SECONDS = 20
