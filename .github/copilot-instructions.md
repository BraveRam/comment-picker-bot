# Copilot Instructions for Comment Picker Bot

## Project Overview
This is a Telegram bot (Python + Telethon) that picks random comment winners from public Telegram channel posts. It uses a dual-client architecture: a **bot client** for user interaction and a **user client** for fetching comments from channels.

## Tech Stack
- **Language**: Python 3.12+
- **Telegram library**: Telethon 1.42
- **Image rendering**: Pillow (PIL)
- **Database**: PostgreSQL via asyncpg (optional)
- **Config**: python-dotenv
- **Deployment**: Docker, GitHub Actions → AWS EC2 + PM2

## Architecture
- `src/main.py` — entry point; sets up clients, DB pool, and event handlers
- `src/bot.py` — all Telegram event handlers (start, help, broadcast, message, callbacks)
- `src/comments.py` — link parsing regex, comment fetching, deduplication
- `src/config.py` — environment variables and constants
- `src/clients.py` — Telegram client factories
- `src/db.py` — PostgreSQL schema and queries
- `src/render.py` — winner image generation with Pillow
- `src/state.py` — TTL-based in-memory state cleanup

## Conventions
- Async-first: all I/O uses `async`/`await`
- Source code lives in `src/`; tests live in `tests/`
- Tests use `pytest` and run with `python -m pytest tests/ -v`
- No ORM; raw SQL via asyncpg
- Environment config through `.env` files (see `.env.example`)

## Testing
Run tests with:
```bash
python -m pytest tests/ -v
```
Tests cover pure utility functions (link parsing, deduplication, state pruning, image rendering). Integration tests requiring Telegram API credentials are not included.
