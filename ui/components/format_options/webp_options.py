from ui.components.format_options.base_format_options import BaseFormatOptions
from ui.components.format_options.common.checkbox_field import CheckboxField
from ui.components.format_options.common.dropdown_field import DropdownField
from ui.components.format_options.common.radio_mode_selector import RadioModeSelector
from ui.components.format_options.common.slider_field import SliderField


class WEBPOptions(BaseFormatOptions):
    def __init__(self):

        super().__init__()

        self.setup_connections()

    def setup_ui(self):

        super().setup_ui()

        # =====================
        # COMPRESSION MODE
        # =====================

        self.mode = RadioModeSelector(
            "Compression Mode", ["Lossless", "Lossy"], "Lossy"
        )

        self.add_widget(self.mode)

        # =====================
        # QUALITY
        # LOSSY ONLY
        # =====================

        self.quality = SliderField("Quality", 1, 100, 85)

        self.add_widget(self.quality)

        # =====================
        # METHOD
        # GLOBAL
        # =====================

        self.method = DropdownField(
            "Compression Method", ["0", "1", "2", "3", "4", "5", "6"], "4"
        )

        self.add_widget(self.method)

        # =====================
        # ALPHA QUALITY
        # GLOBAL
        # =====================

        self.alpha_quality = SliderField("Alpha Quality", 0, 100, 100)

        self.add_widget(self.alpha_quality)

        # =====================
        # NEAR LOSSLESS
        # LOSSY ONLY
        # =====================

        self.near_lossless = CheckboxField("Near Lossless", False)

        self.add_widget(self.near_lossless)

        # =====================
        # EXACT
        # LOSSLESS ONLY
        # =====================

        self.exact = CheckboxField("Preserve Exact RGB", False)

        self.add_widget(self.exact)

    def setup_connections(self):

        self.mode.mode_changed.connect(self.update_mode)

        self.update_mode(self.mode.value())

    def update_mode(self, mode):

        is_lossless = mode == "Lossless"

        self.quality.setVisible(not is_lossless)

        self.near_lossless.setVisible(not is_lossless)

        self.exact.setVisible(is_lossless)

        self.emit_settings_changed()

    def get_settings(self):

        mode = self.mode.value()

        settings = {
            "mode": mode,
            "method": int(self.method.value()),
            "alpha_quality": self.alpha_quality.value(),
        }

        if mode == "Lossless":
            settings.update({"exact": self.exact.value()})

        else:
            settings.update(
                {
                    "quality": self.quality.value(),
                    "near_lossless": self.near_lossless.value(),
                }
            )

        return settings

    def reset(self):

        self.mode.set_value("Lossy")

        self.quality.set_value(85)

        self.method.set_value("4")

        self.alpha_quality.set_value(100)

        self.near_lossless.set_value(False)

        self.exact.set_value(False)
