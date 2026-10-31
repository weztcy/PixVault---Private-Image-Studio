from pathlib import Path

from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import (
    QBoxLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.components.drop_area import DropArea
from ui.components.export_progress import ExportProgress
from ui.components.format_options.common.dropdown_field import PremiumComboBox
from ui.components.format_options.format_options_panel import FormatOptionsPanel
from ui.components.image_info_panel import ImageInfoPanel
from ui.components.image_list_widget import ImageListWidget
from ui.components.image_preview import ImagePreview
from ui.components.output_selector import OutputSelector
from ui.components.processing_options.common.format_support_info import (
    FormatSupportInfo,
)
from ui.pages.format_labels import JPEG_DISPLAY_LABEL, output_format_key
from ui.styles.pixvault_theme import apply_page_theme, role


class ConvertPage(QWidget):
    OUTPUT_FORMATS = [
        JPEG_DISPLAY_LABEL,
        "PNG",
        "WEBP",
        "AVIF",
        "GIF",
        "BMP",
        "TIFF",
        "HEIC",
        "ICO",
        "SVG",
    ]

    def __init__(self, image_service, batch_service):
        super().__init__()
        self.image_service = image_service
        self.batch_service = batch_service
        self.images = []
        self.output_folder = None
        self.format_settings = {}
        self._processing_active = False
        self._cancel_requested = False

        self.setObjectName("convert_page")
        role(self, "page")

        self.setup_ui()
        self.apply_styles()
        self.connect_events()
        self.change_format(self.format_box.currentText())
        self.update_queue_state()
        self.update_responsive_layout()

    # =====================
    # WIDGET HELPERS
    # =====================

    def text(self, content, style_role, wrap=False):
        label = role(QLabel(str(content)), style_role)
        label.setWordWrap(wrap)
        label.setTextFormat(Qt.TextFormat.PlainText)
        label.setMinimumWidth(0)
        return label

    def setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.scroll_area = role(QScrollArea(), "pageScroll")
        self.scroll_area.setObjectName("convert_scroll")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.container = role(QWidget(), "pageContainer")
        self.container.setObjectName("convert_container")
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(26, 26, 26, 30)
        self.layout.setSpacing(18)

        self.layout.addWidget(self.create_header())
        self.format_support = FormatSupportInfo("convert")
        self.layout.addWidget(self.format_support)

        # 01 / IMPORT AND REVIEW
        self.layout.addWidget(
            self.create_section_header(
                "01",
                "Import & Organize",
                "Add images, manage the queue, and inspect selected files.",
            )
        )

        # DropArea already supports images and folders.
        # No ImageImporter instance is needed.
        self.drop_area = DropArea()
        self.image_list = ImageListWidget()
        self.drop_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.image_list.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.import_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.import_layout.setSpacing(16)
        self.import_layout.addWidget(self.drop_area, 4)
        self.import_layout.addWidget(self.image_list, 6)
        self.layout.addLayout(self.import_layout)

        # SAME-HEIGHT PREVIEW / IMAGE DETAILS ROW
        # The details component has no nested scrollbar.
        # Both widgets fill the height of this single horizontal row.
        self.preview = ImagePreview()
        self.info_panel = ImageInfoPanel()
        self.preview.setMinimumWidth(0)
        self.info_panel.setMinimumWidth(0)
        self.preview.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.info_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.preview_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.preview_layout.setSpacing(16)
        self.preview_layout.addWidget(self.preview, 6)
        self.preview_layout.addWidget(self.info_panel, 4)
        self.layout.addLayout(self.preview_layout)

        # 02 / CONVERSION SETTINGS
        self.layout.addWidget(
            self.create_section_header(
                "02",
                "Configure Conversion",
                "Choose a format, customize its options, and select an output folder.",
            )
        )
        self.settings_box = self.create_settings_card()
        self.output_selector = OutputSelector()
        self.output_folder = self.output_selector.get_output_folder()

        self.settings_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.settings_layout.setSpacing(16)
        self.settings_layout.addWidget(self.settings_box, 6, Qt.AlignmentFlag.AlignTop)

        self.settings_layout.addWidget(
            self.output_selector, 5, Qt.AlignmentFlag.AlignTop
        )
        self.layout.addLayout(self.settings_layout)

        # 03 / EXPORT
        self.layout.addWidget(
            self.create_section_header(
                "03",
                "Process & Export",
                "Convert the collection and monitor the export status.",
            )
        )
        self.layout.addWidget(self.create_action_card())
        self.progress = ExportProgress()
        self.layout.addWidget(self.progress)
        self.layout.addStretch(0)

        self.scroll_area.setWidget(self.container)
        self.scroll_area.viewport().installEventFilter(self)
        root.addWidget(self.scroll_area)

    def create_header(self):
        hero = role(QFrame(), "hero")
        layout = QHBoxLayout(hero)
        layout.setContentsMargins(26, 24, 26, 24)
        layout.setSpacing(18)

        heading = QVBoxLayout()
        heading.setSpacing(8)
        heading.addWidget(self.text("PIXVAULT / CONVERSION STUDIO", "eyebrow"))
        heading.addWidget(self.text("Convert Images", "heroTitle"))
        heading.addWidget(
            self.text(
                "Transform images into your preferred format with local processing.",
                "heroDescription",
                True,
            )
        )
        layout.addLayout(heading, 1)

        badges = QVBoxLayout()
        badges.setSpacing(10)
        self.workflow_badge = self.text("READY", "statusBadge")
        self.workflow_badge.setProperty("state", "ready")
        self.workflow_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_count_label = self.text("0 IMAGES", "countBadge")
        self.image_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badges.addWidget(self.workflow_badge)
        badges.addWidget(self.image_count_label)
        layout.addLayout(badges)
        return hero

    def create_section_header(self, number, title, description):
        section = QWidget()
        layout = QHBoxLayout(section)
        layout.setContentsMargins(2, 6, 2, 2)
        layout.setSpacing(14)
        badge = self.text(number, "sectionNumber")
        badge.setFixedSize(40, 40)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading = QVBoxLayout()
        heading.setSpacing(4)
        heading.addWidget(self.text(title, "sectionTitle"))
        heading.addWidget(self.text(description, "sectionDescription", True))
        layout.addWidget(badge)
        layout.addLayout(heading, 1)
        return section

    def create_settings_card(self):
        card = role(QFrame(), "card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(13)
        layout.addWidget(self.text("ENCODER CONFIGURATION", "eyebrow"))
        layout.addWidget(self.text("Conversion Settings", "cardTitle"))
        layout.addWidget(
            self.text(
                "Customize the output format and its encoding settings.",
                "description",
                True,
            )
        )
        layout.addSpacing(5)
        layout.addWidget(self.text("TARGET FORMAT", "fieldTitle"))

        self.format_box = role(PremiumComboBox(), "field")
        self.format_box.setObjectName("convert_format_box")
        self.format_box.setMinimumHeight(44)
        self.format_box.setCursor(Qt.CursorShape.PointingHandCursor)
        self.format_box.setAccessibleName("Target image format")
        self.format_box.addItems(self.OUTPUT_FORMATS)
        layout.addWidget(self.format_box)

        divider = role(QFrame(), "divider")
        divider.setFixedHeight(1)
        layout.addSpacing(5)
        layout.addWidget(divider)
        layout.addWidget(self.text("FORMAT OPTIONS", "fieldTitle"))
        layout.addWidget(
            self.text(
                "Options automatically follow the selected format.",
                "hint",
                True,
            )
        )
        self.format_options = FormatOptionsPanel()
        layout.addWidget(self.format_options)
        layout.addStretch(0)
        return card

    def create_action_card(self):
        card = role(QFrame(), "card")
        self.action_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight, card)
        self.action_layout.setContentsMargins(20, 20, 20, 20)
        self.action_layout.setSpacing(18)

        summary = QVBoxLayout()
        summary.setSpacing(6)
        summary.addWidget(self.text("Ready to Convert?", "cardTitle"))
        self.queue_summary = self.text("Add images to begin.", "description", True)
        summary.addWidget(self.queue_summary)
        self.action_layout.addLayout(summary, 1)

        self.action_buttons = QHBoxLayout()
        self.action_buttons.setSpacing(10)
        self.cancel_button = role(QPushButton("Cancel Processing"), "dangerButton")
        self.start_button = role(QPushButton("Start Conversion →"), "primaryButton")

        for button in (self.cancel_button, self.start_button):
            button.setMinimumHeight(46)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_button.hide()
        self.action_buttons.addWidget(self.cancel_button)
        self.action_buttons.addWidget(self.start_button)
        self.action_layout.addLayout(self.action_buttons)
        return card

    # =====================
    # SIGNALS AND IMAGE QUEUE
    # =====================

    def connect_events(self):
        self.drop_area.files_dropped.connect(self.load_images)
        self.image_list.image_selected.connect(self.show_preview)
        self.image_list.images_changed.connect(self.on_images_changed)
        self.output_selector.output_changed.connect(self.set_output_folder)
        self.format_box.currentTextChanged.connect(self.change_format)
        self.format_options.settings_changed.connect(self.update_format_settings)
        self.start_button.clicked.connect(self.start_convert)
        self.cancel_button.clicked.connect(self.cancel_processing)
        self.batch_service.progress_changed.connect(self.on_batch_progress)
        self.batch_service.processing_finished.connect(self.convert_finished)
        self.batch_service.processing_error.connect(self.convert_error)

    def change_format(self, format_name):
        self.format_options.set_format(output_format_key(format_name))
        self.format_options.reset()
        self.format_settings = self.format_options.get_settings()
        self.update_queue_state()

    def update_format_settings(self, settings):
        self.format_settings = dict(settings) if isinstance(settings, dict) else {}

    def load_images(self, images):
        """Append imported files without duplicating existing queue entries."""
        if not images or self._processing_active:
            return
        incoming = []
        for image in images:
            try:
                file = Path(image).expanduser()
                if file.is_file():
                    incoming.append(file)
            except (TypeError, ValueError, OSError):
                continue
        combined = list(dict.fromkeys(self.image_list.get_images() + incoming))
        if combined != self.image_list.get_images():
            self.image_list.set_images(combined)

    def on_images_changed(self, images):
        self.images = [Path(image) for image in images]
        self.update_queue_state()

        if not self.images:
            self.preview.clear()
            self.info_panel.clear()
            return

        current = self.preview.current_image
        if current not in self.images:
            current = self.images[0]
            self.show_preview(current)

        # The premium ImageListWidget supports visual selection.
        if hasattr(self.image_list, "select_image"):
            index = self.images.index(current)
            self.image_list.select_image(index, emit_signal=False)

    def show_preview(self, image):
        if not image:
            self.preview.clear()
            self.info_panel.clear()
            return
        path = Path(image)
        self.preview.set_image(path)
        self.info_panel.set_image(path)

    def set_output_folder(self, folder):
        self.output_folder = Path(folder) if folder else None
        self.update_queue_state()

    def build_config(self):
        self.format_settings = self.format_options.get_settings()
        return {
            "operations": [{"type": "convert"}],
            "output": {
                "format": output_format_key(self.format_box.currentText()),
                "options": self.format_settings.copy(),
            },
        }

    def update_queue_state(self):
        count = len(self.images)
        noun = "image" if count == 1 else "images"
        self.image_count_label.setText(
            f"{count} IMAGE" if count == 1 else f"{count} IMAGES"
        )

        if count == 0:
            self.queue_summary.setText(
                "Import images using the drop area to prepare a conversion batch."
            )
            self.start_button.setText("Start Conversion →")
        else:
            self.queue_summary.setText(
                f"{count} {noun} selected · Output format: {self.format_box.currentText()}"
            )
            self.start_button.setText(f"Convert {count} {noun.title()} →")
        self.start_button.setEnabled(count > 0 and not self._processing_active)

    def set_workflow_status(self, state, text):
        self.workflow_badge.setText(str(text))
        self.workflow_badge.setProperty("state", str(state))
        self.workflow_badge.style().unpolish(self.workflow_badge)
        self.workflow_badge.style().polish(self.workflow_badge)
        self.workflow_badge.update()

    def set_processing_state(self, running):
        self._processing_active = bool(running)
        enabled = not self._processing_active
        for widget in (
            self.drop_area,
            self.image_list,
            self.settings_box,
            self.output_selector,
        ):
            widget.setEnabled(enabled)
        self.cancel_button.setVisible(self._processing_active)
        self.cancel_button.setEnabled(self._processing_active)
        self.update_queue_state()

    # =====================
    # BATCH PROCESSING
    # =====================

    def start_convert(self):
        if self._processing_active:
            return
        self.images = self.image_list.get_images()

        if not self.images:
            QMessageBox.warning(
                self, "Convert Images", "Please import at least one image."
            )
            return
        if not self.output_folder:
            QMessageBox.warning(
                self, "Convert Images", "Please select an output folder."
            )
            return
        if self.batch_service.is_running():
            QMessageBox.warning(
                self,
                "Processing Busy",
                "Another processing task is running. Finish it before converting.",
            )
            return

        try:
            config = self.build_config()
            files = self.images.copy()
            self._cancel_requested = False
            self.progress.reset()
            self.progress.set_output_folder(self.output_folder)
            self.set_processing_state(True)
            self.set_workflow_status("processing", "PROCESSING")
            self.progress.set_status("processing", "Starting...")
            self.batch_service.start_batch(files, self.output_folder, config)
        except Exception as error:
            self.set_processing_state(False)
            self.set_workflow_status("failed", "FAILED")
            self.progress.failed(str(error))
            QMessageBox.critical(self, "Conversion Error", str(error))

    def on_batch_progress(self, current, total, filename, status):
        if not self._processing_active:
            return
        self.progress.update_progress(current, total, filename, status)
        if self._cancel_requested:
            self.progress.set_status("cancelled", "Cancelling...")

    def cancel_processing(self):
        if not self._processing_active:
            return
        self._cancel_requested = True
        self.cancel_button.setEnabled(False)
        self.set_workflow_status("cancelled", "CANCELLING")
        self.progress.set_status("cancelled", "Cancelling...")
        try:
            self.batch_service.cancel()
        except Exception as error:
            self._cancel_requested = False
            self.cancel_button.setEnabled(True)
            self.set_workflow_status("processing", "PROCESSING")
            self.progress.set_status("processing", "Processing")
            QMessageBox.critical(self, "Cancellation Error", str(error))

    def convert_finished(self, result):
        if not self._processing_active:
            return
        result = result if isinstance(result, dict) else {}
        successes = result.get("success") or []
        failures = result.get("failed") or []
        cancelled = bool(result.get("cancelled", False))
        self.set_processing_state(False)
        self._cancel_requested = False

        if cancelled:
            self.set_workflow_status("cancelled", "CANCELLED")
            self.progress.set_status("cancelled", "Cancelled")
            self.progress.file_label.setText("Processing was cancelled.")
        elif failures:
            self.set_workflow_status("failed", "NEEDS ATTENTION")
            self.progress.set_status("failed", "Finished with errors")
            self.progress.file_label.setText(
                f"{len(successes)} successful, {len(failures)} failed."
            )
        else:
            self.set_workflow_status("completed", "COMPLETED")
            self.progress.finished()

    def convert_error(self, error):
        if not self._processing_active:
            return
        self.set_processing_state(False)
        self._cancel_requested = False
        self.set_workflow_status("failed", "FAILED")
        self.progress.failed(str(error))

    # =====================
    # RESPONSIVE LAYOUT
    # =====================

    def eventFilter(self, watched, event):
        if (
            watched is self.scroll_area.viewport()
            and event.type() == QEvent.Type.Resize
        ):
            self.update_responsive_layout()
        return super().eventFilter(watched, event)

    def update_responsive_layout(self):
        if not hasattr(self, "settings_layout"):
            return
        width = self.scroll_area.viewport().width()

        # A single row makes the Preview and Details exactly as tall
        # as the tallest item. They only stack in narrow windows.
        direction = (
            QBoxLayout.Direction.LeftToRight
            if width >= 960
            else QBoxLayout.Direction.TopToBottom
        )
        for layout in (
            self.import_layout,
            self.preview_layout,
            self.settings_layout,
        ):
            if layout.direction() != direction:
                layout.setDirection(direction)

        action_direction = (
            QBoxLayout.Direction.LeftToRight
            if width >= 620
            else QBoxLayout.Direction.TopToBottom
        )
        if self.action_layout.direction() != action_direction:
            self.action_layout.setDirection(action_direction)

    # Existing method retained; styles are owned by ui.styles.
    def apply_styles(self):
        apply_page_theme(self)
