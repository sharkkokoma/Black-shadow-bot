# 🖼️ បង្កើត Welcome Card រូបភាព (1024x500)
import io
import aiohttp
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

WIDTH, HEIGHT = 1024, 500
AVATAR_SIZE = 180


async def _fetch_image_bytes(session: aiohttp.ClientSession, url: str) -> bytes:
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.read()


def _load_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _draw_centered_text(draw: ImageDraw.ImageDraw, text: str, y: int, font: ImageFont.FreeTypeFont, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (WIDTH - text_w) / 2
    draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0, 180))
    draw.text((x, y), text, font=font, fill=fill)


async def generate_welcome_card(member, member_count: int, background_url: str) -> io.BytesIO:
    async with aiohttp.ClientSession() as session:
        try:
            bg_bytes = await _fetch_image_bytes(session, background_url)
            bg = Image.open(io.BytesIO(bg_bytes)).convert("RGBA")
            bg = ImageOps.fit(bg, (WIDTH, HEIGHT), Image.LANCZOS)
        except Exception:
            bg = Image.new("RGBA", (WIDTH, HEIGHT), (26, 26, 46, 255))
            gradient = Image.new("L", (1, HEIGHT))
            for y in range(HEIGHT):
                gradient.putpixel((0, y), int(255 * (y / HEIGHT)))
            gradient = gradient.resize((WIDTH, HEIGHT))
            overlay = Image.new("RGBA", (WIDTH, HEIGHT), (15, 15, 26, 255))
            bg = Image.composite(overlay, bg, gradient)

        canvas = bg.convert("RGBA")

        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 140))
        canvas = Image.alpha_composite(canvas, overlay)

        draw = ImageDraw.Draw(canvas)
        draw.rectangle([4, 4, WIDTH - 4, HEIGHT - 4], outline=(139, 0, 255, 255), width=8)

        avatar_x = WIDTH // 2 - AVATAR_SIZE // 2
        avatar_y = 60
        try:
            avatar_asset = member.display_avatar.replace(size=256, format="png")
            avatar_bytes = await _fetch_image_bytes(session, str(avatar_asset.url))
            avatar_img = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")
            avatar_img = ImageOps.fit(avatar_img, (AVATAR_SIZE, AVATAR_SIZE), Image.LANCZOS)

            glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            glow_draw = ImageDraw.Draw(glow)
            glow_r = AVATAR_SIZE // 2 + 20
            glow_center = (WIDTH // 2, avatar_y + AVATAR_SIZE // 2)
            glow_draw.ellipse(
                [glow_center[0] - glow_r, glow_center[1] - glow_r, glow_center[0] + glow_r, glow_center[1] + glow_r],
                fill=(139, 0, 255, 160),
            )
            glow = glow.filter(ImageFilter.GaussianBlur(18))
            canvas = Image.alpha_composite(canvas, glow)
            draw = ImageDraw.Draw(canvas)

            mask = Image.new("L", (AVATAR_SIZE, AVATAR_SIZE), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse([0, 0, AVATAR_SIZE, AVATAR_SIZE], fill=255)
            canvas.paste(avatar_img, (avatar_x, avatar_y), mask)

            draw.ellipse(
                [avatar_x - 3, avatar_y - 3, avatar_x + AVATAR_SIZE + 3, avatar_y + AVATAR_SIZE + 3],
                outline=(255, 255, 255, 255),
                width=6,
            )
        except Exception:
            pass

        font_welcome = _load_font(42)
        _draw_centered_text(draw, "W E L C O M E", 260, font_welcome, (139, 0, 255, 255))

        font_name = _load_font(48)
        display_name = member.name
        if len(display_name) > 20:
            display_name = display_name[:18] + "..."
        _draw_centered_text(draw, display_name, 320, font_name, (255, 255, 255, 255))

        font_server = _load_font(28)
        _draw_centered_text(draw, "⚔️ BLACK SHADOW ⚔️", 385, font_server, (204, 204, 204, 255))

        font_count = _load_font(24)
        _draw_centered_text(draw, f"សមាជិកទី #{member_count}", 435, font_count, (139, 0, 255, 255))

        buffer = io.BytesIO()
        canvas.convert("RGB").save(buffer, format="PNG")
        buffer.seek(0)
        return buffer
