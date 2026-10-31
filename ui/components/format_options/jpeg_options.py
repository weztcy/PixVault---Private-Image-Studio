from ui.components.format_options.base_format_options import BaseFormatOptions
from ui.components.format_options.common.checkbox_field import CheckboxField
from ui.components.format_options.common.dropdown_field import DropdownField
from ui.components.format_options.common.slider_field import SliderField


class JPEGOptions(BaseFormatOptions):
    def __init__(self):

        super().__init__()

    def setup_ui(self):

        super().setup_ui()

        # =====================
        # QUALITY
        # =====================

        self.quality = SliderField("Quality", 1, 100, 85)

        self.add_widget(self.quality)

        # =====================
        # PROGRESSIVE
        # =====================

        self.progressive = CheckboxField("Progressive JPEG", True)

        self.add_widget(self.progressive)

        # =====================
        # OPTIMIZE
        # =====================

        self.optimize = CheckboxField("Optimize Huffman Coding", True)

        self.add_widget(self.optimize)

        # =====================
        # SUBSAMPLING
        # =====================

        self.subsampling = DropdownField(
            "Chroma Subsampling", ["4:4:4", "4:2:2", "4:2:0"], "4:2:0"
        )

        self.add_widget(self.subsampling)

    def get_settings(self):

        return {
            "quality": self.quality.value(),
            "progressive": self.progressive.value(),
            "optimize": self.optimize.value(),
            "subsampling": self.subsampling.value(),
        }

    def reset(self):

        self.quality.set_value(85)

        self.progressive.set_value(True)

        self.optimize.set_value(True)

        self.subsampling.set_value("4:2:0")
