from pathlib import Path

from PIL import Image, ImageOps
from PySide6.QtCore import QEvent, QRectF, QSize, Qt, QTimer
from PySide6.QtGui import (
    QImage,
    QImageReader,
    QPainter,
    QPixmap,
)
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

try:
    from PySide6.QtSvg import QSvgRenderer
except ImportError:
    QSvgRenderer = None


from ui.styles.image_preview_style import apply_image_preview_style


class ImagePreview(QWidget):
    def __init__(self):
        super().__init__()

        self.current_image = None

        # Original image data is kept separate
        # from the pixmap displayed on screen.
        self._original_pixmap = None
        self._svg_renderer = None

        # Resizing triggers many Resize events; debounce so a window drag
        # does not re-scale large images on every frame.
        self._last_scaled_size = None
        self._rescale_timer = QTimer(self)
        self._rescale_timer.setSingleShot(True)
        self._rescale_timer.setInterval(60)
        self._rescale_timer.timeout.connect(self.update_scaled_preview)

        self.setObjectName("image_preview_widget")

        self.setup_ui()
        self.apply_styles()
        self.clear()

    # =====================
    # MAIN UI
    # =====================

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Main panel

        self.card = QFrame()
        self.card.setObjectName("image_preview_card")

        self.card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        card_layout = QVBoxLayout(self.card)

        card_layout.setContentsMargins(20, 20, 20, 18)
        card_layout.setSpacing(16)

        # Header

        card_layout.addLayout(self.create_header())

        # Preview canvas

        card_layout.addWidget(
            self.create_canvas(),
            1,
        )

        # Footer

        card_layout.addWidget(self.create_footer())

        main_layout.addWidget(self.card)

    # =====================
    # HEADER
    # =====================

    def create_header(self):
        layout = QHBoxLayout()
        layout.setSpacing(12)

        # Header icon

        icon_box = QFrame()
        icon_box.setObjectName("image_preview_icon_box")
        icon_box.setFixedSize(44, 44)

        icon_layout = QVBoxLayout(icon_box)
        icon_layout.setContentsMargins(0, 0, 0, 0)

        icon = QLabel("▧")
        icon.setObjectName("image_preview_header_icon")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_layout.addWidget(icon)

        # Header text

        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        eyebrow = QLabel("VISUAL WORKSPACE")
        eyebrow.setObjectName("image_preview_eyebrow")

        title = QLabel("Image Preview")
        title.setObjectName("image_preview_title")

        subtitle = QLabel("Inspect your selected image.")
        subtitle.setObjectName("image_preview_subtitle")

        text_layout.addWidget(eyebrow)
        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        # Status badge

        self.status_label = QLabel("NO IMAGE")
        self.status_label.setObjectName("image_preview_status")

        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label.setProperty(
            "preview_state",
            "empty",
        )

        layout.addWidget(icon_box)
        layout.addLayout(text_layout, 1)

        layout.addWidget(
            self.status_label,
            0,
            Qt.AlignmentFlag.AlignTop,
        )

        return layout

    # =====================
    # PREVIEW CANVAS
    # =====================

    def create_canvas(self):
        canvas = QFrame()
        canvas.setObjectName("image_preview_canvas")

        canvas.setMinimumHeight(470)

        canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        layout = QVBoxLayout(canvas)

        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(0)

        # Stack lets us switch between
        # placeholder and image without
        # changing the surrounding layout.

        self.preview_stack = QStackedWidget()
        self.preview_stack.setObjectName("image_preview_stack")

        # Empty / error state

        self.empty_page = self.create_empty_state()

        # Actual image page

        self.image_page = QWidget()
        self.image_page.setObjectName("image_preview_image_page")

        image_layout = QVBoxLayout(self.image_page)

        image_layout.setContentsMargins(0, 0, 0, 0)
        image_layout.setSpacing(0)

        self.preview_label = QLabel()
        self.preview_label.setObjectName("image_preview_display")

        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.preview_label.setMinimumSize(0, 0)

        # Ignored size policy prevents a large
        # pixmap from forcing the workspace
        # to become wider than its container.

        self.preview_label.setSizePolicy(
            QSizePolicy.Policy.Ignored,
            QSizePolicy.Policy.Ignored,
        )

        self.preview_label.setScaledContents(False)

        self.preview_label.installEventFilter(self)

        image_layout.addWidget(self.preview_label)

        self.preview_stack.addWidget(self.empty_page)

        self.preview_stack.addWidget(self.image_page)

        layout.addWidget(self.preview_stack)

        return canvas

    # =====================
    # EMPTY STATE
    # =====================

    def create_empty_state(self):
        page = QWidget()
        page.setObjectName("image_preview_empty_page")

        layout = QVBoxLayout(page)

        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(12)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Placeholder icon

        icon_box = QFrame()
        icon_box.setObjectName("image_preview_empty_icon_box")

        icon_box.setFixedSize(72, 72)

        icon_layout = QVBoxLayout(icon_box)

        icon_layout.setContentsMargins(0, 0, 0, 0)

        icon = QLabel("▧")
        icon.setObjectName("image_preview_empty_icon")

        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_layout.addWidget(icon)

        # Placeholder title

        self.empty_title = QLabel("No Image Selected")

        self.empty_title.setObjectName("image_preview_empty_title")

        self.empty_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_title.setWordWrap(True)

        # Placeholder description

        self.empty_description = QLabel(
            "Select an image from your collection to display its preview here."
        )

        self.empty_description.setObjectName("image_preview_empty_description")

        self.empty_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_description.setWordWrap(True)

        layout.addStretch()

        layout.addWidget(
            icon_box,
            0,
            Qt.AlignmentFlag.AlignHCenter,
        )

        layout.addWidget(self.empty_title)

        layout.addWidget(self.empty_description)

        layout.addStretch()

        return page

    # =====================
    # FOOTER
    # =====================

    def create_footer(self):
        footer = QFrame()
        footer.setObjectName("image_preview_footer")

        layout = QHBoxLayout(footer)

        layout.setContentsMargins(13, 11, 13, 11)
        layout.setSpacing(12)

        # File icon

        file_icon = QLabel("◇")
        file_icon.setObjectName("image_preview_file_icon")

        # Filename

        self.file_label = QLabel("No file selected")

        self.file_label.setObjectName("image_preview_filename")

        self.file_label.setWordWrap(True)

        self.file_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        # Image dimensions

        self.resolution_label = QLabel("-")
        self.resolution_label.setObjectName("image_preview_resolution")

        self.resolution_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # File format

        self.format_label = QLabel("-")
        self.format_label.setObjectName("image_preview_format")

        self.format_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(file_icon)
        layout.addWidget(self.file_label, 1)
        layout.addWidget(self.resolution_label)
        layout.addWidget(self.format_label)

        return footer

    # =====================
    # STATUS MANAGEMENT
    # =====================

    def set_status(self, state, text):
        self.status_label.setText(str(text))

        self.status_label.setProperty(
            "preview_state",
            str(state),
        )

        self.status_label.style().unpolish(self.status_label)

        self.status_label.style().polish(self.status_label)

        self.status_label.update()

    # =====================
    # SET IMAGE
    # =====================

    def set_image(self, image_path):
        if not image_path:
            self.clear()
            return

        # Clear previously loaded image data
        # while preserving the new file path.

        self._original_pixmap = None
        self._svg_renderer = None
        self._last_scaled_size = None

        self.preview_label.clear()

        self.current_image = Path(image_path).expanduser()

        file = self.current_image

        # Footer metadata

        self.file_label.setText(file.name)

        self.file_label.setToolTip(str(file))

        self.format_label.setText(file.suffix.lstrip(".").upper() or "IMAGE")

        self.resolution_label.setText("-")

        if not file.is_file():
            self.show_unavailable("The selected image file could not be found.")
            return

        try:
            if file.suffix.lower() == ".svg" and QSvgRenderer is not None:
                self.load_svg(file)

            else:
                self.load_raster(file)

        except Exception as error:
            self.show_unavailable(str(error))
            return

        # Display image

        self.preview_stack.setCurrentWidget(self.image_page)

        self.set_status(
            "loaded",
            "IMAGE LOADED",
        )

        self.update_scaled_preview()

    # =====================
    # LOAD RASTER IMAGE
    # =====================

    def load_raster(self, file):
        # First use Qt's native image reader.
        # Auto-transform handles supported
        # EXIF orientation metadata.

        reader = QImageReader(str(file))

        reader.setAutoTransform(True)

        qt_image = QImage()

        if reader.canRead():
            qt_image = reader.read()

        # Some formats may not be supported
        # by the installed Qt image plugins.
        # Pillow is used as a fallback.

        if qt_image.isNull():
            qt_image = self.load_with_pillow(file)

        if qt_image.isNull():
            raise ValueError("This image format could not be decoded.")

        self._original_pixmap = QPixmap.fromImage(qt_image)

        if self._original_pixmap.isNull():
            raise ValueError("Unable to create an image preview.")

        self.resolution_label.setText(f"{qt_image.width():,} × {qt_image.height():,}")

    # =====================
    # PILLOW FALLBACK
    # =====================

    def load_with_pillow(self, file):
        with Image.open(file) as image:
            # Apply EXIF orientation if present.

            image = ImageOps.exif_transpose(image)

            # Convert unsupported color modes
            # to a format Qt can display.

            image = image.convert("RGBA")

            width, height = image.size

            image_bytes = image.tobytes()

        qt_image = QImage(
            image_bytes,
            width,
            height,
            width * 4,
            QImage.Format.Format_RGBA8888,
        )

        # Copy pixel data before the Python
        # bytes buffer goes out of scope.

        return qt_image.copy()

    # =====================
    # SVG PREVIEW
    # =====================

    def load_svg(self, file):
        renderer = QSvgRenderer(str(file))

        if not renderer.isValid():
            raise ValueError("This SVG file is invalid or cannot be rendered.")

        self._svg_renderer = renderer

        image_size = renderer.defaultSize()

        if image_size.isValid():
            self.resolution_label.setText(
                f"{image_size.width():,} × {image_size.height():,}"
            )
        else:
            self.resolution_label.setText("Vector image")

    # =====================
    # RESPONSIVE IMAGE RENDER
    # =====================

    def update_scaled_preview(self):
        target_size = self.preview_label.size()

        if target_size.width() <= 0 or target_size.height() <= 0:
            return

        if self._last_scaled_size == target_size:
            return

        self._last_scaled_size = target_size

        # Render SVG directly to the current
        # display size to keep edges sharp.

        if self._svg_renderer is not None:
            self.render_svg_preview(target_size)
            return

        if self._original_pixmap is None or self._original_pixmap.isNull():
            return

        # Scale from original image data,
        # never from an already scaled image.
        # This preserves quality after resize.

        scaled = self._original_pixmap.scaled(
            target_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.preview_label.setPixmap(scaled)

    # =====================
    # RENDER SVG
    # =====================

    def render_svg_preview(self, target_size):
        renderer = self._svg_renderer

        if renderer is None:
            return

        source_size = renderer.defaultSize()

        if not source_size.isValid():
            view_box = renderer.viewBoxF()

            if view_box.width() > 0 and view_box.height() > 0:
                source_size = QSize(
                    max(1, int(view_box.width())),
                    max(1, int(view_box.height())),
                )
            else:
                source_size = QSize(1600, 900)

        scaled_size = source_size.scaled(
            target_size,
            Qt.AspectRatioMode.KeepAspectRatio,
        )

        if scaled_size.isEmpty():
            return

        pixmap = QPixmap(scaled_size)

        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing,
            True,
        )

        renderer.render(
            painter,
            QRectF(
                0,
                0,
                scaled_size.width(),
                scaled_size.height(),
            ),
        )

        painter.end()

        self.preview_label.setPixmap(pixmap)

    # =====================
    # HANDLE PREVIEW RESIZE
    # =====================

    def eventFilter(self, watched, event):
        if watched is self.preview_label and event.type() == QEvent.Type.Resize:
            self._rescale_timer.start()

        return super().eventFilter(
            watched,
            event,
        )

    # =====================
    # ERROR STATE
    # =====================

    def show_unavailable(self, message):
        self._original_pixmap = None
        self._svg_renderer = None
        self._last_scaled_size = None

        self.preview_label.clear()

        self.empty_title.setText("Preview Unavailable")

        self.empty_description.setText(str(message))

        self.preview_stack.setCurrentWidget(self.empty_page)

        self.set_status(
            "error",
            "UNAVAILABLE",
        )

    # =====================
    # CLEAR PREVIEW
    # =====================

    def clear(self):
        self.current_image = None

        self._original_pixmap = None
        self._svg_renderer = None
        self._last_scaled_size = None

        self.preview_label.clear()

        self.empty_title.setText("No Image Selected")

        self.empty_description.setText(
            "Select an image from your collection to display its preview here."
        )

        self.file_label.setText("No file selected")

        self.file_label.setToolTip("")

        self.resolution_label.setText("-")
        self.format_label.setText("-")

        self.preview_stack.setCurrentWidget(self.empty_page)

        self.set_status(
            "empty",
            "NO IMAGE",
        )

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        apply_image_preview_style(self)
