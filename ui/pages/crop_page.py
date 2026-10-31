"""PixVault image-cropping page.

Uses the same reusable widgets, responsive layout, and pvRole theme as
ConvertPage. Cropping behavior remains delegated to CropOptions and ImagePipeline.
"""

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
from ui.components.image_info_panel import ImageInfoPanel
from ui.components.image_list_widget import ImageListWidget
from ui.components.image_preview import ImagePreview
from ui.components.output_selector import OutputSelector
from ui.components.processing_options.common.format_support_info import (
    FormatSupportInfo,
)
from ui.components.processing_options.crop_options import CropOptions
from ui.pages.format_labels import JPEG_DISPLAY_LABEL, output_format_key
from ui.styles.pixvault_theme import apply_page_theme, role


class CropPage(QWidget):
    """Consistent, responsive cropping workflow for PixVault."""

    # Match the formats listed by FormatSupportInfo("crop"). The current batch
    # pipeline needs one explicit output format, even for keep-source batches.
    OUTPUT_FORMATS = [
        "Same as source",
        JPEG_DISPLAY_LABEL,
        "PNG",
        "WEBP",
        "BMP",
        "TIFF",
    ]
    SOURCE_FORMATS = {
        ".jpg": "JPEG",
        ".jpeg": "JPEG",
        ".png": "PNG",
        ".webp": "WEBP",
        ".bmp": "BMP",
        ".tif": "TIFF",
        ".tiff": "TIFF",
    }

    def __init__(self, image_service, batch_service):
        super().__init__()

        self.image_service = image_service
        self.batch_service = batch_service
        self.images = []
        self.output_folder = None
        self._processing_active = False
        self._cancel_requested = False

        self.setObjectName("crop_page")
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
        self.scroll_area.setObjectName("crop_scroll")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.container = role(QWidget(), "pageContainer")
        self.container.setObjectName("crop_container")
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(26, 26, 26, 30)
        self.layout.setSpacing(18)

        # HERO / FORMAT COMPATIBILITY
        self.layout.addWidget(self.create_header())
        self.format_support = FormatSupportInfo("crop")
        self.layout.addWidget(self.format_support)

        # 01 / IMPORT AND REVIEW
        self.layout.addWidget(
            self.create_section_header(
                "01",
                "Import & Organize",
                "Add images, manage the queue, and inspect selected files.",
            )
        )

        # DropArea already supports file/folder import; no ImageImporter needed.
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

        # PREVIEW & DETAILS: equal row height; no nested details scroll area.
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

        # 02 / CROP SETTINGS & OUTPUT
        self.layout.addWidget(
            self.create_section_header(
                "02",
                "Configure Crop",
                "Choose crop dimensions or proportions and an output folder.",
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

        # 03 / PROCESS & EXPORT
        self.layout.addWidget(
            self.create_section_header(
                "03",
                "Process & Export",
                "Crop the selected images and monitor export status.",
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
        heading.addWidget(self.text("PIXVAULT / CROP STUDIO", "eyebrow"))
        heading.addWidget(self.text("Crop Images", "heroTitle"))
        heading.addWidget(
            self.text(
                "Precisely crop images while keeping your files processed locally.",
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

        layout.addWidget(self.text("CROP CONFIGURATION", "eyebrow"))
        layout.addWidget(self.text("Crop Settings", "cardTitle"))
        layout.addWidget(
            self.text(
                "Choose a format, then set an aspect ratio, fixed size, "
                "percentage, or custom coordinates.",
                "description",
                True,
            )
        )
        layout.addSpacing(5)
        layout.addWidget(self.text("OUTPUT FORMAT", "fieldTitle"))

        self.format_box = role(PremiumComboBox(), "field")
        self.format_box.setObjectName("crop_format_box")
        self.format_box.setMinimumHeight(44)
        self.format_box.setCursor(Qt.CursorShape.PointingHandCursor)
        self.format_box.setAccessibleName("Crop output format")
        self.format_box.addItems(self.OUTPUT_FORMATS)
        layout.addWidget(self.format_box)

        self.format_hint = self.text("", "hint", True)
        layout.addWidget(self.format_hint)

        divider = role(QFrame(), "divider")
        divider.setFixedHeight(1)
        layout.addSpacing(5)
        layout.addWidget(divider)
        layout.addWidget(self.text("CROP OPTIONS", "fieldTitle"))
        layout.addWidget(
            self.text(
                "Aspect ratio, fixed dimensions, and percentage crop from the "
                "center. Custom coordinates use a top-left X/Y position.",
                "hint",
                True,
            )
        )

        self.crop_options = CropOptions()
        self.crop_options.reset()
        layout.addWidget(self.crop_options)
        layout.addStretch(0)
        return card

    def create_action_card(self):
        card = role(QFrame(), "card")
        self.action_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight, card)
        self.action_layout.setContentsMargins(20, 20, 20, 20)
        self.action_layout.setSpacing(18)

        summary = QVBoxLayout()
        summary.setSpacing(6)
        summary.addWidget(self.text("Ready to Crop?", "cardTitle"))
        self.queue_summary = self.text("Add images to begin.", "description", True)
        summary.addWidget(self.queue_summary)
        self.action_layout.addLayout(summary, 1)

        self.action_buttons = QHBoxLayout()
        self.action_buttons.setSpacing(10)
        self.cancel_button = role(QPushButton("Cancel Processing"), "dangerButton")
        self.start_button = role(QPushButton("Start Crop →"), "primaryButton")
        for button in (self.cancel_button, self.start_button):
            button.setMinimumHeight(46)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_button.hide()
        self.action_buttons.addWidget(self.cancel_button)
        self.action_buttons.addWidget(self.start_button)
        self.action_layout.addLayout(self.action_buttons)
        return card

    # =====================
    # SIGNALS & IMAGE QUEUE
    # =====================

    def connect_events(self):
        self.drop_area.files_dropped.connect(self.load_images)
        self.image_list.image_selected.connect(self.show_preview)
        self.image_list.images_changed.connect(self.on_images_changed)
        self.output_selector.output_changed.connect(self.set_output_folder)
        self.format_box.currentTextChanged.connect(self.change_format)
        self.start_button.clicked.connect(self.start_crop)
        self.cancel_button.clicked.connect(self.cancel_processing)

        # BatchService is shared between pages; handlers check _processing_active.
        self.batch_service.progress_changed.connect(self.on_batch_progress)
        self.batch_service.processing_finished.connect(self.crop_finished)
        self.batch_service.processing_error.connect(self.crop_error)

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

        existing = self.image_list.get_images()
        combined = list(dict.fromkeys(existing + incoming))
        if combined != existing:
            self.image_list.set_images(combined)

    def on_images_changed(self, images):
        self.images = [Path(image) for image in images]
        self.change_format(self.format_box.currentText())

        if not self.images:
            self.preview.clear()
            self.info_panel.clear()
            return

        current = self.preview.current_image
        if current not in self.images:
            current = self.images[0]
            self.show_preview(current)

        if hasattr(self.image_list, "select_image"):
            self.image_list.select_image(self.images.index(current), emit_signal=False)

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

    def source_format(self):
        """Return a format only if the entire queue shares a supported type."""
        if not self.images:
            return None
        formats = {
            self.SOURCE_FORMATS.get(Path(image).suffix.lower()) for image in self.images
        }
        if len(formats) == 1:
            return next(iter(formats))
        return None

    def selected_output_format(self):
        selection = self.format_box.currentText()
        return (
            self.source_format()
            if selection == "Same as source"
            else output_format_key(selection)
        )

    def change_format(self, _format_name):
        selected = self.format_box.currentText()
        output_format = self.selected_output_format()
        if selected == "Same as source":
            self.format_hint.setText(
                "Requires one supported source format in the batch. "
                "For mixed formats, choose an explicit output format."
            )
        else:
            self.format_hint.setText(
                f"All cropped images will be exported as {output_format}."
            )
        if output_format:
            self.crop_options.set_format(output_format)
        self.update_queue_state()

    def build_config(self):
        output_format = self.selected_output_format()
        if not output_format:
            raise ValueError(
                "Cannot use 'Same as source' for mixed or unsupported formats. "
                "Select one output format for this batch."
            )

        operation = dict(self.crop_options.get_settings())
        operation["type"] = "crop"

        mode = operation.get("mode")
        if mode not in {"aspect_ratio", "fixed", "percentage", "coordinates"}:
            raise ValueError("Please select a valid crop mode.")
        if mode in {"fixed", "coordinates"}:
            if operation.get("width", 0) <= 0 or operation.get("height", 0) <= 0:
                raise ValueError("Crop width and height must be positive.")
        elif mode == "percentage":
            if not 1 <= operation.get("value", 0) <= 100:
                raise ValueError("Crop percentage must be between 1 and 100.")

        return {
            "operations": [operation],
            "output": {"format": output_format, "suffix": "cropped"},
        }

    def update_queue_state(self):
        count = len(self.images)
        noun = "image" if count == 1 else "images"
        self.image_count_label.setText(
            f"{count} IMAGE" if count == 1 else f"{count} IMAGES"
        )
        if count == 0:
            self.queue_summary.setText(
                "Import images using the drop area to prepare a crop batch."
            )
            self.start_button.setText("Start Crop →")
        else:
            output = self.selected_output_format() or "choose output format"
            self.queue_summary.setText(
                f"{count} {noun} selected · Output format: {output}"
            )
            self.start_button.setText(f"Crop {count} {noun.title()} →")
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

    def start_crop(self):
        if self._processing_active:
            return
        self.images = self.image_list.get_images()

        if not self.images:
            QMessageBox.warning(
                self, "Crop Images", "Please import at least one image."
            )
            return
        if not self.output_folder:
            QMessageBox.warning(self, "Crop Images", "Please select an output folder.")
            return
        if self.batch_service.is_running():
            QMessageBox.warning(
                self,
                "Processing Busy",
                "Another processing task is running. Finish it before cropping.",
            )
            return

        unsupported = [
            Path(image).name
            for image in self.images
            if Path(image).suffix.lower() not in self.SOURCE_FORMATS
        ]
        if unsupported:
            QMessageBox.warning(
                self,
                "Unsupported Crop Input",
                "The crop workspace accepts JPEG, PNG, WEBP, BMP, and TIFF. "
                "Remove unsupported files from the queue: "
                + ", ".join(unsupported[:5])
                + (" ..." if len(unsupported) > 5 else ""),
            )
            return

        try:
            config = self.build_config()
        except ValueError as error:
            QMessageBox.warning(self, "Invalid Crop Settings", str(error))
            return

        try:
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
            self._cancel_requested = False
            self.set_workflow_status("failed", "FAILED")
            self.progress.failed(str(error))
            QMessageBox.critical(self, "Crop Error", str(error))

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

    def crop_finished(self, result):
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

    def crop_error(self, error):
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

    def apply_styles(self):
        apply_page_theme(self)
