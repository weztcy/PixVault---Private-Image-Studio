import sys
from pathlib import Path

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QIcon, QPainter, QPainterPath, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from services.batch_service import BatchService
from services.history_service import HistoryService
from services.image_service import ImageService
from ui.sidebar import Sidebar
from ui.styles.main_window_style import apply_main_window_style
from ui.workspace import Workspace


class MainWindow(QMainWindow):
    @staticmethod
    def resolve_app_icon():
        candidates = []
        if hasattr(sys, "_MEIPASS"):
            candidates.append(Path(sys._MEIPASS) / "icons" / "pixvault_icon.png")
        candidates.append(Path(__file__).resolve().parent.parent / "icons" / "pixvault_icon.png")
        candidates.append(Path("icons/pixvault_icon.png").resolve())
        if hasattr(sys, "executable"):
            candidates.append(Path(sys.executable).parent / "icons" / "pixvault_icon.png")
        for c in candidates:
            if c.exists():
                return c
        return None

    def __init__(self):
        super().__init__()

        self.setObjectName("pixvault_main_window")

        self.setWindowTitle("PixVault | Local Image Studio")

        icon_file = self.resolve_app_icon()
        if icon_file:
            self.setWindowIcon(QIcon(str(icon_file)))

        self.resize(1920, 1080)

        self.setup_services()
        self.setup_ui()
        self.apply_styles()

    # =====================
    # SERVICES
    # =====================

    def setup_services(self):
        self.image_service = ImageService()

        self.batch_service = BatchService()

        self.history_service = HistoryService()

    # =====================
    # MAIN UI
    # =====================

    def setup_ui(self):
        container = QWidget()
        container.setObjectName("main_container")

        main_layout = QVBoxLayout(container)

        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.setSpacing(0)

        # =====================
        # HEADER
        # =====================

        self.header = self.create_header()

        main_layout.addWidget(self.header)

        # =====================
        # CONTENT AREA
        # =====================

        content = QWidget()
        content.setObjectName("main_content")

        content_layout = QHBoxLayout(content)

        content_layout.setContentsMargins(0, 0, 0, 0)

        content_layout.setSpacing(0)

        # =====================
        # SIDEBAR
        # =====================

        self.sidebar = Sidebar()

        self.sidebar.setFixedWidth(238)

        self.sidebar.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding,
        )

        # =====================
        # WORKSPACE
        # =====================

        self.workspace = Workspace(
            self.image_service,
            self.batch_service,
            self.history_service,
        )

        self.workspace.setObjectName("main_workspace")

        self.workspace.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        # =====================
        # CONTENT LAYOUT
        # =====================

        content_layout.addWidget(self.sidebar)

        content_layout.addWidget(
            self.workspace,
            1,
        )

        main_layout.addWidget(
            content,
            1,
        )

        self.setCentralWidget(container)

        # =====================
        # NAVIGATION
        # =====================

        self.connect_navigation()

        # Keep sidebar active state synchronized
        # with workspace page changes.

        self.sidebar.bind_workspace(self.workspace)

    # =====================
    # PREMIUM HEADER
    # =====================

    def create_header(self):
        header = QFrame()

        header.setObjectName("main_header")

        header.setFixedHeight(76)

        layout = QHBoxLayout(header)

        layout.setContentsMargins(22, 0, 26, 0)

        layout.setSpacing(14)

        # =====================
        # BRAND ICON
        # =====================

        brand_icon = QLabel()
        brand_icon.setObjectName("main_brand_icon")
        brand_icon.setFixedSize(42, 42)
        brand_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_file = self.resolve_app_icon()
        if icon_file:
            src = QPixmap(str(icon_file))
            if not src.isNull():
                target = QPixmap(42, 42)
                target.fill(Qt.GlobalColor.transparent)
                painter = QPainter(target)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
                painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
                path = QPainterPath()
                path.addRoundedRect(QRectF(0, 0, 42, 42), 10, 10)
                painter.setClipPath(path)
                painter.drawPixmap(0, 0, 42, 42, src)
                painter.end()
                brand_icon.setPixmap(target)
            else:
                brand_icon.setText("◈")
        else:
            brand_icon.setText("◈")

        # =====================
        # BRAND INFORMATION
        # =====================

        brand_layout = QVBoxLayout()
        brand_layout.setContentsMargins(0, 0, 0, 0)
        brand_layout.setSpacing(0)
        brand_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        brand_title = QLabel("PIXVAULT")
        brand_title.setObjectName("main_brand_title")

        brand_subtitle = QLabel("LOCAL IMAGE STUDIO")
        brand_subtitle.setObjectName("main_brand_subtitle")

        brand_layout.addWidget(brand_title)
        brand_layout.addWidget(brand_subtitle)

        # =====================
        # HEADER RIGHT SIDE
        # =====================

        right_layout = QHBoxLayout()

        right_layout.setSpacing(16)

        right_layout.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        # Application information

        app_info = QVBoxLayout()
        app_info.setContentsMargins(0, 0, 0, 0)
        app_info.setSpacing(0)
        app_info.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        info_title = QLabel("Image Processing Workspace")
        info_title.setObjectName("main_header_info")
        info_title.setAlignment(Qt.AlignmentFlag.AlignRight)

        info_subtitle = QLabel("Private • Local • Secure")
        info_subtitle.setObjectName("main_header_subtitle")
        info_subtitle.setAlignment(Qt.AlignmentFlag.AlignRight)

        app_info.addWidget(info_title)
        app_info.addWidget(info_subtitle)

        # =====================
        # LOCAL STATUS
        # =====================

        status_card = self.create_status_card()

        right_layout.addLayout(app_info)

        right_layout.addWidget(status_card)

        # =====================
        # HEADER ASSEMBLY
        # =====================

        layout.addWidget(brand_icon)

        layout.addLayout(brand_layout)

        layout.addStretch()

        layout.addLayout(right_layout)

        return header

    # =====================
    # LOCAL STATUS CARD
    # =====================

    def create_status_card(self):
        card = QFrame()

        card.setObjectName("main_status_card")

        layout = QHBoxLayout(card)

        layout.setContentsMargins(14, 9, 14, 9)

        layout.setSpacing(10)

        # Status indicator

        indicator = QLabel("●")

        indicator.setObjectName("main_status_indicator")

        indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Status information

        text_layout = QVBoxLayout()

        text_layout.setSpacing(3)

        status_title = QLabel("LOCAL PROCESSING")

        status_title.setObjectName("main_status_title")

        status_description = QLabel("On-device operations")

        status_description.setObjectName("main_status_description")

        text_layout.addWidget(status_title)

        text_layout.addWidget(status_description)

        layout.addWidget(indicator)

        layout.addLayout(text_layout)

        return card

    # =====================
    # NAVIGATION
    # =====================

    def connect_navigation(self):
        routes = {
            "home": "home",
            "convert": "convert",
            "compress": "compress",
            "resize": "resize",
            "crop": "crop",
            "transform": "transform",
            "dpi": "dpi",
            "metadata": "metadata",
            "colorspace": "colorspace",
            "bitdepth": "bitdepth",
            "history": "history",
            "privacy": "privacy",
        }

        for button_name, page_name in routes.items():
            button = self.sidebar.buttons.get(button_name)

            if button is None:
                continue

            button.clicked.connect(
                lambda checked=False, name=page_name: self.workspace.show_page(name)
            )

    # =====================
    # PAGE NAVIGATION
    # =====================

    def show_page(self, page_name):
        self.workspace.show_page(page_name)

    # =====================
    # WINDOW CLOSE EVENT
    # =====================

    def closeEvent(self, event):
        if not self.batch_service.is_running():
            event.accept()
            return

        reply = QMessageBox.question(
            self,
            "Processing Running",
            "Batch processing is still running.\n\n"
            "Do you want to cancel processing "
            "and exit PixVault?",
            (QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No),
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.batch_service.cancel()

            event.accept()

        else:
            event.ignore()

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        apply_main_window_style(self)
