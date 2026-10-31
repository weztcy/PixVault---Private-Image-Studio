"""Generate the PixVault application icon (icons/pixvault.ico).

The icon is rendered at 4x resolution and downsampled for crisp small sizes.
The design is a rounded gradient tile (navy -> deep teal) with an emerald
vault arch and an upward arrow, matching the app's dark navy / emerald theme.
"""

from pathlib import Path

from PIL import Image, ImageDraw

NAVY_TOP = (10, 18, 38)
NAVY_BOTTOM = (15, 34, 52)
EMERALD = (52, 211, 153)
EMERALD_DARK = (16, 98, 66)
HIGHLIGHT = (167, 243, 208)

SUPERSAMPLE = 4


def _vertical_gradient(size):
    image = Image.new("RGB", (size, size))
    draw = ImageDraw.Draw(image)
    for y in range(size):
        t = y / max(1, size - 1)
        color = tuple(int(NAVY_TOP[i] + (NAVY_BOTTOM[i] - NAVY_TOP[i]) * t) for i in range(3))
        draw.line((0, y, size, y), fill=color)
    return image


def _rounded_mask(size, radius_ratio=0.22):
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=int(size * radius_ratio), fill=255)
    return mask


def render_icon(size):
    """Render a single icon frame at the requested output size."""
    canvas_size = int(size * SUPERSAMPLE)

    background = (
        _vertical_gradient(canvas_size)
        .convert("RGBA")
        .resize((canvas_size, canvas_size), Image.LANCZOS)
    )

    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    canvas.paste(background, (0, 0), _rounded_mask(canvas_size))

    draw = ImageDraw.Draw(canvas)
    s = canvas_size

    # Vault arch.
    arch_width = int(s * 0.46)
    arch_thickness = max(2, int(s * 0.072))
    arch_box = (
        int((s - arch_width) / 2),
        int(s * 0.20),
        int((s + arch_width) / 2),
        int(s * 0.76),
    )
    draw.arc(arch_box, start=180, end=360, fill=EMERALD_DARK, width=arch_thickness)
    draw.arc(
        (arch_box[0] + 1, arch_box[1] + 1, arch_box[2] - 1, arch_box[3] + 1),
        start=180,
        end=360,
        fill=EMERALD,
        width=max(1, arch_thickness - 2),
    )

    # Arrow inside the vault.
    shaft_half = int(s * 0.032)
    shaft_top = int(s * 0.34)
    shaft_bottom = int(s * 0.58)
    center_x = s // 2
    draw.rectangle(
        (center_x - shaft_half, shaft_top, center_x + shaft_half, shaft_bottom),
        fill=HIGHLIGHT,
    )
    arrow_size = int(s * 0.13)
    draw.polygon(
        [
            (center_x, int(s * 0.20)),
            (center_x - arrow_size, int(s * 0.38)),
            (center_x + arrow_size, int(s * 0.38)),
        ],
        fill=HIGHLIGHT,
    )

    # Subtle top-left sheen.
    sheen = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    sheen_draw = ImageDraw.Draw(sheen)
    sheen_draw.ellipse(
        (int(-s * 0.15), int(-s * 0.35), int(s * 0.75), int(s * 0.45)),
        fill=(255, 255, 255, 34),
    )
    canvas = Image.alpha_composite(canvas, sheen)

    out = canvas.resize((size, size), Image.LANCZOS)
    return out.convert("RGBA")


def main():
    project_root = Path(__file__).resolve().parents[1]
    icons_dir = project_root / "icons"
    icons_dir.mkdir(exist_ok=True)

    icon_path = icons_dir / "pixvault.ico"
    largest = render_icon(256)
    largest.save(
        icon_path,
        format="ICO",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    print(f"Icon written to {icon_path}")


if __name__ == "__main__":
    main()