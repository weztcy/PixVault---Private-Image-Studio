from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import (
    QCursor,
    QDragEnterEvent,
    QDragLeaveEvent,
    QDragMoveEvent,
    QDropEvent,
)
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.styles.drop_area_style import apply_drop_area_style


class DropArea(QWidget):
    files_dropped = Signal(list)

    SUPPORTED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".avif",
        ".gif",
        ".bmp",
        ".tiff",
        ".tif",
        ".heic",
        ".heif",
        ".ico",
        ".svg",
    }

    def __init__(self):
        super().__init__()

        self.setObjectName("drop_area")
        self.setAcceptDrops(True)

        self.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground,
            True,
        )

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.setProperty("drag_active", False)

        self.setMinimumHeight(225)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        self.setup_ui()
        self.apply_styles()

    # =====================
    # MAIN USER INTERFACE
    # =====================

    def setup_ui(self):
        layout = QVBoxLayout(self)

        layout.setContentsMargins(20, 20, 20, 20)

        layout.setSpacing(10)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # =====================
        # UPLOAD ICON
        # =====================

        icon_container = QFrame()
        icon_container.setObjectName("drop_icon_container")

        icon_container.setFixedSize(56, 56)

        icon_layout = QVBoxLayout(icon_container)

        icon_layout.setContentsMargins(0, 0, 0, 0)

        self.upload_icon = QLabel("↥")
        self.upload_icon.setObjectName("drop_upload_icon")

        self.upload_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_layout.addWidget(self.upload_icon)

        # =====================
        # TITLE
        # =====================

        self.label = QLabel("Drag & Drop Images or Folders")

        self.label.setObjectName("drop_title")

        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label.setWordWrap(True)

        # =====================
        # DESCRIPTION
        # =====================

        self.description = QLabel(
            "Drop your files here, or choose images and folders from your device."
        )

        self.description.setObjectName("drop_description")

        self.description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.description.setWordWrap(True)

        # =====================
        # ACTION BUTTONS
        # =====================

        action_layout = QHBoxLayout()

        action_layout.setContentsMargins(0, 4, 0, 4)

        action_layout.setSpacing(10)

        self.browse_button = QPushButton("Browse Images")

        self.browse_button.setObjectName("drop_browse_button")

        self.browse_button.setMinimumHeight(38)

        self.browse_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.browse_button.clicked.connect(self.open_file_dialog)

        self.folder_button = QPushButton("Select Folder")

        self.folder_button.setObjectName("drop_folder_button")

        self.folder_button.setMinimumHeight(38)

        self.folder_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.folder_button.clicked.connect(self.open_folder_dialog)

        action_layout.addStretch()

        action_layout.addWidget(self.browse_button)

        action_layout.addWidget(self.folder_button)

        action_layout.addStretch()

        # =====================
        # SUPPORTED FORMATS
        # =====================

        self.formats_label = QLabel(
            "JPG / JPEG  ·  PNG  ·  WEBP  ·  AVIF  ·  "
            "GIF  ·  BMP  ·  TIFF  ·  "
            "HEIC  ·  HEIF  ·  ICO  ·  SVG"
        )

        self.formats_label.setObjectName("drop_formats")

        self.formats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formats_label.setWordWrap(True)

        # Labels should not intercept
        # mouse clicks or drag events.

        for widget in (
            icon_container,
            self.upload_icon,
            self.label,
            self.description,
            self.formats_label,
        ):
            widget.setAttribute(
                Qt.WidgetAttribute.WA_TransparentForMouseEvents,
                True,
            )

        # =====================
        # ASSEMBLE LAYOUT
        # =====================

        layout.addWidget(
            icon_container,
            0,
            Qt.AlignmentFlag.AlignHCenter,
        )

        layout.addWidget(self.label)

        layout.addWidget(self.description)

        layout.addLayout(action_layout)

        layout.addWidget(self.formats_label)

    # =====================
    # DRAG ACTIVE STATE
    # =====================

    def set_drag_active(self, active):
        active = bool(active)

        if self.property("drag_active") == active:
            return

        self.setProperty(
            "drag_active",
            active,
        )

        self.style().unpolish(self)
        self.style().polish(self)

        self.update()

        if active:
            self.label.setText("Release to Import Images")

            self.description.setText(
                "Your images will be added to the processing workspace."
            )

        else:
            self.label.setText("Drag & Drop Images or Folders")

            self.description.setText(
                "Drop your files here, or choose images and folders from your device."
            )

    # =====================
    # CLICK IMPORT
    # =====================

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.open_file_dialog()
            event.accept()
            return

        super().mousePressEvent(event)

    # =====================
    # OPEN IMAGE FILE DIALOG
    # =====================

    def open_file_dialog(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            str(Path.home()),
            (
                "Image Files "
                "(*.jpg *.jpeg *.png *.webp "
                "*.avif *.gif *.bmp *.tiff "
                "*.tif *.heic *.heif *.ico *.svg)"
            ),
        )

        if not files:
            return

        result = []

        for file in files:
            path = Path(file)

            if path.is_file() and self.is_supported_image(path):
                result.append(path)

        self.emit_files(result)

    # =====================
    # OPEN FOLDER DIALOG
    # =====================

    def open_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Image Folder",
            str(Path.home()),
            QFileDialog.Option.ShowDirsOnly,
        )

        if not folder:
            return

        folder_path = Path(folder)

        if not folder_path.is_dir():
            return

        files = self.scan_folder(folder_path)

        self.emit_files(files)

    # =====================
    # CHECK DRAG CONTENT
    # =====================

    def has_supported_content(self, mime_data):
        if not mime_data.hasUrls():
            return False

        for url in mime_data.urls():
            if not url.isLocalFile():
                continue

            path = Path(url.toLocalFile())

            if path.is_dir():
                return True

            if path.is_file() and self.is_supported_image(path):
                return True

        return False

    # =====================
    # DRAG ENTER
    # =====================

    def dragEnterEvent(
        self,
        event: QDragEnterEvent,
    ):
        if self.has_supported_content(event.mimeData()):
            event.acceptProposedAction()
            self.set_drag_active(True)
        else:
            event.ignore()
            self.set_drag_active(False)

    # =====================
    # DRAG MOVE
    # =====================

    def dragMoveEvent(
        self,
        event: QDragMoveEvent,
    ):
        if self.has_supported_content(event.mimeData()):
            event.acceptProposedAction()
        else:
            event.ignore()

    # =====================
    # DRAG LEAVE
    # =====================

    def dragLeaveEvent(
        self,
        event: QDragLeaveEvent,
    ):
        self.set_drag_active(False)
        event.accept()

    # =====================
    # DROP EVENT
    # =====================

    def dropEvent(
        self,
        event: QDropEvent,
    ):
        self.set_drag_active(False)

        if not self.has_supported_content(event.mimeData()):
            event.ignore()
            return

        files = []

        for url in event.mimeData().urls():
            if not url.isLocalFile():
                continue

            path = Path(url.toLocalFile())

            if path.is_file():
                if self.is_supported_image(path):
                    files.append(path)

            elif path.is_dir():
                files.extend(self.scan_folder(path))

        self.emit_files(files)

        event.acceptProposedAction()

    # =====================
    # SCAN FOLDER
    # =====================

    def scan_folder(self, folder):
        folder = Path(folder)

        if not folder.is_dir():
            return []

        result = []

        try:
            for file in folder.rglob("*"):
                if file.is_file() and self.is_supported_image(file):
                    result.append(file)

        except OSError:
            # Some directories may be inaccessible.
            # Avoid crashing the import interface.
            pass

        return result

    # =====================
    # VALIDATE IMAGE
    # =====================

    def is_supported_image(self, path):
        path = Path(path)

        return path.suffix.lower() in self.SUPPORTED_EXTENSIONS

    # =====================
    # EMIT IMPORTED FILES
    # =====================

    def emit_files(self, files):
        if not files:
            return

        # Remove duplicate paths while
        # preserving the original order.

        unique_files = list(dict.fromkeys(Path(file) for file in files))

        if unique_files:
            self.files_dropped.emit(unique_files)

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        apply_drop_area_style(self)
