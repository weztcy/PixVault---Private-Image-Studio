"""Resize settings with independent width, height, side, and percent inputs."""

from ui.components.processing_options.base_processing_options import (
    BaseProcessingOptions,
)
from ui.components.processing_options.common.checkbox_field import CheckboxField
from ui.components.processing_options.common.dropdown_field import DropdownField
from ui.components.processing_options.common.number_field import NumberField


class ResizeOptions(BaseProcessingOptions):
    METHODS = {
        "Exact Dimensions": "exact",
        "Width": "width",
        "Height": "height",
        "Longest Side": "longest_side",
        "Shortest Side": "shortest_side",
        "Percentage": "percentage",
    }

    def setup_ui(self):
        super().setup_ui()
        self.method_field = self.add_widget(
            DropdownField("Resize Method", list(self.METHODS), "Width")
        )
        self.width_field = self.add_widget(NumberField("Width", 1, 100000, 1000, " px"))
        self.height_field = self.add_widget(
            NumberField("Height", 1, 100000, 1000, " px")
        )
        self.side_field = self.add_widget(
            NumberField("Target Side", 1, 100000, 1000, " px")
        )
        self.percentage_field = self.add_widget(
            NumberField("Percentage (%)", 1, 1000, 100, " %")
        )
        self.keep_ratio_field = self.add_widget(
            CheckboxField("Keep Aspect Ratio", True)
        )
        self.resampling_field = self.add_widget(
            DropdownField(
                "Resampling", ["Nearest", "Bilinear", "Bicubic", "Lanczos"], "Lanczos"
            )
        )
        self.method = self.method_field.combo
        self.width_input = self.width_field.spin
        self.height_input = self.height_field.spin
        self.side_input = self.side_field.spin
        self.percentage_input = self.percentage_field.spin
        self.width_label = self.width_field.label
        self.height_label = self.height_field.label
        self.percentage_label = self.percentage_field.label
        self.keep_ratio = self.keep_ratio_field.checkbox
        self.resampling = self.resampling_field.combo
        self.method.currentTextChanged.connect(self._method_changed)
        for field in (
            self.width_field,
            self.height_field,
            self.side_field,
            self.percentage_field,
            self.keep_ratio_field,
            self.resampling_field,
        ):
            field.value_changed.connect(self.emit_settings)
        self.update_ui()

    def _method_changed(self, *_args):
        self.update_ui()
        self.emit_settings()

    def update_ui(self):
        method = self.method.currentText()
        self.width_field.setVisible(method in ("Exact Dimensions", "Width"))
        self.height_field.setVisible(method in ("Exact Dimensions", "Height"))
        self.side_field.setVisible(method in ("Longest Side", "Shortest Side"))
        self.percentage_field.setVisible(method == "Percentage")
        self.keep_ratio_field.setEnabled(
            method
            not in ("Exact Dimensions", "Percentage", "Longest Side", "Shortest Side")
        )

    def get_settings(self):
        method = self.METHODS[self.method.currentText()]
        settings = {
            "type": "resize",
            "method": method,
            "keep_ratio": self.keep_ratio.isChecked()
            if method in ("width", "height")
            else (method != "exact"),
            "resampling": self.resampling.currentText().lower(),
        }
        if method == "exact":
            settings.update(
                width=self.width_input.value(), height=self.height_input.value()
            )
        elif method == "width":
            settings["value"] = self.width_input.value()
        elif method == "height":
            settings["value"] = self.height_input.value()
        elif method in ("longest_side", "shortest_side"):
            settings["value"] = self.side_input.value()
        elif method == "percentage":
            settings["value"] = self.percentage_input.value()
        return settings

    def reset(self):
        self.method.setCurrentText("Width")
        self.width_input.setValue(1000)
        self.height_input.setValue(1000)
        self.side_input.setValue(1000)
        self.percentage_input.setValue(100)
        self.keep_ratio.setChecked(True)
        self.resampling.setCurrentText("Lanczos")
        self.update_ui()

    def update_capability(self):
        self.show_warning(
            "SVG resizing requires rasterization or a vector renderer."
            if self.current_format == "SVG"
            else ""
        )

    def validate(self):
        if self.current_format == "SVG":
            return False, "The Pillow-based resize backend cannot load SVG directly."
        return True, ""

    def set_defaults(self, settings):
        s = settings or {}
        method = str(s.get("method", "width"))
        label = next(
            (name for name, key in self.METHODS.items() if key == method), "Width"
        )
        self.method.setCurrentText(label)
        self.width_input.setValue(
            int(s.get("width", s.get("value", 1000) if method == "width" else 1000))
        )
        self.height_input.setValue(
            int(s.get("height", s.get("value", 1000) if method == "height" else 1000))
        )
        self.side_input.setValue(int(s.get("value", 1000)))
        self.percentage_input.setValue(
            int(s.get("value", 100) if method == "percentage" else 100)
        )
        self.keep_ratio.setChecked(bool(s.get("keep_ratio", True)))
        self.resampling.setCurrentText(str(s.get("resampling", "lanczos")).title())
        self.update_ui()
