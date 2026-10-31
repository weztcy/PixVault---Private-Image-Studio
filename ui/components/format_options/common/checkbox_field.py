from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from ui.styles.format_fields_style import apply_checkbox_field_style


class CheckboxField(QWidget):
    value_changed = Signal(bool)

    def __init__(self, text, default=False):
        super().__init__()

        self.setObjectName("checkbox_field")

        self.setup_ui(text, default)
        self.apply_styles()

    # =====================
    # USER INTERFACE
    # =====================

    def setup_ui(self, text, default):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # =====================
        # CHECKBOX CONTAINER
        # =====================

        self.container = QFrame()
        self.container.setObjectName("checkbox_field_container")

        self.container.setMinimumHeight(44)

        container_layout = QHBoxLayout(self.container)

        container_layout.setContentsMargins(14, 8, 14, 8)

        container_layout.setSpacing(10)

        # =====================
        # CHECKBOX
        # =====================

        self.checkbox = QCheckBox(text)

        self.checkbox.setObjectName("premium_checkbox")

        self.checkbox.setCursor(Qt.CursorShape.PointingHandCursor)

        self.checkbox.setChecked(bool(default))

        self.checkbox.setMinimumHeight(26)

        self.checkbox.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        container_layout.addWidget(
            self.checkbox,
            1,
        )

        main_layout.addWidget(self.container)

        # =====================
        # SIGNAL CONNECTION
        # =====================

        self.checkbox.toggled.connect(self.changed)

    # =====================
    # VALUE CHANGED
    # =====================

    def changed(self, checked=None):
        self.value_changed.emit(self.checkbox.isChecked())

    # =====================
    # GET VALUE
    # =====================

    def value(self):
        return self.checkbox.isChecked()

    # =====================
    # SET VALUE
    # =====================

    def set_value(self, value):
        self.checkbox.setChecked(bool(value))

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        apply_checkbox_field_style(self)
