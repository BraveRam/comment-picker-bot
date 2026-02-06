# Comment Picker Bot

A Telegram bot that picks random comment winners from public Telegram channel posts. Send a link to a public post, and the bot fetches comments, deduplicates by user, and randomly selects a winner — displayed as a nicely formatted image.

## Features

- **Random winner selection** from public Telegram post comments
- **Comment deduplication** — each user can only win once per draw
- **Configurable pool sizes** — choose from top 5, 10, 20, 50, 100, or all comments
- **Winner card image** — generates a styled PNG announcement with user info
- **Rate limiting** — per-user cooldown to prevent abuse
- **Admin broadcast** — send messages to all registered users
- **PostgreSQL user tracking** — optional persistent user storage
- **Docker-ready** — containerised deployment with GitHub Actions CI/CD

## Prerequisites

- Python 3.12+
- A [Telegram Bot Token](https://core.telegram.org/bots#botfather)
- A Telegram API ID and API Hash from [my.telegram.org](https://my.telegram.org)
- A Telegram user session string (used to read comments via the Telegram API)
- *(Optional)* A PostgreSQL database for user tracking

## Configuration

Copy `.env.example` to `.env` and fill in the values:

| Variable              | Required | Description                                      |
|-----------------------|----------|--------------------------------------------------|
| `API_ID`              | Yes      | Telegram API ID from my.telegram.org             |
| `API_HASH`            | Yes      | Telegram API hash from my.telegram.org           |
| `BOT_TOKEN`           | Yes      | Bot token from @BotFather                        |
| `USER_SESSION_STRING` | Yes      | Telethon session string for the user client      |
| `ADMIN_ID`            | No       | Telegram user ID for admin-only commands         |
| `DATABASE_URL`        | No       | PostgreSQL connection string for user tracking   |

## Installation

### Docker (recommended)

```bash
docker build -t tg-comment-picker .
docker run --rm --env-file .env tg-comment-picker
```

### Local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

## Bot Commands

| Command      | Description                                            |
|--------------|--------------------------------------------------------|
| `/start`     | Register and see the welcome message                   |
| `/help`      | Show usage instructions                                |
| `/broadcast` | *(Admin only)* Send a message to all registered users  |

## Usage

1. Send a public Telegram post link (e.g. `https://t.me/channel/123`) to the bot.
2. Choose a pool size — the bot shows buttons for top N or all unique commenters.
3. Tap **Pick winner** — the bot randomly selects a winner and sends a styled image card.

## Project Structure

```
src/
├── main.py       # Entry point — initialises clients and registers handlers
├── bot.py        # Telegram event handlers and core bot logic
├── comments.py   # Link parsing, comment fetching, and deduplication
├── config.py     # Environment variable loading and constants
├── clients.py    # Telegram client factory (bot + user)
├── db.py         # PostgreSQL connection pool and user storage
├── render.py     # Winner announcement image generation (Pillow)
└── state.py      # TTL-based user session state management
```

## Running Tests

```bash
pip install -r requirements.txt
python -m pytest tests/ -v
```

## License

This project does not currently specify a license.
