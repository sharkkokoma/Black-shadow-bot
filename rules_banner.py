# 🌐 Web3.0 Rules Banner — neon gradient, cyber-grid aesthetic
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH, HEIGHT = 900, 260


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "DejaVuSans-Bold.ttf",
        "arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def generate_rules_banner(server_name: str = "BLACK SHADOW") -> io.BytesIO:
    """បង្កើត banner រចនាប័ទ្ម Web3.0 — neon gradient + cyber grid lines"""
    canvas = Image.new("RGB", (WIDTH, HEIGHT), (6, 4, 16))
    draw = ImageDraw.Draw(canvas, "RGBA")

    # ១. Diagonal neon gradient background (purple → cyan)
    top_color = (30, 8, 60)
    bottom_color = (5, 30, 40)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))

    # ២. Cyber grid lines (subtle)
    grid_color = (153, 69, 255, 40)
    for x in range(0, WIDTH, 45):
        draw.line([(x, 0), (x, HEIGHT)], fill=grid_color, width=1)
    for y in range(0, HEIGHT, 45):
        draw.line([(0, y), (WIDTH, y)], fill=grid_color, width=1)

    # ៣. Glow orbs (neon purple + cyan) — trang trí góc
    glow_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.ellipse([-80, -80, 200, 200], fill=(153, 69, 255, 130))
    glow_draw.ellipse([WIDTH - 200, HEIGHT - 150, WIDTH + 80, HEIGHT + 80], fill=(20, 241, 217, 110))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(60))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), glow_layer)
    draw = ImageDraw.Draw(canvas, "RGBA")

    # ៤. Neon border frame
    draw.rectangle([3, 3, WIDTH - 3, HEIGHT - 3], outline=(153, 69, 255, 255), width=3)
    draw.rectangle([9, 9, WIDTH - 9, HEIGHT - 9], outline=(20, 241, 217, 120), width=1)

    # ៥. Corner accent brackets (cyber HUD style)
    bracket_len = 26
    bracket_color = (20, 241, 217, 255)
    corners = [(14, 14, 1, 1), (WIDTH - 14, 14, -1, 1), (14, HEIGHT - 14, 1, -1), (WIDTH - 14, HEIGHT - 14, -1, -1)]
    for cx, cy, dx, dy in corners:
        draw.line([(cx, cy), (cx + bracket_len * dx, cy)], fill=bracket_color, width=3)
        draw.line([(cx, cy), (cx, cy + bracket_len * dy)], fill=bracket_color, width=3)

    # ៦. Title text "SERVER RULES" ជាមួយ glow effect
    font_tag = _load_font(20)
    font_title = _load_font(52)
    font_sub = _load_font(18)

    tag_text = "⛓ ON-CHAIN MANIFESTO"
    tag_bbox = draw.textbbox((0, 0), tag_text, font=font_tag)
    tag_w = tag_bbox[2] - tag_bbox[0]
    draw.text(((WIDTH - tag_w) / 2, 46), tag_text, font=font_tag, fill=(20, 241, 217, 255))

    title_text = "SERVER RULES"
    title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
    title_w = title_bbox[2] - title_bbox[0]
    title_x = (WIDTH - title_w) / 2
    # glow layers (draw offset copies with transparency for a neon-glow feel)
    for offset in [(0, 0, 255), (-1, -1, 120), (1, 1, 120), (2, 2, 90)]:
        ox, oy, alpha = offset
        draw.text((title_x + ox, 82 + oy), title_text, font=font_title, fill=(153, 69, 255, alpha))
    draw.text((title_x, 82), title_text, font=font_title, fill=(255, 255, 255, 255))

    sub_text = f"⟦ {server_name.upper()} PROTOCOL ⟧"
    sub_bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
    sub_w = sub_bbox[2] - sub_bbox[0]
    draw.text(((WIDTH - sub_w) / 2, 155), sub_text, font=font_sub, fill=(180, 170, 220, 255))

    footer_text = "▸ READ · AGREE · PARTICIPATE ◂"
    font_footer = _load_font(14)
    footer_bbox = draw.textbbox((0, 0), footer_text, font=font_footer)
    footer_w = footer_bbox[2] - footer_bbox[0]
    draw.text(((WIDTH - footer_w) / 2, 200), footer_text, font=font_footer, fill=(20, 241, 217, 200))

    buffer = io.BytesIO()
    canvas.convert("RGB").save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
