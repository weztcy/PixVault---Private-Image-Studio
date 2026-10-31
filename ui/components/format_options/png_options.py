from ui.components.format_options.base_format_options import BaseFormatOptions
from ui.components.format_options.common.checkbox_field import CheckboxField
from ui.components.format_options.common.dropdown_field import DropdownField
from ui.components.format_options.common.slider_field import SliderField


class PNGOptions(BaseFormatOptions):
    def __init__(self):

        super().__init__()

    def setup_ui(self):

        super().setup_ui()

        # =====================
        # COMPRESSION LEVEL
        # =====================

        self.compression_level = SliderField("Compression Level", 0, 9, 6)

        self.add_widget(self.compression_level)

        # =====================
        # OPTIMIZE
        # =====================

        self.optimize = CheckboxField("Optimize PNG", True)

        self.add_widget(self.optimize)

        # =====================
        # INTERLACE
        # =====================

        self.interlace = CheckboxField("Interlaced PNG", False)

        self.add_widget(self.interlace)

        # =====================
        # FILTER
        # =====================

        self.filter_mode = DropdownField(
            "Filter Strategy",
            ["none", "sub", "up", "average", "paeth", "adaptive"],
            "adaptive",
        )

        self.add_widget(self.filter_mode)

    def get_settings(self):

        return {
            "compression_level": self.compression_level.value(),
            "optimize": self.optimize.value(),
            "interlace": self.interlace.value(),
            "filter": self.filter_mode.value(),
        }

    def reset(self):

        self.compression_level.set_value(6)

        self.optimize.set_value(True)

        self.interlace.set_value(False)

        self.filter_mode.set_value("adaptive")
