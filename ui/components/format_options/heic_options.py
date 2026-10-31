from ui.components.format_options.base_format_options import BaseFormatOptions
from ui.components.format_options.common.checkbox_field import CheckboxField
from ui.components.format_options.common.dropdown_field import DropdownField
from ui.components.format_options.common.radio_mode_selector import RadioModeSelector
from ui.components.format_options.common.slider_field import SliderField


class HEICOptions(BaseFormatOptions):
    def __init__(self):

        super().__init__()

        self.setup_connections()

    def setup_ui(self):

        super().setup_ui()

        # =====================
        # MODE
        # =====================

        self.mode = RadioModeSelector(
            "Compression Mode", ["Lossy", "Lossless"], "Lossy"
        )

        self.add_widget(self.mode)

        # =====================
        # QUALITY
        # LOSSY ONLY
        # =====================

        self.quality = SliderField("Quality", 1, 100, 85)

        self.add_widget(self.quality)

        # =====================
        # COMPRESSION
        # GLOBAL
        # =====================

        self.compression = DropdownField(
            "Compression", ["hevc", "hevc_lossless"], "hevc"
        )

        self.add_widget(self.compression)

        # =====================
        # CHROMA
        # GLOBAL
        # =====================

        self.subsampling = DropdownField(
            "Chroma Subsampling", ["4:4:4", "4:2:2", "4:2:0"], "4:2:0"
        )

        self.add_widget(self.subsampling)

        # =====================
        # METADATA
        # GLOBAL
        # =====================

        self.preserve_metadata = CheckboxField("Preserve Metadata", False)

        self.add_widget(self.preserve_metadata)

        # =====================
        # ALPHA
        # GLOBAL
        # =====================

        self.alpha = CheckboxField("Enable Alpha Channel", True)

        self.add_widget(self.alpha)

    def setup_connections(self):

        self.mode.mode_changed.connect(self.update_mode)

        self.update_mode(self.mode.value())

    def update_mode(self, mode):

        is_lossless = mode == "Lossless"

        self.quality.setVisible(not is_lossless)

        self.emit_settings_changed()

    def get_settings(self):

        mode = self.mode.value()

        settings = {
            "mode": mode,
            "compression": self.compression.value(),
            "subsampling": self.subsampling.value(),
            "preserve_metadata": self.preserve_metadata.value(),
            "alpha": self.alpha.value(),
        }

        if mode == "Lossy":
            settings["quality"] = self.quality.value()

        else:
            settings["compression"] = "hevc_lossless"

        return settings

    def reset(self):

        self.mode.set_value("Lossy")

        self.quality.set_value(85)

        self.compression.set_value("hevc")

        self.subsampling.set_value("4:2:0")

        self.preserve_metadata.set_value(False)

        self.alpha.set_value(True)
