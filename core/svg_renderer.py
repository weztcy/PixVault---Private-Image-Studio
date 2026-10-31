"""
SVG Renderer for PixVault.

SVG -> PIL.Image

Backend:
    PySide6.QtSvg
"""

from pathlib import Path

from PIL import Image
from PySide6.QtCore import QByteArray, QSize
from PySide6.QtGui import QImage, QPainter
from PySide6.QtSvg import QSvgRenderer


class SVGRenderer:
    def __init__(self):
        pass

    # ==================================================
    # MAIN ENTRY
    # ==================================================

    def render(self, svg_path, width=None, height=None):

        svg_path = Path(svg_path)

        if not svg_path.exists():
            raise FileNotFoundError(f"SVG file not found: {svg_path}")

        svg_data = svg_path.read_bytes()

        return self.render_bytes(svg_data, width, height)

    # ==================================================
    # SVG BYTES RENDER
    # ==================================================

    def render_bytes(self, svg_data, width=None, height=None):

        renderer = QSvgRenderer(QByteArray(svg_data))

        if not renderer.isValid():
            raise RuntimeError("Invalid SVG document")

        default_size = renderer.defaultSize()

        size = self.calculate_size(default_size, width, height)

        canvas = QImage(size, QImage.Format.Format_RGBA8888)

        canvas.fill(0)

        painter = QPainter(canvas)

        renderer.render(painter)

        painter.end()

        return self.qimage_to_pil(canvas)

    # ==================================================
    # SIZE
    # ==================================================

    def calculate_size(self, original, width=None, height=None):

        ow = original.width()

        oh = original.height()

        if width and height:
            return QSize(int(width), int(height))

        if width and ow > 0:
            return QSize(int(width), max(1, int(width * oh / ow)))

        if height and oh > 0:
            return QSize(max(1, int(height * ow / oh)), int(height))

        if ow > 0 and oh > 0:
            return QSize(ow, oh)

        return QSize(1024, 1024)

    # ==================================================
    # QIMAGE -> PIL
    # ==================================================

    def qimage_to_pil(self, image):

        image = image.convertToFormat(QImage.Format.Format_RGBA8888)

        width = image.width()

        height = image.height()

        bytes_per_line = image.bytesPerLine()

        ptr = image.bits()

        # PySide6 6.x:
        # bits() dapat berupa memoryview/bytes

        if hasattr(ptr, "tobytes"):
            raw = ptr.tobytes()

        else:
            raw = bytes(ptr)

        expected_size = height * bytes_per_line

        raw = raw[:expected_size]

        pil = Image.frombuffer(
            "RGBA", (width, height), raw, "raw", "RGBA", bytes_per_line, 1
        )

        return pil.copy()
