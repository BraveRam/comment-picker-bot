import re

PUBLIC_LINK_RE = re.compile(r"(?:https?://)?t\.me/([A-Za-z0-9_]+)/(\d+)")

def extract_public_post_link(text: str):
    match = PUBLIC_LINK_RE.search(text or "")
    if not match:
        return None, None
    username = match.group(1)
    post_id = int(match.group(2))
    return username, post_id

async def fetch_comments(user_client, username: str, post_id: int, max_comments: int):
    channel = await user_client.get_entity(username)
    comments = []
    async for msg in user_client.iter_messages(channel, reply_to=post_id):
        if msg.message:
            sender = await msg.get_sender()
            username = getattr(sender, "username", None)
            first_name = getattr(sender, "first_name", None)
            last_name = getattr(sender, "last_name", None)
            full_name = " ".join([p for p in [first_name, last_name] if p])
            comments.append(
                {
                    "text": msg.message.strip(),
                    "sender_id": msg.sender_id,
                    "username": username,
                    "name": full_name or None,
                }
            )
        if len(comments) >= max_comments:
            break
    return comments

def dedupe_comments_by_user(comments):
    seen = set()
    unique = []
    for item in comments:
        key = item["sender_id"]
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique
