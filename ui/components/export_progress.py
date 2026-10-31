import os
from pathlib import Path

from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.styles.export_progress_style import apply_export_progress_style


class ExportProgress(QWidget):
    open_folder_requested = Signal()

    def __init__(self):
        super().__init__()

        self.output_folder = None

        self.setObjectName("export_progress_widget")

        self.setup_ui()
        self.apply_styles()

        self.set_status("ready", "Ready")

    # =====================
    # MAIN USER INTERFACE
    # =====================

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Main card

        self.container = QFrame()
        self.container.setObjectName("export_progress_card")

        self.container.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(18)

        # =====================
        # HEADER
        # =====================

        header = QHBoxLayout()
        header.setSpacing(12)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(6)

        eyebrow = QLabel("EXPORT WORKFLOW")
        eyebrow.setObjectName("export_eyebrow")

        title = QLabel("Export Progress")
        title.setObjectName("export_title")

        description = QLabel("Monitor image processing and export activity.")
        description.setObjectName("export_description")
        description.setWordWrap(True)

        title_layout.addWidget(eyebrow)
        title_layout.addWidget(title)
        title_layout.addWidget(description)

        # =====================
        # STATUS BADGE
        # =====================

        self.status_badge = QFrame()
        self.status_badge.setObjectName("export_status_badge")

        badge_layout = QHBoxLayout(self.status_badge)
        badge_layout.setContentsMargins(12, 7, 12, 7)
        badge_layout.setSpacing(8)

        self.status_indicator = QLabel("●")
        self.status_indicator.setObjectName("export_status_indicator")

        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("export_status_text")

        badge_layout.addWidget(self.status_indicator)
        badge_layout.addWidget(self.status_label)

        header.addLayout(title_layout, 1)
        header.addWidget(
            self.status_badge,
            0,
            Qt.AlignmentFlag.AlignTop,
        )

        layout.addLayout(header)

        # =====================
        # PROGRESS SECTION
        # =====================

        progress_header = QHBoxLayout()
        progress_header.setSpacing(10)

        progress_title = QLabel("OVERALL PROGRESS")
        progress_title.setObjectName("export_section_label")

        self.percentage_label = QLabel("0%")
        self.percentage_label.setObjectName("export_percentage")

        self.percentage_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        progress_header.addWidget(progress_title)
        progress_header.addStretch()
        progress_header.addWidget(self.percentage_label)

        # Progress bar

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("export_progress_bar")

        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(12)

        self.progress_bar.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        layout.addLayout(progress_header)
        layout.addWidget(self.progress_bar)

        # =====================
        # FILE INFORMATION
        # =====================

        information_layout = QHBoxLayout()
        information_layout.setSpacing(12)

        # Current file

        file_card = QFrame()
        file_card.setObjectName("export_info_card")

        file_layout = QVBoxLayout(file_card)
        file_layout.setContentsMargins(14, 12, 14, 12)
        file_layout.setSpacing(8)

        file_title = QLabel("CURRENT FILE")
        file_title.setObjectName("export_info_title")

        self.file_label = QLabel("File: -")
        self.file_label.setObjectName("export_file_label")

        self.file_label.setWordWrap(True)
        self.file_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        file_layout.addWidget(file_title)
        file_layout.addWidget(self.file_label)

        # File counter

        counter_card = QFrame()
        counter_card.setObjectName("export_info_card")

        counter_layout = QVBoxLayout(counter_card)

        counter_layout.setContentsMargins(14, 12, 14, 12)
        counter_layout.setSpacing(8)

        counter_title = QLabel("FILES PROCESSED")
        counter_title.setObjectName("export_info_title")

        self.counter_label = QLabel("0 / 0")
        self.counter_label.setObjectName("export_counter_label")

        counter_layout.addWidget(counter_title)
        counter_layout.addWidget(self.counter_label)

        # Parallel Engine card

        engine_card = QFrame()
        engine_card.setObjectName("export_info_card")

        engine_layout = QVBoxLayout(engine_card)
        engine_layout.setContentsMargins(14, 12, 14, 12)
        engine_layout.setSpacing(8)

        engine_title = QLabel("PROCESSING ENGINE")
        engine_title.setObjectName("export_info_title")

        cpu_cores = os.cpu_count() or 4
        self.engine_label = QLabel(f"Multi-Core ({cpu_cores} Cores)")
        self.engine_label.setObjectName("export_counter_label")

        engine_layout.addWidget(engine_title)
        engine_layout.addWidget(self.engine_label)

        information_layout.addWidget(file_card, 4)
        information_layout.addWidget(counter_card, 2)
        information_layout.addWidget(engine_card, 3)

        layout.addLayout(information_layout)

        # =====================
        # OUTPUT SECTION
        # =====================

        footer = QHBoxLayout()
        footer.setSpacing(12)

        footer_text = QLabel("Output files are saved to your selected folder.")
        footer_text.setObjectName("export_footer_text")
        footer_text.setWordWrap(True)

        # Open output folder

        self.open_button = QPushButton("Open Output Folder  ↗")

        self.open_button.setObjectName("export_open_button")

        self.open_button.setMinimumHeight(40)
        self.open_button.setEnabled(False)

        self.open_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.open_button.clicked.connect(self.open_folder)

        footer.addWidget(footer_text, 1)
        footer.addWidget(self.open_button)

        layout.addLayout(footer)

        # Assemble main component

        main_layout.addWidget(self.container)

    # =====================
    # STATUS MANAGEMENT
    # =====================

    def set_engine_info(self, text):
        if hasattr(self, "engine_label"):
            self.engine_label.setText(str(text))

    def set_status(self, state, text):
        self.status_label.setText(str(text))

        widgets = (
            self.status_badge,
            self.status_indicator,
            self.status_label,
            self.progress_bar,
        )

        for widget in widgets:
            widget.setProperty(
                "process_state",
                state,
            )

            widget.style().unpolish(widget)
            widget.style().polish(widget)
            widget.update()

    # =====================
    # OUTPUT FOLDER
    # =====================

    def set_output_folder(self, folder):
        if not folder:
            self.output_folder = None
            self.open_button.setEnabled(False)
            self.open_button.setToolTip("")
            return

        self.output_folder = Path(folder).expanduser()

        self.open_button.setEnabled(True)

        self.open_button.setToolTip(str(self.output_folder))

    # =====================
    # UPDATE PROGRESS
    # =====================

    def update_progress(
        self,
        current,
        total,
        filename,
        status,
    ):
        if total <= 0:
            return

        percentage = int((current / total) * 100)

        percentage = max(
            0,
            min(100, percentage),
        )

        # Update progress bar

        self.progress_bar.setValue(percentage)

        self.percentage_label.setText(f"{percentage}%")

        # Update file information

        self.file_label.setText(f"File: {filename}")

        self.file_label.setToolTip(str(filename))

        self.counter_label.setText(f"{current} / {total}")

        # Determine status appearance

        status_text = str(status)
        normalized = status_text.lower()

        if "fail" in normalized or "error" in normalized:
            state = "failed"

        elif "cancel" in normalized:
            state = "cancelled"

        else:
            state = "processing"

        self.set_status(
            state,
            status_text,
        )

    # =====================
    # EXPORT COMPLETED
    # =====================

    def finished(self):
        self.progress_bar.setValue(100)

        self.percentage_label.setText("100%")

        self.file_label.setText("All files finished")

        self.file_label.setToolTip("All files finished")

        self.set_status(
            "completed",
            "Completed",
        )

    # =====================
    # EXPORT FAILED
    # =====================

    def failed(self, error):
        self.file_label.setText(str(error))

        self.file_label.setToolTip(str(error))

        self.set_status(
            "failed",
            "Failed",
        )

    # =====================
    # RESET PROGRESS
    # =====================

    def reset(self):
        self.progress_bar.setValue(0)

        self.percentage_label.setText("0%")

        self.file_label.setText("File: -")

        self.file_label.setToolTip("")

        self.counter_label.setText("0 / 0")

        cpu_cores = os.cpu_count() or 4
        self.engine_label.setText(f"Multi-Core ({cpu_cores} Cores)")

        self.set_status(
            "ready",
            "Ready",
        )

    # =====================
    # OPEN OUTPUT FOLDER
    # =====================

    def open_folder(self):
        if self.output_folder is None:
            return

        folder = self.output_folder

        if not folder.is_dir():
            QMessageBox.warning(
                self,
                "Output Folder Unavailable",
                f"The selected output folder does not exist yet:\n\n{folder}",
            )
            return

        self.open_folder_requested.emit()

        success = QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder.resolve())))

        if not success:
            QMessageBox.warning(
                self,
                "Open Folder Failed",
                "Unable to open the selected output folder.",
            )

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        apply_export_progress_style(self)
