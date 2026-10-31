from ui.components.format_options.base_format_options import BaseFormatOptions
from ui.components.format_options.common.checkbox_field import CheckboxField
from ui.components.format_options.common.dropdown_field import DropdownField


class BMPOptions(BaseFormatOptions):
    def __init__(self):

        super().__init__()

        self.setup_connections()

    def setup_ui(self):

        super().setup_ui()

        # =====================
        # BIT DEPTH
        # =====================

        self.bit_depth = DropdownField(
            "Bit Depth", ["1", "4", "8", "16", "24", "32"], "24"
        )

        self.add_widget(self.bit_depth)

        # =====================
        # ALPHA
        # =====================

        self.alpha = CheckboxField("Enable Alpha Channel", False)

        self.add_widget(self.alpha)

        # =====================
        # COMPRESSION
        # =====================

        self.compression = DropdownField("Compression", ["none", "rle"], "none")

        self.add_widget(self.compression)

        # =====================
        # ORIENTATION
        # =====================

        self.top_down = CheckboxField("Top Down Orientation", False)

        self.add_widget(self.top_down)

    def setup_connections(self):

        self.bit_depth.value_changed.connect(self.update_bit_depth)

        self.update_bit_depth("24")

    def update_bit_depth(self, depth):

        depth = int(depth)

        # Alpha hanya valid
        # pada 16 dan 32 bit

        alpha_enabled = depth in [16, 32]

        self.alpha.setEnabled(alpha_enabled)

        if not alpha_enabled:
            self.alpha.set_value(False)

        # RLE hanya valid
        # untuk 8 bit BMP

        if depth == 8:
            self.compression.setEnabled(True)

        else:
            self.compression.set_value("none")

            self.compression.setEnabled(False)

        self.emit_settings_changed()

    def get_settings(self):

        return {
            "bit_depth": int(self.bit_depth.value()),
            "alpha": self.alpha.value(),
            "compression": self.compression.value(),
            "top_down": self.top_down.value(),
        }

    def reset(self):

        self.bit_depth.set_value("24")

        self.alpha.set_value(False)

        self.compression.set_value("none")

        self.top_down.set_value(False)
