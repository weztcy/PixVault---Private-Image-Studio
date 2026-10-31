from PySide6.QtWidgets import QLabel, QLineEdit

from ui.components.format_options.base_format_options import BaseFormatOptions
from ui.components.format_options.common.checkbox_field import CheckboxField
from ui.components.format_options.common.dropdown_field import DropdownField


class TIFFOptions(BaseFormatOptions):
    def __init__(self):

        super().__init__()

        self.setup_connections()

    def setup_ui(self):

        super().setup_ui()

        # =====================
        # COMPRESSION
        # =====================

        self.compression = DropdownField(
            "Compression", ["none", "lzw", "deflate", "packbits", "jpeg", "zstd"], "lzw"
        )

        self.add_widget(self.compression)

        # =====================
        # PREDICTOR
        # =====================

        self.predictor = DropdownField(
            "Predictor", ["none", "horizontal", "floating_point"], "horizontal"
        )

        self.add_widget(self.predictor)

        # =====================
        # BIG TIFF
        # =====================

        self.bigtiff = CheckboxField("Enable BigTIFF", False)

        self.add_widget(self.bigtiff)

        # =====================
        # TILED
        # =====================

        self.tiled = CheckboxField("Enable Tiled Image", False)

        self.add_widget(self.tiled)

        # =====================
        # TILE WIDTH
        # =====================

        self.tile_width_label = QLabel("Tile Width")

        self.add_widget(self.tile_width_label)

        self.tile_width = QLineEdit("256")

        self.add_widget(self.tile_width)

        # =====================
        # TILE HEIGHT
        # =====================

        self.tile_height_label = QLabel("Tile Height")

        self.add_widget(self.tile_height_label)

        self.tile_height = QLineEdit("256")

        self.add_widget(self.tile_height)

        # =====================
        # DPI
        # =====================

        self.dpi_label = QLabel("Resolution DPI")

        self.add_widget(self.dpi_label)

        self.dpi = QLineEdit("300")

        self.add_widget(self.dpi)

    def setup_connections(self):

        self.compression.value_changed.connect(self.update_predictor)

        self.tiled.value_changed.connect(self.update_tiles)

        self.update_predictor(self.compression.value())

        self.update_tiles(False)

    def update_predictor(self, compression):

        enabled = compression in ["lzw", "deflate", "zstd"]

        self.predictor.setEnabled(enabled)

        self.emit_settings_changed()

    def update_tiles(self, enabled):

        self.tile_width.setEnabled(enabled)

        self.tile_height.setEnabled(enabled)

        self.tile_width_label.setEnabled(enabled)

        self.tile_height_label.setEnabled(enabled)

        self.emit_settings_changed()

    def get_settings(self):

        return {
            "compression": self.compression.value(),
            "predictor": self.predictor.value(),
            "bigtiff": self.bigtiff.value(),
            "tiled": self.tiled.value(),
            "tile_width": int(self.tile_width.text()),
            "tile_height": int(self.tile_height.text()),
            "dpi": int(self.dpi.text()),
        }

    def reset(self):

        self.compression.set_value("lzw")

        self.predictor.set_value("horizontal")

        self.bigtiff.set_value(False)

        self.tiled.set_value(False)

        self.tile_width.setText("256")

        self.tile_height.setText("256")

        self.dpi.setText("300")
