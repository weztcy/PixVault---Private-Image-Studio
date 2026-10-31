from pathlib import Path

from PIL import Image
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.styles.image_info_panel_style import apply_image_info_panel_style


class ImageInfoPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.current_image = None

        self.setObjectName("image_info_panel")

        self.setup_ui()
        self.apply_styles()

        self.clear()

    # =====================
    # MAIN USER INTERFACE
    # =====================

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Scroll Area

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("image_info_scroll")

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # Main Container

        self.container = QWidget()
        self.container.setObjectName("image_info_container")

        layout = QVBoxLayout(self.container)

        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(16)

        # Header

        layout.addWidget(self.create_header())

        # Information Card

        self.info_box = QGroupBox()
        self.info_box.setObjectName("image_info_box")

        self.setup_info_card()

        layout.addWidget(self.info_box)

        # Footer

        layout.addWidget(self.create_footer())

        layout.addStretch()

        self.scroll_area.setWidget(self.container)

        main_layout.addWidget(self.scroll_area)

    # =====================
    # COMMON HELPERS
    # =====================

    def create_label(
        self,
        text,
        object_name,
        word_wrap=True,
    ):
        label = QLabel(str(text))

        label.setObjectName(object_name)
        label.setWordWrap(word_wrap)

        return label

    def create_card(self, object_name):
        card = QFrame()

        card.setObjectName(object_name)

        card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        return card

    # =====================
    # PREMIUM HEADER
    # =====================

    def create_header(self):
        header = self.create_card("image_info_header")

        layout = QHBoxLayout(header)

        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)

        # Icon

        icon_box = QFrame()
        icon_box.setObjectName("image_info_icon_box")

        icon_box.setFixedSize(46, 46)

        icon_layout = QVBoxLayout(icon_box)
        icon_layout.setContentsMargins(0, 0, 0, 0)

        icon = QLabel("◈")
        icon.setObjectName("image_info_icon")

        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_layout.addWidget(icon)

        # Header Text

        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)

        eyebrow = self.create_label(
            "IMAGE INSPECTOR",
            "image_info_eyebrow",
        )

        title = self.create_label(
            "Image Details",
            "image_info_title",
        )

        description = self.create_label(
            "Properties of the selected image",
            "image_info_description",
        )

        text_layout.addWidget(eyebrow)
        text_layout.addWidget(title)
        text_layout.addWidget(description)

        layout.addWidget(icon_box)
        layout.addLayout(text_layout, 1)

        return header

    # =====================
    # INFORMATION CARD
    # =====================

    def setup_info_card(self):
        layout = QVBoxLayout(self.info_box)

        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(20)

        # =====================
        # FILE OVERVIEW
        # =====================

        overview_layout = QVBoxLayout()
        overview_layout.setSpacing(9)

        overview_header = QHBoxLayout()
        overview_header.setSpacing(10)

        overview_title = self.create_label(
            "FILE OVERVIEW",
            "image_info_section_label",
        )

        self.status_label = self.create_label(
            "NO IMAGE",
            "image_info_status",
            False,
        )

        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        overview_header.addWidget(overview_title)
        overview_header.addStretch()
        overview_header.addWidget(self.status_label)

        self.name_label = self.create_label(
            "-",
            "image_info_filename",
        )

        self.name_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        overview_layout.addLayout(overview_header)

        overview_layout.addWidget(self.name_label)

        layout.addLayout(overview_layout)

        # Divider

        layout.addWidget(self.create_divider())

        # =====================
        # IMAGE STATISTICS
        # =====================

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(10)

        format_card, self.format_label = self.create_stat_card(
            "FORMAT",
            "image_info_format",
        )

        size_card, self.size_label = self.create_stat_card(
            "FILE SIZE",
            "image_info_size",
        )

        resolution_card, self.resolution_label = self.create_stat_card(
            "RESOLUTION",
            "image_info_resolution",
        )

        stats_layout.addWidget(format_card, 1)
        stats_layout.addWidget(size_card, 1)
        stats_layout.addWidget(resolution_card, 1)

        layout.addLayout(stats_layout)

        # =====================
        # IMAGE PROPERTIES
        # =====================

        properties_title = self.create_label(
            "IMAGE PROPERTIES",
            "image_info_section_label",
        )

        layout.addWidget(properties_title)

        properties_layout = QHBoxLayout()
        properties_layout.setSpacing(10)

        mode_card, self.mode_label = self.create_property_card("COLOR MODE")

        depth_card, self.depth_label = self.create_property_card("BIT DEPTH")

        properties_layout.addWidget(mode_card, 1)

        properties_layout.addWidget(depth_card, 1)

        layout.addLayout(properties_layout)

        # =====================
        # FILE LOCATION
        # =====================

        layout.addWidget(self.create_divider())

        location_header = QHBoxLayout()
        location_header.setSpacing(10)

        location_title = self.create_label(
            "FILE LOCATION",
            "image_info_section_label",
        )

        self.copy_button = QPushButton("Copy Path")

        self.copy_button.setObjectName("image_info_copy_button")

        self.copy_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.copy_button.setMinimumHeight(30)
        self.copy_button.setEnabled(False)

        self.copy_button.clicked.connect(self.copy_path)

        location_header.addWidget(location_title)

        location_header.addStretch()

        location_header.addWidget(self.copy_button)

        layout.addLayout(location_header)

        # Path Container

        path_card = self.create_card("image_info_path_card")

        path_layout = QVBoxLayout(path_card)

        path_layout.setContentsMargins(14, 12, 14, 12)

        self.path_label = self.create_label(
            "-",
            "image_info_path",
        )

        self.path_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        path_layout.addWidget(self.path_label)

        layout.addWidget(path_card)

        # =====================
        # ERROR MESSAGE
        # =====================

        self.error_label = self.create_label(
            "",
            "image_info_error",
        )

        self.error_label.setVisible(False)

        layout.addWidget(self.error_label)

    # =====================
    # STATISTICS CARD
    # =====================

    def create_stat_card(
        self,
        title,
        object_name,
    ):
        card = self.create_card("image_info_stat_card")

        card.setMinimumHeight(90)

        layout = QVBoxLayout(card)

        layout.setContentsMargins(13, 14, 13, 14)
        layout.setSpacing(10)

        title_label = self.create_label(
            title,
            "image_info_stat_title",
        )

        value_label = self.create_label(
            "-",
            "image_info_stat_value",
        )

        value_label.setProperty(
            "field_type",
            object_name,
        )

        value_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        layout.addStretch()

        return card, value_label

    # =====================
    # PROPERTY CARD
    # =====================

    def create_property_card(self, title):
        card = self.create_card("image_info_property_card")

        layout = QVBoxLayout(card)

        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(9)

        title_label = self.create_label(
            title,
            "image_info_property_title",
        )

        value_label = self.create_label(
            "-",
            "image_info_property_value",
        )

        value_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        return card, value_label

    # =====================
    # DIVIDER
    # =====================

    def create_divider(self):
        divider = QFrame()

        divider.setObjectName("image_info_divider")

        divider.setFrameShape(QFrame.Shape.HLine)

        divider.setFixedHeight(1)

        return divider

    # =====================
    # FOOTER
    # =====================

    def create_footer(self):
        footer = QWidget()

        layout = QHBoxLayout(footer)

        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(8)

        icon = self.create_label(
            "●",
            "image_info_footer_icon",
            False,
        )

        text = self.create_label(
            "Image properties are read from the selected file.",
            "image_info_footer_text",
        )

        layout.addWidget(icon)
        layout.addWidget(text, 1)

        return footer

    # =====================
    # STATUS MANAGEMENT
    # =====================

    def set_status(self, state, text):
        self.status_label.setText(str(text))

        self.status_label.setProperty(
            "image_state",
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

        self.current_image = Path(image_path).expanduser()

        self.load_information()

    # =====================
    # LOAD INFORMATION
    # =====================

    def load_information(self):
        if self.current_image is None:
            return

        file = self.current_image

        # Reset previous information

        self.reset_information()

        # Basic file information

        self.name_label.setText(file.name)

        self.path_label.setText(str(file))

        self.path_label.setToolTip(str(file))

        # Validate source

        if not file.is_file():
            self.show_error("The selected image file does not exist.")
            return

        try:
            # File size

            file_size = file.stat().st_size

            self.size_label.setText(self.format_size(file_size))

            # Image properties

            with Image.open(file) as image:
                image_format = image.format or "Unknown"

                self.format_label.setText(str(image_format).upper())

                self.resolution_label.setText(f"{image.width:,} × {image.height:,}")

                self.mode_label.setText(str(image.mode))

                self.depth_label.setText(self.get_bit_depth(image))

            # Update status

            self.set_status(
                "loaded",
                "IMAGE LOADED",
            )

            self.copy_button.setEnabled(True)

            self.error_label.hide()

        except Exception as error:
            self.show_error(str(error))

    # =====================
    # ERROR HANDLING
    # =====================

    def show_error(self, message):
        self.set_status(
            "error",
            "UNAVAILABLE",
        )

        self.error_label.setText(f"Unable to read image: {message}")

        self.error_label.show()

        self.copy_button.setEnabled(self.current_image is not None)

    # =====================
    # BIT DEPTH
    # =====================

    def get_bit_depth(self, image):
        mode = str(image.mode)

        mode_depth = {
            "1": 1,
            "L": 8,
            "LA": 8,
            "P": 8,
            "PA": 8,
            "RGB": 8,
            "RGBA": 8,
            "RGBX": 8,
            "CMYK": 8,
            "YCbCr": 8,
            "HSV": 8,
            "LAB": 8,
            "I": 32,
            "F": 32,
        }

        # Pillow 16-bit integer modes

        if mode.startswith("I;16"):
            return "16 bit"

        depth = mode_depth.get(mode)

        if depth is None:
            return "Unknown"

        return f"{depth} bit"

    # =====================
    # FORMAT FILE SIZE
    # =====================

    def format_size(self, size):
        units = [
            "B",
            "KB",
            "MB",
            "GB",
        ]

        value = float(size)

        for unit in units:
            if value < 1024:
                return f"{value:.2f} {unit}"

            value /= 1024

        return f"{value:.2f} TB"

    # =====================
    # COPY FILE PATH
    # =====================

    def copy_path(self):
        if self.current_image is None:
            return

        clipboard = QApplication.clipboard()

        if clipboard is None:
            return

        clipboard.setText(str(self.current_image))

        self.copy_button.setText("Copied ✓")

    # =====================
    # RESET DISPLAY
    # =====================

    def reset_information(self):
        self.name_label.setText("-")
        self.path_label.setText("-")
        self.format_label.setText("-")
        self.size_label.setText("-")
        self.resolution_label.setText("-")
        self.mode_label.setText("-")
        self.depth_label.setText("-")

        self.path_label.setToolTip("")

        self.copy_button.setText("Copy Path")

        self.copy_button.setEnabled(False)

        self.error_label.clear()
        self.error_label.hide()

    # =====================
    # CLEAR IMAGE
    # =====================

    def clear(self):
        self.current_image = None

        self.reset_information()

        self.set_status(
            "empty",
            "NO IMAGE",
        )

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        apply_image_info_panel_style(self)
