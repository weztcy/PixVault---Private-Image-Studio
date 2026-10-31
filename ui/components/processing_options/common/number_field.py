"""Reusable, styled integer input consistent with DropdownField/SliderField."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QSpinBox, QVBoxLayout, QWidget

from ui.styles.processing_fields_style import apply_number_field_style


class NumberField(QWidget):
    value_changed = Signal(int)

    def __init__(
        self, title, minimum=0, maximum=100000, default=0, suffix="", parent=None
    ):
        super().__init__(parent)
        self.setObjectName("number_field")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(9)
        self.label = QLabel(str(title))
        self.label.setObjectName("number_field_label")
        self.label.setWordWrap(True)
        self.spin = QSpinBox(self)
        self.spin.setObjectName("premium_number_input")
        self.spin.setRange(int(minimum), int(maximum))
        self.spin.setSuffix(str(suffix))
        self.spin.setValue(int(default))
        self.spin.setMinimumHeight(44)
        self.spin.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.spin.setAccessibleName(str(title))
        self.label.setBuddy(self.spin)
        layout.addWidget(self.label)
        layout.addWidget(self.spin)
        self.spin.valueChanged.connect(self.value_changed.emit)
        self.apply_styles()

    def value(self):
        return self.spin.value()

    def set_value(self, value):
        self.spin.setValue(int(value))

    def set_range(self, minimum, maximum):
        self.spin.setRange(int(minimum), int(maximum))

    def apply_styles(self):
        apply_number_field_style(self)
