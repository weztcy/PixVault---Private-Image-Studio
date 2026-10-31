"""Base contract used by every PixVault processing options widget.

UI composition is delegated to reusable controls in common/. Subclasses own
feature behavior and preserve their historic public Qt control attributes.
"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget

from ui.components.processing_options.common.warning_label import WarningLabel


class BaseProcessingOptions(QWidget):
    settings_changed = Signal(dict)
    validation_changed = Signal(bool, str)

    def __init__(self):
        super().__init__()
        self.current_format = None
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(12)
        self.warning_label = WarningLabel(self)
        self.layout.addWidget(self.warning_label)

    def add_widget(self, widget):
        self.layout.addWidget(widget)
        return widget

    def set_format(self, format_name):
        self.current_format = str(format_name or "").upper()
        self.update_capability()
        self.emit_settings()

    def update_capability(self):
        pass

    def show_warning(self, message):
        self.warning_label.show_warning(message)

    def emit_settings(self, *_args):
        self.settings_changed.emit(self.get_settings())
        self.validation_changed.emit(*self.validate())

    def get_settings(self):
        return {}

    def reset(self):
        pass

    def validate(self):
        return True, ""

    def set_defaults(self, settings):
        """Load saved values when a subclass supports them."""
