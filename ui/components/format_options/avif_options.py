from ui.components.format_options.base_format_options import BaseFormatOptions
from ui.components.format_options.common.checkbox_field import CheckboxField
from ui.components.format_options.common.dropdown_field import DropdownField
from ui.components.format_options.common.radio_mode_selector import RadioModeSelector
from ui.components.format_options.common.slider_field import SliderField


class AVIFOptions(BaseFormatOptions):
    def __init__(self):

        super().__init__()

        self.setup_connections()

    def setup_ui(self):

        super().setup_ui()

        # =====================
        # MODE
        # =====================

        self.mode = RadioModeSelector(
            "Compression Mode", ["Lossless", "Lossy"], "Lossy"
        )

        self.add_widget(self.mode)

        # =====================
        # QUALITY
        # LOSSY ONLY
        # =====================

        self.quality = SliderField("Quality", 1, 100, 80)

        self.add_widget(self.quality)

        # =====================
        # SPEED
        # GLOBAL
        # =====================

        self.speed = SliderField("Encoder Speed", 0, 10, 6)

        self.add_widget(self.speed)

        # =====================
        # SUBSAMPLING
        # GLOBAL
        # =====================

        self.subsampling = DropdownField(
            "Chroma Subsampling", ["4:4:4", "4:2:2", "4:2:0", "monochrome"], "4:2:0"
        )

        self.add_widget(self.subsampling)

        # =====================
        # ALPHA QUALITY
        # GLOBAL
        # =====================

        self.alpha_quality = SliderField("Alpha Quality", 0, 100, 100)

        self.add_widget(self.alpha_quality)

        # =====================
        # PROGRESSIVE
        # LOSSY ONLY
        # =====================

        self.progressive = CheckboxField("Progressive Encoding", False)

        self.add_widget(self.progressive)

    def setup_connections(self):

        self.mode.mode_changed.connect(self.update_mode)

        self.update_mode(self.mode.value())

    def update_mode(self, mode):

        is_lossless = mode == "Lossless"

        self.quality.setVisible(not is_lossless)

        self.progressive.setVisible(not is_lossless)

        self.emit_settings_changed()

    def get_settings(self):

        mode = self.mode.value()

        settings = {
            "mode": mode,
            "speed": self.speed.value(),
            "subsampling": self.subsampling.value(),
            "alpha_quality": self.alpha_quality.value(),
        }

        if mode == "Lossy":
            settings.update(
                {
                    "quality": self.quality.value(),
                    "progressive": self.progressive.value(),
                }
            )

        return settings

    def reset(self):

        self.mode.set_value("Lossy")

        self.quality.set_value(80)

        self.speed.set_value(6)

        self.subsampling.set_value("4:2:0")

        self.alpha_quality.set_value(100)

        self.progressive.set_value(False)
