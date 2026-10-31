from ui.components.format_options.base_format_options import BaseFormatOptions
from ui.components.format_options.common.checkbox_field import CheckboxField
from ui.components.format_options.common.dropdown_field import DropdownField


class ICOOptions(BaseFormatOptions):
    def __init__(self):

        super().__init__()

        self.setup_connections()

    def setup_ui(self):

        super().setup_ui()

        # =====================
        # ICON SIZE
        # =====================

        self.size = DropdownField(
            "Icon Size", ["16", "32", "48", "64", "128", "256"], "256"
        )

        self.add_widget(self.size)

        # =====================
        # BIT DEPTH
        # =====================

        self.bit_depth = DropdownField("Bit Depth", ["1", "4", "8", "24", "32"], "32")

        self.add_widget(self.bit_depth)

        # =====================
        # ALPHA
        # =====================

        self.alpha = CheckboxField("Preserve Alpha Channel", True)

        self.add_widget(self.alpha)

        # =====================
        # MULTI SIZE
        # =====================

        self.multiple_sizes = CheckboxField("Generate Multiple Icon Sizes", True)

        self.add_widget(self.multiple_sizes)

    def setup_connections(self):

        self.bit_depth.value_changed.connect(self.update_alpha)

        self.update_alpha("32")

    def update_alpha(self, depth):

        enabled = int(depth) == 32

        self.alpha.setEnabled(enabled)

        if not enabled:
            self.alpha.set_value(False)

        self.emit_settings_changed()

    def get_settings(self):

        return {
            "size": int(self.size.value()),
            "bit_depth": int(self.bit_depth.value()),
            "alpha": self.alpha.value(),
            "multiple_sizes": self.multiple_sizes.value(),
        }

    def reset(self):

        self.size.set_value("256")

        self.bit_depth.set_value("32")

        self.alpha.set_value(True)

        self.multiple_sizes.set_value(True)
