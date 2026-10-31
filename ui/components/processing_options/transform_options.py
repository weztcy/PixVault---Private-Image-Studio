"""Rotation and flip settings built exclusively from shared field controls."""

from ui.components.processing_options.base_processing_options import (
    BaseProcessingOptions,
)
from ui.components.processing_options.common.dropdown_field import DropdownField
from ui.components.processing_options.common.number_field import NumberField


class TransformOptions(BaseProcessingOptions):
    ROTATIONS = [
        "None",
        "90° Clockwise",
        "180°",
        "90° Counterclockwise",
        "Custom Angle",
    ]
    FLIPS = ["None", "Horizontal", "Vertical", "Both"]
    ROTATION_VALUES = {
        "None": "none",
        "90° Clockwise": 90,
        "180°": 180,
        "90° Counterclockwise": -90,
    }
    FLIP_VALUES = {
        "None": "none",
        "Horizontal": "horizontal",
        "Vertical": "vertical",
        "Both": "both",
    }

    def setup_ui(self):
        super().setup_ui()
        self.rotation_field = self.add_widget(
            DropdownField("Rotation", self.ROTATIONS, "None")
        )
        self.angle_field = self.add_widget(
            NumberField("Custom Angle", -360, 360, 0, "°")
        )
        self.flip_field = self.add_widget(DropdownField("Flip", self.FLIPS, "None"))
        self.rotation = self.rotation_field.combo
        self.angle = self.angle_field.spin
        self.angle_label = self.angle_field.label
        self.flip = self.flip_field.combo
        self.rotation.currentTextChanged.connect(self._rotation_changed)
        self.angle_field.value_changed.connect(self.emit_settings)
        self.flip_field.value_changed.connect(self.emit_settings)
        self.update_ui()

    def _rotation_changed(self, *_args):
        self.update_ui()
        self.emit_settings()

    def update_ui(self):
        self.angle_field.setVisible(self.rotation.currentText() == "Custom Angle")

    def get_settings(self):
        rotation = self.rotation.currentText()
        return {
            "type": "transform",
            "rotation": self.angle.value()
            if rotation == "Custom Angle"
            else self.ROTATION_VALUES[rotation],
            "flip": self.FLIP_VALUES[self.flip.currentText()],
        }

    def reset(self):
        self.rotation.setCurrentText("None")
        self.angle.setValue(0)
        self.flip.setCurrentText("None")
        self.update_ui()

    def update_capability(self):
        self.show_warning(
            "SVG uses vector transforms rather than pixel transforms."
            if self.current_format == "SVG"
            else ""
        )

    def validate(self):
        if self.current_format == "SVG":
            return (
                False,
                "The raster transform backend cannot directly process SVG files.",
            )
        return True, ""

    def set_defaults(self, settings):
        s = settings or {}
        rotation = s.get("rotation", "none")
        label = next(
            (name for name, value in self.ROTATION_VALUES.items() if value == rotation),
            None,
        )
        if label is None:
            label = "Custom Angle"
            self.angle.setValue(int(float(rotation)))
        self.rotation.setCurrentText(label)
        flip = next(
            (
                name
                for name, value in self.FLIP_VALUES.items()
                if value == s.get("flip", "none")
            ),
            "None",
        )
        self.flip.setCurrentText(flip)
        self.update_ui()
