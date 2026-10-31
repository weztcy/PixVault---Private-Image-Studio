"""Capture full-page screenshots of every PixVault workspace page.

Run from the repository root with the project virtualenv active::

    python tools/capture_pages.py
    python tools/capture_pages.py --width 1920 --scale 2
    python tools/capture_pages.py --empty
    python tools/capture_pages.py --pages home,convert,history
    python tools/capture_pages.py --samples "C:/Users/me/Pictures/docs" --limit 40

The tool is strictly read-only: pages are populated through their own
``load_images`` / ``load_history`` import path, which only fills the queue
and the preview widgets.  No batch is ever started, no image is processed
and no output file is written.  ``assert_idle()`` enforces that guarantee.

The main window is laid out with ``Qt.WidgetAttribute.WA_DontShowOnScreen``
so nothing flashes on the desktop, then resized until the active page's
``QScrollArea`` no longer needs a vertical scrollbar.  Each PNG therefore
contains the complete page content, not just the first viewport.

The native ``windows`` platform plugin is required: the ``offscreen``
plugin ships no fonts, which would render every label as a blank box.
"""

import argparse
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Page order mirrors the sidebar / Workspace registration order.
PAGE_ORDER = [
    "home",
    "convert",
    "compress",
    "resize",
    "crop",
    "transform",
    "dpi",
    "metadata",
    "colorspace",
    "bitdepth",
    "history",
    "privacy",
]

# Formats the preview can display.  The .ico and .gif samples are skipped
# because they are too small to illustrate a full workspace page.
IMAGE_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".jpe",
    ".jfif",
    ".webp",
    ".avif",
    ".bmp",
    ".tif",
    ".tiff",
    ".heic",
    ".heif",
}

SKIPPED_SAMPLES = {".ico", ".gif"}

# Preferred preview subject so every page shows a real photograph instead
# of whichever file happens to sort first.
HERO_SAMPLE = "sample-photo-3840x2160.jpg"

# How many candidates to probe when no HERO_SAMPLE is present.
HERO_SEARCH_DEPTH = 80

DEFAULT_SAMPLE_DIRS = [
    Path.home() / "OneDrive" / "Pictures" / "docs",
    Path.home() / "Pictures" / "docs",
    Path.home() / "OneDrive" / "Pictures" / "sample",
    Path.home() / "Pictures" / "sample",
    Path.home() / "OneDrive" / "Pictures" / "PixVault",
    Path.home() / "Pictures" / "PixVault",
]


# =====================
# COMMAND LINE
# =====================

def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Capture full-page screenshots of every PixVault page.",
    )
    parser.add_argument(
        "--out",
        default=str(PROJECT_ROOT / "docs" / "screenshots"),
        help="Directory that receives the PNG files.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1920,
        help="Logical window width (default: 1920).",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=1080,
        help="Initial logical window height before fitting (default: 1080).",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=1.0,
        help="Device pixel ratio, e.g. 2 for retina-crisp output (default: 1).",
    )
    parser.add_argument(
        "--samples",
        default=None,
        help="Folder with sample images used to populate the pages.",
    )
    parser.add_argument(
        "--empty",
        action="store_true",
        help="Keep the pages empty instead of loading sample images.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Only load the first N sample images (0 = no limit).",
    )
    parser.add_argument(
        "--pages",
        default=",".join(PAGE_ORDER),
        help="Comma separated subset of pages to capture.",
    )
    return parser.parse_args(argv)


def resolve_sample_dir(explicit):
    if explicit:
        folder = Path(explicit).expanduser()
        return folder if folder.is_dir() else None

    for candidate in DEFAULT_SAMPLE_DIRS:
        if candidate.is_dir():
            return candidate

    return None


def pick_hero(files):
    """Return the best preview subject, or None when nothing suits."""
    exact = next((path for path in files if path.name == HERO_SAMPLE), None)

    if exact is not None:
        return exact

    # No curated hero: probe a bounded number of candidates and take the
    # first landscape photograph large enough to fill the preview panel.
    try:
        from PIL import Image
    except ImportError:
        return files[0] if files else None

    for path in files[:HERO_SEARCH_DEPTH]:
        try:
            with Image.open(path) as image:
                width, height = image.size
        except (OSError, ValueError):
            continue

        if width >= 1000 and width >= height:
            return path

    return files[0] if files else None


def collect_samples(sample_dir, limit=0):
    """Return sample files with the hero photograph first."""
    if sample_dir is None:
        return []

    files = sorted(
        path
        for path in sample_dir.iterdir()
        if path.is_file()
        and path.suffix.lower() in IMAGE_SUFFIXES
        and path.suffix.lower() not in SKIPPED_SAMPLES
    )

    hero = pick_hero(files)

    if hero is not None:
        files.remove(hero)
        files.insert(0, hero)

    if limit and limit > 0:
        files = files[:limit]

    return files


