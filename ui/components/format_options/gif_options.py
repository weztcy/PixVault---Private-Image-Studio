from PySide6.QtWidgets import QLabel, QLineEdit

from ui.components.format_options.base_format_options import BaseFormatOptions
from ui.components.format_options.common.checkbox_field import CheckboxField
from ui.components.format_options.common.dropdown_field import DropdownField
from ui.components.format_options.common.slider_field import SliderField


class GIFOptions(BaseFormatOptions):
    def __init__(self):

        super().__init__()

        self.setup_connections()

    def setup_ui(self):

        super().setup_ui()

        # =====================
        # COLORS
        # =====================

        self.colors = SliderField("Color Count", 2, 256, 256)

        self.add_widget(self.colors)

        # =====================
        # DITHER
        # =====================

        self.dither = DropdownField(
            "Dithering",
            ["none", "floyd_steinberg", "ordered", "atkinson"],
            "floyd_steinberg",
        )

        self.add_widget(self.dither)

        # =====================
        # OPTIMIZE
        # =====================

        self.optimize = CheckboxField("Optimize GIF", True)

        self.add_widget(self.optimize)

        # =====================
        # LOOP
        # =====================

        self.loop = CheckboxField("Enable Animation Loop", True)

        self.add_widget(self.loop)

        # =====================
        # LOOP COUNT
        # =====================

        self.loop_label = QLabel("Loop Count (0 = infinite)")

        self.add_widget(self.loop_label)

        self.loop_count = QLineEdit("0")

        self.add_widget(self.loop_count)

        # =====================
        # TRANSPARENCY
        # =====================

        self.transparency = CheckboxField("Enable Transparency", True)

        self.add_widget(self.transparency)

        # =====================
        # FRAME DURATION
        # =====================

        self.duration_label = QLabel("Frame Duration (ms)")

        self.add_widget(self.duration_label)

        self.duration = QLineEdit("100")

        self.add_widget(self.duration)

    def setup_connections(self):

        self.loop.value_changed.connect(self.update_loop)

        self.update_loop(True)

    def update_loop(self, enabled):

        self.loop_count.setEnabled(enabled)

        self.loop_label.setEnabled(enabled)

        self.emit_settings_changed()

    def get_settings(self):

        return {
            "colors": self.colors.value(),
            "dither": self.dither.value(),
            "optimize": self.optimize.value(),
            "loop": self.loop.value(),
            "loop_count": int(self.loop_count.text()),
            "transparency": self.transparency.value(),
            "duration": int(self.duration.text()),
        }

    def reset(self):

        self.colors.set_value(256)

        self.dither.set_value("floyd_steinberg")

        self.optimize.set_value(True)

        self.loop.set_value(True)

        self.loop_count.setText("0")

        self.transparency.set_value(True)

        self.duration.setText("100")
