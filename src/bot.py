import random
import time
import re
import asyncio
from telethon import events, Button
from telethon.errors import FloodWaitError, UserIsBlockedError, ChatWriteForbiddenError

from config import MAX_COMMENTS, STATE_TTL_SECONDS, WINNER_TEXT_LEN, ADMIN_ID, LINK_COOLDOWN_SECONDS
from comments import extract_public_post_link, fetch_comments, dedupe_comments_by_user
from render import render_winner_image
from state import prune_state
from db import insert_user, list_user_ids

def register_handlers(bot_client, user_client, db_pool=None):
    state_by_user = {}
    last_link_at = {}

    @bot_client.on(events.NewMessage(pattern=r"^/start$"))
    async def handle_start(event):
        if db_pool:
            sender = await event.get_sender()
            await insert_user(
                db_pool,
                sender.id,
                getattr(sender, "username", None),
                getattr(sender, "first_name", None),
                getattr(sender, "last_name", None),
            )
        await event.reply(
            "Welcome! Send me a public post link like `https://t.me/channel/123` "
            "and I'll pick a random comment winner."
        )

    @bot_client.on(events.NewMessage(incoming=True, pattern=r"^/help$"))
    async def handle_help(event):
        await event.reply(
            "How it works:\n"
            "1. Send a public post link\n"
            "2. Choose the pool size (top 5/10/20/50/100 or all)\n"
            "3. Tap 'Pick winner' to select a random comment"
            "\n\n"
            "Developer: https://t.me/braveram"
        )

    @bot_client.on(events.NewMessage(incoming=True, pattern=r"^/broadcast(?:\s|$)"))
    async def handle_broadcast(event):
        if not db_pool:
            await event.reply("Database is not configured.")
            return
        if event.sender_id != ADMIN_ID:
            await event.reply("You are not authorized to use this command.")
            return

        message_text = event.raw_text.split(" ", 1)
        message_text = message_text[1].strip() if len(message_text) > 1 else ""

        reply_msg = await event.get_reply_message() if event.is_reply else None
        if not message_text and not reply_msg:
            await event.reply("Usage: /broadcast <message> or reply to a message with /broadcast")
            return

        user_ids = await list_user_ids(db_pool)
        sent = 0
        failed = 0

        for user_id in user_ids:
            try:
                if reply_msg and reply_msg.media:
                    await bot_client.send_file(user_id, reply_msg, caption=reply_msg.message)
                else:
                    text = message_text or (reply_msg.message if reply_msg else "")
                    if text:
                        await bot_client.send_message(user_id, text)
                sent += 1
                await asyncio.sleep(1.1)
            except FloodWaitError as exc:
                await asyncio.sleep(exc.seconds + 1)
            except (UserIsBlockedError, ChatWriteForbiddenError):
                failed += 1
            except Exception:
                failed += 1

        await event.reply(f"Broadcast complete. Sent: {sent}, Failed: {failed}")

    @bot_client.on(events.NewMessage(incoming=True))
    async def handle_message(event):
        prune_state(state_by_user, STATE_TTL_SECONDS)
        if event.raw_text and event.raw_text.strip().startswith("/"):
            return
        username, post_id = extract_public_post_link(event.raw_text)
        if not username:
            await event.reply("Send a public post link like `https://t.me/channel/123` or use /help.")
            return
        now = time.time()
        last = last_link_at.get(event.sender_id, 0)
        elapsed = now - last
        if elapsed < LINK_COOLDOWN_SECONDS:
            wait_for = int(LINK_COOLDOWN_SECONDS - elapsed)
            await event.reply(f"Please wait {wait_for}s before sending another link.")
            return
        last_link_at[event.sender_id] = now

        try:
            comments = await fetch_comments(user_client, username, post_id, MAX_COMMENTS)
        except Exception as exc:
            await event.reply(f"Failed to fetch comments: ensure the link is correct.")
            return

        if not comments:
            await event.reply("No comments found for that post (or comments are disabled).")
            return

        state_by_user[event.sender_id] = {
            "ts": time.time(),
            "comments_unique": dedupe_comments_by_user(comments),
        }

        total = len(state_by_user[event.sender_id]["comments_unique"])
        sizes = [5, 10, 20, 50, 100]
        available = [n for n in sizes if n <= total]

        buttons = []
        if available:
            row = []
            for n in available:
                row.append(Button.inline(f"Top {n}", f"pool:{n}".encode()))
                if len(row) == 3:
                    buttons.append(row)
                    row = []
            if row:
                buttons.append(row)
        buttons.append([Button.inline(f"All {total}", f"pool:{total}".encode())])

        await event.reply(
            f"Fetched {total} unique comment(s). Choose the pool size to pick from:",
            buttons=buttons,
        )

    @bot_client.on(events.CallbackQuery(data=re.compile(br"^pool:(\d+)$")))
    async def handle_pool_choice(event):
        prune_state(state_by_user, STATE_TTL_SECONDS)
        user_state = state_by_user.get(event.sender_id)
        if not user_state:
            await event.answer("Send a link first.", alert=True)
            return

        pool_size = int(event.data.split(b":")[1])
        unique = user_state["comments_unique"]
        if pool_size < 1:
            await event.answer("Invalid pool size.", alert=True)
            return
        pool_size = min(pool_size, len(unique))
        chosen = unique[:pool_size]
        user_state["picked_pool"] = chosen
        user_state["ts"] = time.time()

        await event.edit(
            f"Pool size: {len(chosen)} comment(s). Ready to pick a winner?",
            buttons=[[Button.inline("Pick winner", b"pick:winner")]],
        )

    @bot_client.on(events.CallbackQuery(data=b"pick:winner"))
    async def handle_pick_winner(event):
        prune_state(state_by_user, STATE_TTL_SECONDS)
        user_state = state_by_user.get(event.sender_id)
        if not user_state or "picked_pool" not in user_state:
            await event.answer("Pick a link and pool size first.", alert=True)
            return

        pool = user_state["picked_pool"]
        if not pool:
            await event.answer("No comments to pick from.", alert=True)
            return

        winner = random.choice(pool)
        text = winner["text"]
        if len(text) > WINNER_TEXT_LEN:
            text = text[:WINNER_TEXT_LEN].rstrip() + "..."
        user_id = winner["sender_id"]
        username = winner["username"] or "—"
        name = winner["name"] or "—"

        await event.edit(buttons=None)
        image = render_winner_image(user_id, username, name, text)
        await bot_client.send_file(event.chat_id, image)
        await event.answer()
