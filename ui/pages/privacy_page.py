from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.styles.privacy_page_style import apply_privacy_page_style


class PrivacyPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("privacy_page")
        self.setup_ui()
        self.apply_styles()

    # =====================
    # MAIN LAYOUT
    # =====================

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("privacy_scroll")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.container = QWidget()
        self.container.setObjectName("privacy_container")

        self.content_layout = QVBoxLayout(self.container)
        self.content_layout.setContentsMargins(30, 28, 30, 30)
        self.content_layout.setSpacing(22)

        # Header
        self.content_layout.addWidget(self.create_header())

        # Information cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(18)

        cards_layout.addWidget(self.create_local_card(), 1)

        cards_layout.addWidget(self.create_data_card(), 1)

        self.content_layout.addLayout(cards_layout)

        # Lifecycle
        self.content_layout.addWidget(self.create_lifecycle_card())

        # Footer
        self.content_layout.addWidget(self.create_footer())

        self.content_layout.addStretch()

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
        label = QLabel(text)
        label.setObjectName(object_name)
        label.setWordWrap(word_wrap)

        return label

    def create_card(self, object_name="privacy_card"):
        card = QFrame()
        card.setObjectName(object_name)

        card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(28)
        shadow.setOffset(0, 7)
        shadow.setColor(QColor(0, 0, 0, 55))

        card.setGraphicsEffect(shadow)

        return card

    def add_check_item(self, layout, text):
        row = QHBoxLayout()
        row.setSpacing(12)

        icon = self.create_label(
            "✓",
            "privacy_check_icon",
            False,
        )
        icon.setFixedSize(28, 28)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = self.create_label(
            text,
            "privacy_item_text",
        )

        row.addWidget(
            icon,
            0,
            Qt.AlignmentFlag.AlignTop,
        )
        row.addWidget(label, 1)

        layout.addLayout(row)

    # =====================
    # HEADER
    # =====================

    def create_header(self):
        card = self.create_card("privacy_hero")

        layout = QHBoxLayout(card)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(24)

        left = QVBoxLayout()
        left.setSpacing(12)

        eyebrow = self.create_label(
            "PRIVACY & SECURITY",
            "privacy_eyebrow",
        )

        title = self.create_label(
            "Your images.\nYour control.",
            "privacy_hero_title",
        )

        description = self.create_label(
            "PixVault is built around local-first "
            "image processing. Your files are "
            "processed directly on your device, "
            "without requiring cloud uploads "
            "or external processing services.",
            "privacy_hero_description",
        )

        left.addWidget(eyebrow)
        left.addWidget(title)
        left.addWidget(description)

        right = QVBoxLayout()
        right.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right.setSpacing(12)

        status = self.create_label(
            "●  LOCAL-FIRST",
            "privacy_status",
            False,
        )
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        shield = self.create_label(
            "◇",
            "privacy_shield",
            False,
        )
        shield.setAlignment(Qt.AlignmentFlag.AlignCenter)

        status_text = self.create_label(
            "Designed for local processing",
            "privacy_status_text",
        )
        status_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        right.addWidget(status)
        right.addWidget(shield)
        right.addWidget(status_text)

        layout.addLayout(left, 3)
        layout.addLayout(right, 2)

        return card

    # =====================
    # LOCAL PROCESSING
    # =====================

    def create_local_card(self):
        card = self.create_card()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(14)

        badge = self.create_label(
            "01 / PROCESSING",
            "privacy_card_badge",
        )

        title = self.create_label(
            "Local Processing",
            "privacy_card_title",
        )

        description = self.create_label(
            "Image processing is designed to run directly on your device.",
            "privacy_card_description",
        )

        layout.addWidget(badge)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(12)

        items = [
            "Image processing runs locally",
            "Processing engines run on your device",
            "No external image transfer required",
            "Works without cloud dependency",
        ]

        for item in items:
            self.add_check_item(layout, item)

        layout.addStretch()

        return card

    # =====================
    # DATA HANDLING
    # =====================

    def create_data_card(self):
        card = self.create_card()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(14)

        badge = self.create_label(
            "02 / DATA OWNERSHIP",
            "privacy_card_badge",
        )

        title = self.create_label(
            "Data Handling",
            "privacy_card_title",
        )

        description = self.create_label(
            "Maintain control over your source images and output files.",
            "privacy_card_description",
        )

        layout.addWidget(badge)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(12)

        items = [
            "Source images remain under your control",
            "Output files are saved to your selected folder",
            "Processing history is stored locally",
            "You choose the output destination",
        ]

        for item in items:
            self.add_check_item(layout, item)

        layout.addStretch()

        return card

    # =====================
    # FILE LIFECYCLE
    # =====================

    def create_lifecycle_card(self):
        card = self.create_card()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(26, 24, 26, 26)
        layout.setSpacing(18)

        header = QVBoxLayout()
        header.setSpacing(7)

        badge = self.create_label(
            "03 / WORKFLOW",
            "privacy_card_badge",
        )

        title = self.create_label(
            "File Lifecycle",
            "privacy_card_title",
        )

        description = self.create_label(
            "A simple, transparent workflow from source image to final output.",
            "privacy_card_description",
        )

        header.addWidget(badge)
        header.addWidget(title)
        header.addWidget(description)

        layout.addLayout(header)

        # Horizontal workflow

        steps_layout = QHBoxLayout()
        steps_layout.setSpacing(12)

        steps = [
            (
                "01",
                "Select",
                "Choose your source image",
            ),
            (
                "02",
                "Process",
                "Image processing runs locally",
            ),
            (
                "03",
                "Clean Up",
                "Clean temporary processing files",
            ),
            (
                "04",
                "Export",
                "Save to your selected location",
            ),
        ]

        for number, title, description in steps:
            step = self.create_step(
                number,
                title,
                description,
            )
            steps_layout.addWidget(step, 1)

        layout.addLayout(steps_layout)

        return card

    # =====================
    # WORKFLOW STEP
    # =====================

    def create_step(
        self,
        number,
        title,
        description,
    ):
        step = QFrame()
        step.setObjectName("privacy_step")

        layout = QVBoxLayout(step)
        layout.setContentsMargins(16, 18, 16, 18)
        layout.setSpacing(9)

        number_label = self.create_label(
            number,
            "privacy_step_number",
            False,
        )

        title_label = self.create_label(
            title,
            "privacy_step_title",
        )

        description_label = self.create_label(
            description,
            "privacy_step_description",
        )

        layout.addWidget(number_label)
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addStretch()

        return step

    # =====================
    # FOOTER
    # =====================

    def create_footer(self):
        footer = QWidget()

        layout = QHBoxLayout(footer)
        layout.setContentsMargins(2, 6, 2, 6)

        left = self.create_label(
            "PIXVAULT  /  PRIVACY BY DESIGN",
            "privacy_footer_label",
        )

        right = self.create_label(
            "Your device. Your files. Your control.",
            "privacy_footer_text",
        )

        right.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(left)
        layout.addStretch()
        layout.addWidget(right)

        return footer

    # =====================
    # STYLING
    # =====================

    def apply_styles(self):
        apply_privacy_page_style(self)
