"""Bit-depth settings (backend contract: {'type': 'bitdepth', 'value': int})."""

from ui.components.processing_options.base_processing_options import (
    BaseProcessingOptions,
)
from ui.components.processing_options.common.dropdown_field import DropdownField


class BitDepthOptions(BaseProcessingOptions):
    BIT_DEPTHS = ["8-bit", "16-bit", "32-bit"]
    # Per-channel precision. PNG supports 8/16, TIFF supports 8/16/32.
    # All other formats expose only the standard 8-bit option in this tool.
    SUPPORTED_DEPTHS = {
        "PNG": {"8-bit", "16-bit"},
        "TIFF": {"8-bit", "16-bit", "32-bit"},
    }

    def setup_ui(self):
        super().setup_ui()
        self.bit_depth_field = self.add_widget(
            DropdownField("Bit Depth", self.BIT_DEPTHS, "8-bit")
        )
        self.bit_depth = self.bit_depth_field.combo
        self.bit_depth.currentTextChanged.connect(self.emit_settings)

    def get_settings(self):
        return {
            "type": "bitdepth",
            "value": int(self.bit_depth.currentText().split("-")[0]),
        }

    def reset(self):
        self.bit_depth.setCurrentText("8-bit")
        self.update_capability()

    def update_capability(self):
        fmt = str(getattr(self, "current_format", "")).upper()
        supported = self.SUPPORTED_DEPTHS.get(fmt, {"8-bit"})
        model = self.bit_depth.model()
        for i in range(self.bit_depth.count()):
            item = model.item(i) if hasattr(model, "item") else None
            if item is not None:
                item.setEnabled(self.bit_depth.itemText(i) in supported)
        if self.bit_depth.currentText() not in supported:
            old = self.bit_depth.currentText()
            self.bit_depth.setCurrentText("8-bit")
            self.show_warning(
                f"{fmt or 'This format'} does not support {old} per channel."
            )
        else:
            self.show_warning("")

    def validate(self):
        fmt = str(getattr(self, "current_format", "")).upper()
        if self.bit_depth.currentText() not in self.SUPPORTED_DEPTHS.get(
            fmt, {"8-bit"}
        ):
            return False, "The selected bit depth is unavailable for this format."
        return True, ""

    def set_defaults(self, settings):
        value = str((settings or {}).get("value", 8)).replace("-bit", "") + "-bit"
        if value in self.BIT_DEPTHS:
            self.bit_depth.setCurrentText(value)
        self.update_capability()
