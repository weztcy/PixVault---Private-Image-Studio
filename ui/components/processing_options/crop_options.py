"""Crop controls using shared dropdown and number fields."""

from ui.components.processing_options.base_processing_options import (
    BaseProcessingOptions,
)
from ui.components.processing_options.common.dropdown_field import DropdownField
from ui.components.processing_options.common.number_field import NumberField


class CropOptions(BaseProcessingOptions):
    MODE_KEYS = {
        "Aspect Ratio": "aspect_ratio",
        "Fixed Dimensions": "fixed",
        "Percentage": "percentage",
        "Custom Coordinates": "coordinates",
    }

    def setup_ui(self):
        super().setup_ui()
        self.mode_field = self.add_widget(
            DropdownField("Crop Mode", list(self.MODE_KEYS), "Aspect Ratio")
        )
        self.ratio_field = self.add_widget(
            DropdownField("Aspect Ratio", ["1:1", "4:3", "16:9", "3:2", "21:9"], "1:1")
        )
        self.width_field = self.add_widget(NumberField("Width", 1, 100000, 1000, " px"))
        self.height_field = self.add_widget(
            NumberField("Height", 1, 100000, 1000, " px")
        )
        self.percentage_field = self.add_widget(
            NumberField("Percentage (%)", 1, 100, 100, " %")
        )
        self.x_field = self.add_widget(NumberField("X", 0, 100000, 0, " px"))
        self.y_field = self.add_widget(NumberField("Y", 0, 100000, 0, " px"))
        self.mode = self.mode_field.combo
        self.ratio = self.ratio_field.combo
        self.width = self.width_field.spin
        self.height = self.height_field.spin
        self.percentage = self.percentage_field.spin
        self.x = self.x_field.spin
        self.y = self.y_field.spin
        for name in ("ratio", "width", "height", "percentage", "x", "y"):
            setattr(self, name + "_label", getattr(self, name + "_field").label)
        self.mode.currentTextChanged.connect(self._on_mode_changed)
        for field in (
            self.ratio_field,
            self.width_field,
            self.height_field,
            self.percentage_field,
            self.x_field,
            self.y_field,
        ):
            field.value_changed.connect(self.emit_settings)
        self.update_ui()

    def _on_mode_changed(self, *_args):
        self.update_ui()
        self.emit_settings()

    def update_ui(self):
        mode = self.mode.currentText()
        states = {
            "ratio": mode == "Aspect Ratio",
            "width": mode in ("Fixed Dimensions", "Custom Coordinates"),
            "height": mode in ("Fixed Dimensions", "Custom Coordinates"),
            "percentage": mode == "Percentage",
            "x": mode == "Custom Coordinates",
            "y": mode == "Custom Coordinates",
        }
        for name, visible in states.items():
            getattr(self, name + "_field").setVisible(visible)

    def get_settings(self):
        mode = self.MODE_KEYS[self.mode.currentText()]
        settings = {"type": "crop", "mode": mode}
        if mode == "aspect_ratio":
            settings["ratio"] = self.ratio.currentText()
        elif mode == "percentage":
            settings["value"] = self.percentage.value()
        else:
            settings.update(width=self.width.value(), height=self.height.value())
            if mode == "coordinates":
                settings.update(x=self.x.value(), y=self.y.value())
        return settings

    def reset(self):
        self.mode.setCurrentText("Aspect Ratio")
        self.ratio.setCurrentText("1:1")
        self.width.setValue(1000)
        self.height.setValue(1000)
        self.percentage.setValue(100)
        self.x.setValue(0)
        self.y.setValue(0)
        self.update_ui()

    def update_capability(self):
        self.show_warning(
            "SVG crop requires vector clipping support."
            if self.current_format == "SVG"
            else ""
        )

    def validate(self):
        if self.current_format == "SVG":
            return False, "The raster crop backend cannot crop SVG images."
        return True, ""

    def set_defaults(self, settings):
        s = settings or {}
        label = next(
            (label for label, key in self.MODE_KEYS.items() if key == s.get("mode")),
            "Aspect Ratio",
        )
        self.mode.setCurrentText(label)
        self.ratio.setCurrentText(str(s.get("ratio", "1:1")))
        for name, default in (
            ("width", 1000),
            ("height", 1000),
            ("percentage", 100),
            ("x", 0),
            ("y", 0),
        ):
            value = (
                s.get("value", default)
                if name == "percentage"
                else s.get(name, default)
            )
            getattr(self, name).setValue(int(value))
        self.update_ui()
