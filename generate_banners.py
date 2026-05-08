"""Generate 3 LinkedIn banner variants (1584x396)."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(__file__).resolve().parent / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1584, 396
FONT_PATH = "/tmp/dmsans/DMSans-VF.ttf"


def load_font(weight: int, size_px: int) -> ImageFont.FreeTypeFont:
    """Load DM Sans variable font at a given weight axis value."""
    f = ImageFont.truetype(FONT_PATH, size=size_px)
    try:
        f.set_variation_by_axes([size_px, weight])
    except Exception:
        try:
            f.set_variation_by_name(
                {600: "SemiBold", 500: "Medium", 400: "Regular", 700: "Bold"}[weight]
            )
        except Exception:
            pass
    return f


def text_width(draw: ImageDraw.ImageDraw, text: str, font) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def draw_right_aligned(draw, text, font, right_x, top_y, fill):
    w = text_width(draw, text, font)
    draw.text((right_x - w, top_y), text, font=font, fill=fill)


def draw_tracked_right(draw, text, font, right_x, top_y, fill, em_size, tracking_em):
    """Draw text right-aligned with per-character extra spacing (in em units)."""
    extra = em_size * tracking_em
    advances = []
    for ch in text:
        bbox = draw.textbbox((0, 0), ch, font=font)
        advances.append(bbox[2] - bbox[0])
    total = sum(advances) + extra * (len(text) - 1)
    x = right_x - int(round(total))
    for i, ch in enumerate(text):
        draw.text((x, top_y), ch, font=font, fill=fill)
        x += advances[i] + (extra if i < len(text) - 1 else 0)


# ---------- Variant 1: Pure white ----------
img1 = Image.new("RGB", (W, H), "#FFFFFF")
img1.save(OUT / "linkedin_banner_v1_pure.png", "PNG")

# ---------- Variant 2: Corner mark ----------
img2 = Image.new("RGB", (W, H), "#FAFAFA")
d2 = ImageDraw.Draw(img2)
font_name_22 = load_font(weight=600, size_px=22)
draw_right_aligned(
    d2, "Roberto Quintero", font_name_22,
    right_x=W - 36, top_y=36, fill="#999999",
)
img2.save(OUT / "linkedin_banner_v2_corner.png", "PNG")

# ---------- Variant 3: Tagline line ----------
img3 = Image.new("RGB", (W, H), "#FAFAFA")
d3 = ImageDraw.Draw(img3)

font_name_22 = load_font(weight=600, size_px=22)
draw_right_aligned(
    d3, "Roberto Quintero", font_name_22,
    right_x=W - 36, top_y=36, fill="#1A1A1A",
)

tagline = "BUILDING CONSUMER PRODUCTS · BARCELONA"
font_tag = load_font(weight=500, size_px=12)
# Anchor tagline so its visual baseline sits 36px from the bottom edge.
# Use the font's ascent/descent to compute the top-y for a 12px nominal size.
ascent, descent = font_tag.getmetrics()
line_height = ascent + descent
top_y_tag = H - 36 - line_height
draw_tracked_right(
    d3, tagline, font_tag,
    right_x=W - 36, top_y=top_y_tag, fill="#999999",
    em_size=12, tracking_em=0.18,
)
img3.save(OUT / "linkedin_banner_v3_tagline.png", "PNG")

for f in sorted(OUT.glob("linkedin_banner_v*.png")):
    print(f, f.stat().st_size, "bytes")