# =====================
# RENDERING HELPERS
# =====================

def settle(app, rounds=8):
    """Let pending layout / paint work complete."""
    for _ in range(rounds):
        app.processEvents()


def scroll_area_of(page):
    scroll = getattr(page, "scroll_area", None)

    if scroll is None:
        return None

    return scroll if scroll.widget() is not None else None


def assert_idle(window):
    """Refuse to continue if any page started a processing batch.

    Capturing a screenshot must never trigger real image processing or
    write files, so this guard turns an accidental start into a hard
    failure instead of silently exporting a user's images.
    """
    service = getattr(window, "batch_service", None)

    if service is None:
        return

    if service.is_running():
        raise RuntimeError(
            "Batch processing is running; screenshots must not start work."
        )

    pages = getattr(getattr(window, "workspace", None), "pages", {}) or {}

    busy = [
        name
        for name, page in pages.items()
        if getattr(page, "_processing_active", False)
    ]

    if busy:
        raise RuntimeError(
            "Page(s) report an active processing state: " + ", ".join(sorted(busy))
        )


def populate_page(page, samples):
    """Load sample images through the page's own import path."""
    loader = getattr(page, "load_images", None)

    if callable(loader) and samples:
        loader(samples)

    reload_history = getattr(page, "load_history", None)

    if callable(reload_history):
        reload_history()


def fit_page(app, window, page, margin=2, attempts=5):
    """Resize the window until the whole page fits without a scrollbar."""
    scroll = scroll_area_of(page)

    if scroll is None:
        settle(app)
        return

    height = window.header.height() + scroll.widget().sizeHint().height() + margin

    for _ in range(attempts):
        window.resize(window.width(), height)
        settle(app)

        # When the viewport is still too short Qt reports the remaining
        # overflow on the vertical scrollbar; grow by exactly that much.
        overflow = scroll.verticalScrollBar().maximum()

        if overflow <= 0:
            break

        height += overflow + margin

    settle(app)


def capture(app, window, name, page, output_dir, index, samples):
    window.workspace.show_page(name)
    settle(app)

    populate_page(page, samples)
    settle(app)

    # Screenshots only ever read state; fail loudly if that changed.
    assert_idle(window)

    fit_page(app, window, page)

    pixmap = window.grab()
    target = output_dir / f"{index:02d}_{name}.png"

    if not pixmap.save(str(target), "PNG"):
        raise RuntimeError(f"Unable to write {target}")

    image = pixmap.toImage()

    return target, image.width(), image.height()


# =====================
# MAIN
# =====================

def main(argv=None):
    args = parse_args(argv)

    # Qt must see the scale factor before QApplication is constructed.
    if args.scale and args.scale != 1.0:
        os.environ["QT_SCALE_FACTOR"] = str(args.scale)

    # The offscreen plugin has no font database, so force the native one.
    os.environ.pop("QT_QPA_PLATFORM", None)

    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication

    from ui.main_window import MainWindow

    output_dir = Path(args.out).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    sample_dir = None if args.empty else resolve_sample_dir(args.samples)
    samples = collect_samples(sample_dir, limit=args.limit)

    requested = [name.strip() for name in args.pages.split(",") if name.strip()]
    unknown = [name for name in requested if name not in PAGE_ORDER]

    if unknown:
        raise SystemExit(
            "Unknown page(s): "
            + ", ".join(unknown)
            + "\nAvailable: "
            + ", ".join(PAGE_ORDER)
        )

    app = QApplication(sys.argv[:1])

    window = MainWindow()
    window.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen, True)
    window.resize(args.width, args.height)
    window.show()
    settle(app)

    print(f"Platform      : {app.platformName()}")
    print(f"Output folder : {output_dir}")
    print(f"Samples       : {sample_dir if samples else 'none (empty state)'}")
    print(f"Loaded        : {len(samples)} image(s)")
    print("Processing    : disabled (screenshots never start a batch)")
    print()

    written = []

    for index, name in enumerate(PAGE_ORDER, start=1):
        if name not in requested:
            continue

        page = window.workspace.pages.get(name)

        if page is None:
            print(f"{index:02d} {name:<11} SKIPPED (page not registered)")
            continue

        target, width, height = capture(
            app,
            window,
            name,
            page,
            output_dir,
            index,
            samples,
        )

        written.append(target)
        print(
            f"{index:02d} {name:<11} {width}x{height}px  "
            f"{target.stat().st_size // 1024} KB  {target.name}"
        )

    print()
    print(f"Captured {len(written)} page(s).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

