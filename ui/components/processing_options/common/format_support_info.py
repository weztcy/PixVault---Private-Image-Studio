from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLayout,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

# =====================
# PREMIUM FORMAT CARD
# =====================
from ui.styles.processing_fields_style import apply_format_support_info_style


class FormatCard(QFrame):
    def __init__(self, format_name, parent=None):
        super().__init__(parent)

        self.format_name = format_name

        self.setObjectName("format_card")
        # Width adapts to the format label it contains; only the height is
        # kept fixed so every card in the strip stays the same size.
        self.setFixedHeight(46)
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Fixed,
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground,
            True,
        )

        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)

        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(9)

        # Accent indicator

        indicator = QLabel("◆")
        indicator.setObjectName("format_indicator")

        indicator.setFixedWidth(12)
        indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Format name

        name = QLabel(str(self.format_name).upper())

        name.setObjectName("format_name")

        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Never expand beyond the text itself, or the card would stretch
        # to fill the scroll area instead of hugging its content.
        name.setSizePolicy(
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Fixed,
        )

        layout.addWidget(indicator)
        layout.addWidget(name, 0)


# =====================
# FORMAT SUPPORT INFO
# =====================


class FormatSupportInfo(QWidget):
    SUPPORT_DATA = {
        "convert": [
            "JPG / JPEG",
            "PNG",
            "WEBP",
            "AVIF",
            "GIF",
            "BMP",
            "TIFF",
            "HEIC",
            "ICO",
            "SVG",
        ],
        "resize": [
            "JPG / JPEG",
            "PNG",
            "WEBP",
            "AVIF",
            "BMP",
            "TIFF",
            "HEIC",
        ],
        "crop": [
            "JPG / JPEG",
            "PNG",
            "WEBP",
            "BMP",
            "TIFF",
        ],
        "transform": [
            "JPG / JPEG",
            "PNG",
            "WEBP",
            "BMP",
            "TIFF",
        ],
        "compression": [
            "JPG / JPEG",
            "PNG",
            "WEBP",
            "TIFF",
        ],
        "dpi": [
            "JPG / JPEG",
            "PNG",
            "TIFF",
        ],
        "colorspace": [
            "JPG / JPEG",
            "PNG",
            "TIFF",
        ],
        "bitdepth": [
            "PNG",
            "TIFF",
        ],
        "metadata": [
            "JPG / JPEG",
            "TIFF",
            "HEIC",
        ],
    }

    # Accept alternative processor keys
    # without changing the original mapping.

    PROCESSOR_ALIASES = {
        "compress": "compression",
        "color_space": "colorspace",
        "bit_depth": "bitdepth",
    }

    def __init__(self, processor_name, parent=None):
        super().__init__(parent)

        self.processor_name = str(processor_name).strip().lower()

        self.setObjectName("format_support_info")

        self.setup_ui()
        self.apply_styles()
        self.refresh()

    # =====================
    # MAIN UI
    # =====================

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Premium container

        self.main_card = QFrame()
        self.main_card.setObjectName("format_support_card")

        self.main_card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        card_layout = QVBoxLayout(self.main_card)

        card_layout.setContentsMargins(18, 18, 18, 16)
        card_layout.setSpacing(14)

        # Header

        card_layout.addLayout(self.create_header())

        # Horizontal format browser

        card_layout.addLayout(self.create_format_browser())

        main_layout.addWidget(self.main_card)

    # =====================
    # HEADER
    # =====================

    def create_header(self):
        header = QHBoxLayout()
        header.setSpacing(12)

        # Header text

        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)

        eyebrow = QLabel("FORMAT COMPATIBILITY")

        eyebrow.setObjectName("support_eyebrow")

        title = QLabel("Supported Formats")

        title.setObjectName("support_title")

        description = QLabel("Image formats listed for this processing operation.")

        description.setObjectName("support_description")

        description.setWordWrap(True)

        text_layout.addWidget(eyebrow)
        text_layout.addWidget(title)
        text_layout.addWidget(description)

        # Format count badge

        self.count_label = QLabel("0 FORMATS")

        self.count_label.setObjectName("support_count")

        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.count_label.setMinimumHeight(32)

        header.addLayout(text_layout, 1)

        header.addWidget(
            self.count_label,
            0,
            Qt.AlignmentFlag.AlignTop,
        )

        return header

    # =====================
    # FORMAT BROWSER
    # =====================

    def create_format_browser(self):
        browser_layout = QHBoxLayout()

        browser_layout.setContentsMargins(0, 0, 0, 0)
        browser_layout.setSpacing(8)

        # =====================
        # SCROLL AREA
        # =====================

        self.scroll_area = QScrollArea()

        self.scroll_area.setObjectName("format_support_scroll")

        self.scroll_area.setWidgetResizable(True)

        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.scroll_area.setFixedHeight(76)

        self.scroll_area.setMinimumWidth(0)

        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # =====================
        # FORMATS CONTAINER
        # =====================

        self.container = QWidget()

        self.container.setObjectName("format_support_container")

        self.card_layout = QHBoxLayout(self.container)

        self.card_layout.setContentsMargins(4, 6, 4, 6)

        self.card_layout.setSpacing(10)

        self.card_layout.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        # Ensure the content retains its
        # minimum width so that horizontal
        # scrolling is available.

        self.card_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        self.scroll_area.setWidget(self.container)

        # =====================
        # ASSEMBLE BROWSER
        # =====================

        browser_layout.addWidget(
            self.scroll_area,
            1,
        )

        # =====================
        # SCROLLBAR SIGNALS
        # =====================

        scrollbar = self.scroll_area.horizontalScrollBar()

        return browser_layout

    # =====================
    # REFRESH FORMATS
    # =====================

    def refresh(self):
        # Remove old cards first.
        # Repeated refresh calls must not
        # create duplicate format cards.

        self.clear_cards()

        processor_key = self.PROCESSOR_ALIASES.get(
            self.processor_name,
            self.processor_name,
        )

        formats = self.SUPPORT_DATA.get(
            processor_key,
            [],
        )

        # Update counter

        count = len(formats)

        self.count_label.setText(
            f"{count} FORMAT" if count == 1 else f"{count} FORMATS"
        )

        # =====================
        # EMPTY STATE
        # =====================

        if not formats:
            empty_label = QLabel("No format information available for this operation.")

            empty_label.setObjectName("support_empty_label")

            empty_label.setWordWrap(True)

            self.card_layout.addWidget(empty_label)

        # =====================
        # CREATE FORMAT CARDS
        # =====================

        else:
            for fmt in formats:
                card = FormatCard(
                    fmt,
                    self.container,
                )

                self.card_layout.addWidget(card)

        # Push items to the left when
        # there is extra horizontal space.

        self.card_layout.addStretch(1)

        # Reset horizontal position.

        self.scroll_area.horizontalScrollBar().setValue(0)

    # =====================
    # CLEAR EXISTING CARDS
    # =====================

    def clear_cards(self):
        while self.card_layout.count():
            item = self.card_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.hide()
                widget.deleteLater()

    # =====================
    # HORIZONTAL SCROLL
    # =====================

    def scroll_formats(self, direction):
        scrollbar = self.scroll_area.horizontalScrollBar()

        scrollbar.setValue(scrollbar.value() + (int(direction) * 240))

    # =====================
    # OPTIONAL PROCESSOR UPDATE
    # =====================

    def set_processor(self, processor_name):
        self.processor_name = str(processor_name).strip().lower()

        self.refresh()

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        apply_format_support_info_style(self)
