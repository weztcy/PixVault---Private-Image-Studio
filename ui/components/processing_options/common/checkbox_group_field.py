"""Reusable titled group of premium CheckboxField widgets."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ui.styles.processing_fields_style import apply_checkbox_group_field_style

from .checkbox_field import CheckboxField


class CheckboxGroupField(QWidget):
    changed = Signal()

    def __init__(self, title, items, default=True, parent=None):
        super().__init__(parent)
        self.setObjectName("checkbox_group_field")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(9)
        self.title_label = QLabel(str(title), self)
        self.title_label.setObjectName("checkbox_group_title")
        self.title_label.setWordWrap(True)
        self.layout.addWidget(self.title_label)
        self.fields = {}
        self.checkboxes = {}
        for text in items:
            field = CheckboxField(str(text), default)
            self.fields[text] = field
            self.checkboxes[text] = field.checkbox
            self.layout.addWidget(field)
            field.value_changed.connect(lambda *_args: self.changed.emit())
        apply_checkbox_group_field_style(self)
