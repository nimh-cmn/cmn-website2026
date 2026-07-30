from pathlib import Path
import re
from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "collaborators"
THEME_IMAGES = ROOT / "themes" / "cmn-2026" / "static" / "images"
ICON_DIR = THEME_IMAGES / "collaborators"
OUTPUT = THEME_IMAGES / "collaborative-cores-and-teams.png"


PALETTE = [
    "#285f8f",
    "#6f8f3f",
    "#8a5b35",
    "#5d6f85",
    "#3f7f79",
    "#8a4260",
    "#5f5a92",
    "#6e6a2d",
    "#2f6f9f",
]


def field(text, name, default=""):
    match = re.search(rf"^{name}:\s*(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else default


def load_items():
    items = []
    for path in CONTENT.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        items.append(
            {
                "title": field(text, "Title"),
                "short": field(text, "Short_name"),
                "lead": field(text, "Lead"),
                "icon": field(text, "Icon"),
                "label": field(text, "Icon_label"),
                "weight": int(field(text, "Weight", "99")),
            }
        )
    return sorted(items, key=lambda item: item["title"].lower())


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def fit_image(image, box):
    image = image.convert("RGBA")
    image = trim_whitespace(image)
    image.thumbnail(box, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", box, (255, 255, 255, 0))
    canvas.alpha_composite(image, ((box[0] - image.width) // 2, (box[1] - image.height) // 2))
    return canvas


def trim_whitespace(image):
    rgb = Image.new("RGBA", image.size, "white")
    rgb.alpha_composite(image)
    diff = ImageChops.difference(rgb, Image.new("RGBA", image.size, "white"))
    diff = ImageChops.add(diff, diff, 2.0, -20)
    bbox = diff.getbbox()
    return image.crop(bbox) if bbox else image


def draw_lettermark(draw, box, label, color, title_font):
    x, y, w, h = box
    draw.rounded_rectangle((x, y, x + w, y + h), radius=20, fill=color)
    text = label or "CMN"
    bbox = draw.textbbox((0, 0), text, font=title_font)
    tx = x + (w - (bbox[2] - bbox[0])) / 2
    ty = y + (h - (bbox[3] - bbox[1])) / 2 - 2
    draw.text((tx, ty), text, font=title_font, fill="white")


def wrap_pixels(draw, text, font_obj, max_width, max_lines=3):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), candidate, font=font_obj)
        if bbox[2] - bbox[0] <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines[-1] and draw.textbbox((0, 0), lines[-1] + "...", font=font_obj)[2] > max_width:
            lines[-1] = lines[-1][:-1].rstrip()
        lines[-1] = lines[-1] + "..."
    return lines


def main():
    items = load_items()
    width, height = 720 * 11 // 6, 612
    image = Image.new("RGB", (width, height), "#f3f7fa").convert("RGBA")
    draw = ImageDraw.Draw(image)

    title_font = font(44, bold=True)
    small_font = font(18)
    mark_font = font(34, bold=True)

    brains = Image.open(THEME_IMAGES / "brains.jpg").convert("RGBA")
    brain_h = 366
    brains = brains.resize((width, brain_h), Image.Resampling.LANCZOS)
    image.alpha_composite(brains, (0, 0))
    overlay = Image.new("RGBA", (width, brain_h), (255, 255, 255, 18))
    image.alpha_composite(overlay, (0, 0))

    draw.text((54, 390), "Collaborative Cores and Teams", font=title_font, fill="#17202a")
    draw.text(
        (56, 448),
        "A connected neuroimaging ecosystem spanning acquisition, computation, machine learning, data sharing, and molecular imaging.",
        font=small_font,
        fill="#56616f",
    )

    icon_size = 112
    gap_x = 34
    total_width = len(items) * icon_size + (len(items) - 1) * gap_x
    start_x = (width - total_width) // 2
    start_y = 488

    for index, item in enumerate(items):
        x = start_x + index * (icon_size + gap_x)
        y = start_y
        color = PALETTE[index % len(PALETTE)]

        draw.rounded_rectangle(
            (x + 7, y + 9, x + icon_size + 7, y + icon_size + 9),
            radius=24,
            fill=(30, 45, 58, 42),
        )
        draw.rounded_rectangle((x, y, x + icon_size, y + icon_size), radius=24, fill="white")

        icon_box = (x + 14, y + 14, icon_size - 28, icon_size - 28)
        icon_path = ICON_DIR / item["icon"] if item["icon"] else None
        if icon_path and icon_path.exists():
            draw.rounded_rectangle(
                (icon_box[0], icon_box[1], icon_box[0] + icon_box[2], icon_box[1] + icon_box[3]),
                radius=18,
                fill="#f3f7fa",
            )
            icon = fit_image(Image.open(icon_path), (icon_box[2] - 10, icon_box[3] - 12))
            image.alpha_composite(
                icon,
                (icon_box[0] + (icon_box[2] - icon.width) // 2, icon_box[1] + (icon_box[3] - icon.height) // 2),
            )
        else:
            draw_lettermark(draw, icon_box, item["label"] or item["short"], color, mark_font)

    image = image.convert("RGB")
    image.save(OUTPUT, quality=94)
    print(OUTPUT)


if __name__ == "__main__":
    main()
