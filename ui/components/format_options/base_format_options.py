from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget


class BaseFormatOptions(QWidget):
    settings_changed = Signal(dict)

    def __init__(self):

        super().__init__()

        self.widgets = []

        self.setup_ui()

    def setup_ui(self):

        self.layout = QVBoxLayout(self)

        self.layout.setSpacing(10)

        self.layout.setContentsMargins(0, 0, 0, 0)

    def add_widget(self, widget):

        self.widgets.append(widget)

        self.layout.addWidget(widget)

    def remove_widget(self, widget):

        if widget in self.widgets:
            self.widgets.remove(widget)

        self.layout.removeWidget(widget)

        widget.deleteLater()

    def clear_options(self):

        for widget in self.widgets:
            self.layout.removeWidget(widget)

            widget.deleteLater()

        self.widgets.clear()

    def set_widget_visible(self, widget, visible):

        if widget:
            widget.setVisible(visible)

    def emit_settings_changed(self):

        self.settings_changed.emit(self.get_settings())

    def get_settings(self):
        """
        Return format specific encoder settings.

        Must be overridden by child class.

        Example:

        {
            "quality":85,
            "progressive":True
        }

        """

        return {}

    def reset(self):
        """
        Reset all widgets.

        Child classes should override.
        """

    def set_defaults(self, settings=None):
        """
        Load saved encoder settings.

        Example:

        {
            "quality":85,
            "lossless":False
        }

        """
