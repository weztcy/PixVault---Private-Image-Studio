from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QBoxLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.styles.history_page_style import apply_history_page_style


OPERATION_DISPLAY_NAMES = {
    "convert": "Convert",
    "conversion": "Convert",
    "compression": "Compression",
    "compress": "Compression",
    "resize": "Resize",
    "crop": "Crop",
    "transform": "Transform",
    "dpi": "DPI",
    "metadata": "Metadata",
    "colorspace": "Color Space",
    "bitdepth": "Bit Depth",
}


class HistoryPage(QWidget):
    def __init__(self, history_service):
        super().__init__()

        self.history_service = history_service
        self.history_records = []
        self._selected_row_widget = None

        self.setObjectName("history_page")

        self.setup_ui()
        self.apply_styles()
        self.load_history()

    # =====================
    # MAIN UI
    # =====================

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("history_scroll")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.container = QWidget()
        self.container.setObjectName("history_container")

        self.content_layout = QVBoxLayout(self.container)
        self.content_layout.setContentsMargins(28, 26, 28, 26)
        self.content_layout.setSpacing(20)

        # Header

        self.content_layout.addWidget(self.create_header())

        # Statistics

        self.content_layout.addLayout(self.create_statistics())

        # History / Details

        self.panel_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.panel_layout.setSpacing(18)

        self.panel_layout.addWidget(self.create_history_panel(), 6)
        self.panel_layout.addWidget(self.create_details_panel(), 5)

        self.content_layout.addLayout(self.panel_layout, 1)

        self.scroll_area.setWidget(self.container)
        main_layout.addWidget(self.scroll_area)

    # =====================
    # HELPERS
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

    def create_card(self, object_name="history_card"):
        card = QFrame()
        card.setObjectName(object_name)

        card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        return card

    def get_filename(self, path):
        value = str(path or "-")

        return value.replace("\\", "/").split("/")[-1]

    def normalize_status(self, status):
        value = str(status or "unknown").lower()

        if value == "success":
            return "success"

        if value in ("error", "failed", "failure"):
            return "failed"

        if value in ("cancelled", "canceled"):
            return "cancelled"

        return "unknown"

    def get_status_text(self, status):
        labels = {
            "success": "COMPLETED",
            "failed": "FAILED",
            "cancelled": "CANCELLED",
            "unknown": "UNKNOWN",
        }

        return labels.get(
            self.normalize_status(status),
            "UNKNOWN",
        )

    # =====================
    # HEADER
    # =====================

    def create_header(self):
        card = self.create_card("history_hero")

        layout = QHBoxLayout(card)
        layout.setContentsMargins(26, 24, 26, 24)
        layout.setSpacing(20)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(8)

        eyebrow = self.create_label(
            "ACTIVITY CENTER",
            "history_eyebrow",
        )

        title = self.create_label(
            "Processing History",
            "history_hero_title",
        )

        description = self.create_label(
            "Review, search, and manage your locally stored image processing activity.",
            "history_description",
        )

        text_layout.addWidget(eyebrow)
        text_layout.addWidget(title)
        text_layout.addWidget(description)

        layout.addLayout(text_layout, 1)

        # Header actions

        actions = QVBoxLayout()
        actions.setSpacing(10)

        self.refresh_button = QPushButton("↻  Refresh History")
        self.refresh_button.setObjectName("history_refresh_button")

        self.refresh_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.refresh_button.clicked.connect(self.load_history)

        self.clear_button = QPushButton("Clear All History")
        self.clear_button.setObjectName("history_clear_button")

        self.clear_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.clear_button.clicked.connect(self.clear_history)

        self.refresh_button.setMinimumHeight(38)
        self.clear_button.setMinimumHeight(38)

        actions.addWidget(self.refresh_button)
        actions.addWidget(self.clear_button)

        layout.addLayout(actions)

        return card

    # =====================
    # STATISTICS
    # =====================

    def create_statistics(self):
        layout = QHBoxLayout()
        layout.setSpacing(14)

        total_card, self.total_value = self.create_stat_card(
            "TOTAL RECORDS",
            "0",
            "total",
        )

        success_card, self.success_value = self.create_stat_card(
            "SUCCESSFUL",
            "0",
            "success",
        )

        failed_card, self.failed_value = self.create_stat_card(
            "FAILED",
            "0",
            "failed",
        )

        layout.addWidget(total_card, 1)
        layout.addWidget(success_card, 1)
        layout.addWidget(failed_card, 1)

        return layout

    def create_stat_card(
        self,
        title,
        value,
        category,
    ):
        card = self.create_card("history_stat_card")
        card.setMinimumHeight(100)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)

        title_label = self.create_label(
            title,
            "history_stat_title",
        )

        value_label = self.create_label(
            value,
            "history_stat_value",
            False,
        )
        value_label.setProperty("category", category)

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()

        return card, value_label

    def update_statistics(self):
        records = self.history_records

        total = len(records)

        success = sum(
            self.normalize_status(record.get("status")) == "success"
            for record in records
        )

        failed = sum(
            self.normalize_status(record.get("status")) == "failed"
            for record in records
        )

        self.total_value.setText(str(total))
        self.success_value.setText(str(success))
        self.failed_value.setText(str(failed))

        self.clear_button.setEnabled(total > 0)

    # =====================
    # HISTORY PANEL
    # =====================

    def create_history_panel(self):
        card = self.create_card("history_card")
        card.setMinimumHeight(400)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 22, 20, 20)
        layout.setSpacing(14)

        title = self.create_label(
            "Recent Activity",
            "history_section_title",
        )

        subtitle = self.create_label(
            "Select a record to view its details.",
            "history_section_description",
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Search

        self.search_input = QLineEdit()
        self.search_input.setObjectName("history_search")

        self.search_input.setPlaceholderText("Search files, formats, operations...")

        self.search_input.setClearButtonEnabled(True)
        self.search_input.setMinimumHeight(40)

        self.search_input.textChanged.connect(self.render_history)

        layout.addWidget(self.search_input)

        # History List

        self.list_widget = QListWidget()
        self.list_widget.setObjectName("history_list")

        self.list_widget.setSpacing(6)
        self.list_widget.setWordWrap(True)

        self.list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

        self.list_widget.currentItemChanged.connect(self.on_history_selected)

        layout.addWidget(self.list_widget, 1)

        return card

    # =====================
    # HISTORY ROW
    # =====================

    def create_history_row(self, record):
        row = QFrame()
        row.setObjectName("history_record")
        row.setProperty("selected", False)

        layout = QVBoxLayout(row)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)

        source = record.get("source", "-")
        filename = self.get_filename(source)

        # Filename

        display_name = filename if len(filename) <= 35 else filename[:32] + "..."

        name_label = self.create_label(
            display_name,
            "history_record_name",
            False,
        )
        name_label.setToolTip(str(source))

        # Status

        status = self.normalize_status(record.get("status"))

        status_label = self.create_label(
            self.get_status_text(status),
            "history_status_badge",
            False,
        )

        status_label.setProperty("status", status)

        top_layout.addWidget(name_label, 1)
        top_layout.addWidget(status_label)

        # Secondary information

        format_name = str(record.get("format") or "-")

        timestamp = str(record.get("timestamp") or "-")

        metadata = self.create_label(
            f"{format_name.upper()}  •  {timestamp}",
            "history_record_metadata",
        )

        layout.addLayout(top_layout)
        layout.addWidget(metadata)

        return row

    # =====================
    # LOAD HISTORY
    # =====================

    def load_history(self):
        try:
            history = self.history_service.get_history()

            if history is None:
                history = []

            if not isinstance(history, list):
                raise ValueError("Invalid history data format.")

            self.history_records = [
                item for item in reversed(history) if isinstance(item, dict)
            ]

            self.update_statistics()
            self.render_history()

        except Exception as error:
            QMessageBox.critical(
                self,
                "History Error",
                str(error),
            )

    # =====================
    # SEARCH & RENDER
    # =====================

    def render_history(self, *_args):
        if not hasattr(self, "list_widget"):
            return

        query = self.search_input.text().strip().lower()

        self._selected_row_widget = None

        self.list_widget.blockSignals(True)
        self.list_widget.clear()

        filtered = []

        for record in self.history_records:
            operations = record.get("operations") or []
            op_names = self.get_operation_names(operations)
            search_text = " ".join(
                str(value)
                for value in (
                    record.get("source", ""),
                    record.get("output", ""),
                    record.get("format", ""),
                    record.get("status", ""),
                    record.get("timestamp", ""),
                    " ".join(op_names),
                )
            ).lower()

            if query in search_text:
                filtered.append(record)

        # Empty state

        if not filtered:
            self.list_widget.blockSignals(False)

            message = (
                "No matching history records."
                if query
                else "No processing history yet."
            )

            self.show_empty_state(message)
            self.reset_details()
            return

        # Render records

        for record in filtered:
            item = QListWidgetItem()

            item.setData(
                Qt.ItemDataRole.UserRole,
                record,
            )

            item.setSizeHint(QSize(100, 82))

            row_widget = self.create_history_row(record)

            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(
                item,
                row_widget,
            )

        self.list_widget.blockSignals(False)

        self.list_widget.setCurrentRow(0)

    # =====================
    # EMPTY STATE
    # =====================

    def show_empty_state(self, message):
        item = QListWidgetItem(
            f"\n\n     {message}\n\n     Your activity will appear here."
        )

        item.setFlags(Qt.ItemFlag.NoItemFlags)

        item.setSizeHint(QSize(100, 130))

        self.list_widget.addItem(item)

    # =====================
    # DETAILS PANEL
    # =====================

    def create_details_panel(self):
        card = self.create_card("history_card")
        card.setMinimumHeight(400)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 22, 20, 20)
        layout.setSpacing(12)

        title = self.create_label(
            "Processing Details",
            "history_section_title",
        )

        subtitle = self.create_label(
            "Detailed information for the selected processing record.",
            "history_section_description",
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Scrollable details

        details_scroll = QScrollArea()
        details_scroll.setObjectName("history_details_scroll")
        details_scroll.setWidgetResizable(True)

        details_scroll.setFrameShape(QFrame.Shape.NoFrame)

        details_widget = QWidget()
        details_widget.setObjectName("history_details_container")

        details_layout = QVBoxLayout(details_widget)
        details_layout.setContentsMargins(0, 12, 0, 0)
        details_layout.setSpacing(16)

        # Status

        self.detail_status = self.create_label(
            "NO RECORD SELECTED",
            "history_detail_status",
        )
        self.detail_status.setProperty("status", "unknown")

        details_layout.addWidget(self.detail_status)

        # Fields

        self.detail_timestamp = self.add_detail_field(
            details_layout,
            "DATE & TIME",
        )

        self.detail_source = self.add_detail_field(
            details_layout,
            "SOURCE FILE",
        )

        self.detail_output = self.add_detail_field(
            details_layout,
            "OUTPUT FILE",
        )

        self.detail_format = self.add_detail_field(
            details_layout,
            "OUTPUT FORMAT",
        )

        self.detail_operations = self.add_detail_field(
            details_layout,
            "OPERATIONS",
        )

        self.error_section = QWidget()

        error_layout = QVBoxLayout(self.error_section)

        error_layout.setContentsMargins(0, 0, 0, 0)

        self.detail_error = self.add_detail_field(
            error_layout,
            "ERROR DETAILS",
        )

        details_layout.addWidget(self.error_section)

        details_layout.addStretch()

        details_scroll.setWidget(details_widget)

        layout.addWidget(details_scroll, 1)

        self.reset_details()

        return card

    # =====================
    # DETAIL FIELD
    # =====================

    def add_detail_field(
        self,
        layout,
        title,
    ):
        container = QVBoxLayout()
        container.setSpacing(6)

        title_label = self.create_label(
            title,
            "history_field_title",
        )

        value_label = self.create_label(
            "-",
            "history_field_value",
        )

        value_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        container.addWidget(title_label)
        container.addWidget(value_label)

        layout.addLayout(container)

        return value_label

    # =====================
    # ITEM SELECTION
    # =====================

    def on_history_selected(
        self,
        current,
        previous,
    ):
        # Remove previous row highlight

        if previous is not None:
            old_widget = self.list_widget.itemWidget(previous)

            self.set_row_selected(
                old_widget,
                False,
            )

        if current is None:
            self.reset_details()
            return

        record = current.data(Qt.ItemDataRole.UserRole)

        if not isinstance(record, dict):
            self.reset_details()
            return

        row_widget = self.list_widget.itemWidget(current)

        self.set_row_selected(
            row_widget,
            True,
        )

        self.update_details(record)

    def set_row_selected(
        self,
        widget,
        selected,
    ):
        if widget is None:
            return

        widget.setProperty(
            "selected",
            selected,
        )

        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.update()

    # =====================
    # GET OPERATION NAMES
    # =====================

    def get_operation_names(self, operations):
        operation_names = []
        if isinstance(operations, list):
            for op in operations:
                if isinstance(op, dict):
                    op_type = op.get("type", "unknown")
                    display_name = OPERATION_DISPLAY_NAMES.get(
                        str(op_type).lower(),
                        str(op_type).replace("_", " ").title(),
                    )
                    operation_names.append(display_name)
                elif op:
                    display_name = OPERATION_DISPLAY_NAMES.get(
                        str(op).lower(),
                        str(op).replace("_", " ").title(),
                    )
                    operation_names.append(display_name)

        if not operation_names:
            return ["Convert"]

        return operation_names

    # =====================
    # UPDATE DETAILS
    # =====================

    def update_details(self, record):
        status = self.normalize_status(record.get("status"))

        self.detail_status.setText(self.get_status_text(status))

        self.detail_status.setProperty("status", status)

        self.detail_status.style().unpolish(self.detail_status)

        self.detail_status.style().polish(self.detail_status)

        self.detail_timestamp.setText(str(record.get("timestamp") or "-"))

        self.detail_source.setText(str(record.get("source") or "-"))

        self.detail_output.setText(str(record.get("output") or "-"))

        self.detail_format.setText(str(record.get("format") or "-").upper())

        # Operations

        operations = record.get("operations") or []
        operation_names = self.get_operation_names(operations)

        self.detail_operations.setText(", ".join(operation_names))

        # Error details

        error = record.get("error")

        if error:
            self.error_section.show()
            self.detail_error.setText(str(error))
        else:
            self.error_section.hide()

    # =====================
    # RESET DETAILS
    # =====================

    def reset_details(self):
        self.detail_status.setText("NO RECORD SELECTED")

        self.detail_status.setProperty(
            "status",
            "unknown",
        )

        self.detail_status.style().unpolish(self.detail_status)
        self.detail_status.style().polish(self.detail_status)

        for field in (
            self.detail_timestamp,
            self.detail_source,
            self.detail_output,
            self.detail_format,
            self.detail_operations,
            self.detail_error,
        ):
            field.setText("-")

        self.error_section.hide()

    # =====================
    # ORIGINAL FORMAT METHOD
    # =====================

    def format_history_item(
        self,
        status,
        source,
        output,
        format_name,
        operations,
        error=None,
    ):
        operation_names = self.get_operation_names(operations)
        operation_text = ", ".join(operation_names)

        text = (
            f"{self.get_status_text(status)}\n"
            f"Source: {source}\n"
            f"Output: {output}\n"
            f"Format: {format_name}\n"
            f"Operations: {operation_text}"
        )

        if error:
            text += f"\nError: {error}"

        return text

    # =====================
    # CLEAR HISTORY
    # =====================

    def clear_history(self):
        if not self.history_records:
            return

        confirm = QMessageBox.question(
            self,
            "Clear Processing History",
            "Are you sure you want to delete "
            "all processing history records?\n\n"
            "This action cannot be undone.\n"
            "Your processed image files "
            "will not be deleted.",
            (QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No),
            QMessageBox.StandardButton.No,
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            self.history_service.clear_history()
            self.load_history()

        except Exception as error:
            QMessageBox.critical(
                self,
                "Clear History Error",
                str(error),
            )

    # =====================
    # RESPONSIVE LAYOUT
    # =====================

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if not hasattr(self, "panel_layout"):
            return

        if self.width() < 740:
            self.panel_layout.setDirection(QBoxLayout.Direction.TopToBottom)
        else:
            self.panel_layout.setDirection(QBoxLayout.Direction.LeftToRight)

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        apply_history_page_style(self)
