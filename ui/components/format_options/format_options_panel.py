from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget

from ui.components.format_options.avif_options import AVIFOptions
from ui.components.format_options.bmp_options import BMPOptions
from ui.components.format_options.gif_options import GIFOptions
from ui.components.format_options.heic_options import HEICOptions
from ui.components.format_options.ico_options import ICOOptions
from ui.components.format_options.jpeg_options import JPEGOptions
from ui.components.format_options.png_options import PNGOptions
from ui.components.format_options.svg_options import SVGOptions
from ui.components.format_options.tiff_options import TIFFOptions
from ui.components.format_options.webp_options import WEBPOptions


class FormatOptionsPanel(QWidget):
    settings_changed = Signal(dict)

    FORMAT_WIDGETS = {
        "JPEG": JPEGOptions,
        "JPG": JPEGOptions,
        "PNG": PNGOptions,
        "WEBP": WEBPOptions,
        "AVIF": AVIFOptions,
        "TIFF": TIFFOptions,
        "TIF": TIFFOptions,
        "GIF": GIFOptions,
        "BMP": BMPOptions,
        "HEIC": HEICOptions,
        "ICO": ICOOptions,
        "SVG": SVGOptions,
    }

    def __init__(self):

        super().__init__()

        self.current_format = None

        self.current_widget = None

        self.widget_cache = {}

        self.setup_ui()

    def setup_ui(self):

        self.layout = QVBoxLayout(self)

        self.layout.setSpacing(10)

    def set_format(self, format_name):

        format_name = format_name.upper()

        self.current_format = format_name

        self.clear_current_widget()

        widget = self.get_or_create_widget(format_name)

        if widget:
            self.current_widget = widget

            self.layout.addWidget(widget)

            widget.show()

            self.emit_settings()

    def get_or_create_widget(self, format_name):

        if format_name in self.widget_cache:
            return self.widget_cache[format_name]

        widget_class = self.FORMAT_WIDGETS.get(format_name)

        if not widget_class:
            return None

        widget = widget_class()

        if hasattr(widget, "settings_changed"):
            widget.settings_changed.connect(self.emit_settings)

        self.widget_cache[format_name] = widget

        return widget

    def clear_current_widget(self):

        if not self.current_widget:
            return

        self.layout.removeWidget(self.current_widget)

        self.current_widget.hide()

        self.current_widget = None

    def get_settings(self):

        if not self.current_widget:
            return {}

        return self.current_widget.get_settings()

    def reset(self):

        if self.current_widget:
            self.current_widget.reset()

            self.emit_settings()

    def emit_settings(self):

        self.settings_changed.emit(self.get_settings())
