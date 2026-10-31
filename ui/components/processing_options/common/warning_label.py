"""A single reusable visual warning used throughout processing options."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from ui.styles.processing_fields_style import apply_warning_label_style


class WarningLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("processing_warning")
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.hide()
        apply_warning_label_style(self)

    def show_warning(self, message):
        if not message:
            return self.clear_warning()
        self.setText("⚠ " + str(message))
        self.show()

    def clear_warning(self):
        self.clear()
        self.hide()

    def has_warning(self):
        return bool(self.text())
