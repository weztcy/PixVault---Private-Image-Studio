from PySide6.QtWidgets import QStackedWidget

from ui.pages.bitdepth_page import BitDepthPage
from ui.pages.colorspace_page import ColorSpacePage
from ui.pages.compress_page import CompressPage
from ui.pages.convert_page import ConvertPage
from ui.pages.crop_page import CropPage
from ui.pages.dpi_page import DPIPage
from ui.pages.history_page import HistoryPage
from ui.pages.home_page import HomePage
from ui.pages.metadata_page import MetadataPage
from ui.pages.privacy_page import PrivacyPage
from ui.pages.resize_page import ResizePage
from ui.pages.transform_page import TransformPage


class Workspace(QStackedWidget):
    def __init__(
        self,
        image_service,
        batch_service,
        history_service,
    ):
        super().__init__()

        if image_service is None:
            raise ValueError("ImageService is required")

        if batch_service is None:
            raise ValueError("BatchService is required")

        if history_service is None:
            raise ValueError("HistoryService is required")

        self.image_service = image_service
        self.batch_service = batch_service
        self.history_service = history_service

        self.pages = {}

        self.setup_pages()

    # =====================
    # INITIALIZE PAGES
    # =====================

    def setup_pages(self):
        self.register_main_pages()
        self.register_tool_pages()
        self.register_system_pages()

        self.show_page("home")

    # =====================
    # MAIN
    # =====================

    def register_main_pages(self):
        self.add_page(
            "home",
            HomePage(),
        )

    # =====================
    # PROCESSING TOOLS
    # =====================

    def register_tool_pages(self):
        tools = {
            "convert": ConvertPage(
                self.image_service,
                self.batch_service,
            ),
            "compress": CompressPage(
                self.image_service,
                self.batch_service,
            ),
            "resize": ResizePage(
                self.image_service,
                self.batch_service,
            ),
            "crop": CropPage(
                self.image_service,
                self.batch_service,
            ),
            "transform": TransformPage(
                self.image_service,
                self.batch_service,
            ),
            "dpi": DPIPage(
                self.image_service,
                self.batch_service,
            ),
            "metadata": MetadataPage(
                self.image_service,
                self.batch_service,
            ),
            "colorspace": ColorSpacePage(
                self.image_service,
                self.batch_service,
            ),
            "bitdepth": BitDepthPage(
                self.image_service,
                self.batch_service,
            ),
        }

        for name, page in tools.items():
            self.add_page(name, page)

    # =====================
    # SYSTEM
    # =====================

    def register_system_pages(self):
        self.add_page(
            "history",
            HistoryPage(self.history_service),
        )

        self.add_page(
            "privacy",
            PrivacyPage(),
        )

    # =====================
    # PAGE MANAGEMENT
    # =====================

    def add_page(self, name, widget):
        if name in self.pages:
            return

        if widget is None:
            raise ValueError(f"Invalid page widget: {name}")

        self.pages[name] = widget
        self.addWidget(widget)

    def show_page(self, name):
        page = self.pages.get(name)

        if page is not None:
            self.setCurrentWidget(page)

    def get_page(self, name):
        return self.pages.get(name)
