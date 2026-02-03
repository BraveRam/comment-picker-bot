import io
import textwrap
from PIL import Image, ImageDraw, ImageFont

def _load_font(size, bold=False):
    return ImageFont.load_default()

def render_winner_image(user_id, username, name, comment):
    width = 820
    padding = 32
    bg_top = (252, 240, 220)
    bg_bottom = (230, 245, 255)
    fg = (20, 20, 20)
    accent = (20, 90, 160)
    border = (220, 230, 240)

    title_font = _load_font(34, bold=True)
    body_font = _load_font(22, bold=False)

    wrapped_comment = textwrap.wrap(f"Comment: {comment}", width=50)
    lines = [
        "And the winner is:",
        f"User ID: {user_id}",
        f"Username: {username}",
        f"Name: {name}",
        "",
        *wrapped_comment,
    ]

    line_height = body_font.getbbox("Ag")[3] + 8
    title_height = title_font.getbbox("Ag")[3] + 10
    height = padding * 2 + title_height + line_height * (len(lines) - 1)

    img = Image.new("RGB", (width, height), bg_top)
    draw = ImageDraw.Draw(img)

    # Vertical gradient background
    for y in range(height):
        mix = y / max(1, height - 1)
        r = int(bg_top[0] * (1 - mix) + bg_bottom[0] * mix)
        g = int(bg_top[1] * (1 - mix) + bg_bottom[1] * mix)
        b = int(bg_top[2] * (1 - mix) + bg_bottom[2] * mix)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Card container
    card_margin = 16
    card_rect = [card_margin, card_margin, width - card_margin, height - card_margin]
    draw.rounded_rectangle(card_rect, radius=24, fill=(255, 255, 255), outline=border, width=2)

    x = padding + 8
    y = padding + 4
    for i, line in enumerate(lines):
        if i == 0:
            draw.text((x, y), line, font=title_font, fill=accent)
            y += title_height
            continue
        draw.text((x, y), line, font=body_font, fill=fg)
        y += line_height

    output = io.BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    output.name = "winner.png"
    return output
