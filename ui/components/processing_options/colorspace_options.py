"""Color-space UI expressed using reusable DropdownField controls."""

from ui.components.processing_options.base_processing_options import (
    BaseProcessingOptions,
)
from ui.components.processing_options.common.dropdown_field import DropdownField


class ColorSpaceOptions(BaseProcessingOptions):
    COLOR_SPACES = ["sRGB", "Adobe RGB", "Display P3", "CMYK", "Grayscale"]
    RENDERING_INTENTS = [
        "Perceptual",
        "Relative Colorimetric",
        "Saturation",
        "Absolute Colorimetric",
    ]
    TARGET_KEYS = {
        "sRGB": "sRGB",
        "Adobe RGB": "adobe_rgb",
        "Display P3": "display_p3",
        "CMYK": "cmyk",
        "Grayscale": "grayscale",
    }
    INTENT_KEYS = {
        "Perceptual": "perceptual",
        "Relative Colorimetric": "relative_colorimetric",
        "Saturation": "saturation",
        "Absolute Colorimetric": "absolute_colorimetric",
    }
    LIMITED = {
        "WEBP": {"Adobe RGB", "Display P3", "CMYK"},
        "GIF": {"Adobe RGB", "Display P3", "CMYK"},
        "BMP": {"Adobe RGB", "Display P3", "CMYK"},
        "ICO": {"Adobe RGB", "Display P3", "CMYK"},
        "PNG": {"CMYK"},
        "AVIF": {"CMYK"},
        "HEIC": {"CMYK"},
    }

    def setup_ui(self):
        super().setup_ui()
        self.color_space_field = self.add_widget(
            DropdownField("Color Space", self.COLOR_SPACES, "sRGB")
        )
        self.intent_field = self.add_widget(
            DropdownField("Rendering Intent", self.RENDERING_INTENTS, "Perceptual")
        )
        self.color_space = self.color_space_field.combo
        self.intent = self.intent_field.combo
        self.intent_label = self.intent_field.label
        self.color_space.currentTextChanged.connect(self._on_target_changed)
        self.intent.currentTextChanged.connect(self.emit_settings)
        self.update_ui()

    def _on_target_changed(self, *_args):
        self.update_capability()
        self.emit_settings()

    def update_ui(self):
        # Grayscale bypasses ICC transforms; no rendering intent needed.
        self.intent_field.setEnabled(self.color_space.currentText() != "Grayscale")

    def get_settings(self):
        target = self.color_space.currentText()
        # Backend processing/colorspace.py consumes `intent`, not `rendering_intent`.
        return {
            "type": "colorspace",
            "target": self.TARGET_KEYS[target],
            "intent": self.INTENT_KEYS[self.intent.currentText()],
        }

    def reset(self):
        self.color_space.setCurrentText("sRGB")
        self.intent.setCurrentText("Perceptual")
        self.update_capability()
        self.update_ui()

    def update_capability(self):
        """
        Update available color spaces based on output format.

        ICC backend supports:
        - sRGB
        - Adobe RGB
        - Display P3
        - CMYK
        - Grayscale
        """

        restricted = self.LIMITED.get(self.current_format, set())

        model = self.color_space.model()

        for i in range(self.color_space.count()):
            item = model.item(i)

            if item is not None:
                item.setEnabled(self.color_space.itemText(i) not in restricted)

        current = self.color_space.currentText()

        # Reset if current selection is incompatible
        if current in restricted:
            self.color_space.setCurrentText("sRGB")

        # Only show warning for format incompatibility
        if self.color_space.currentText() in restricted:
            self.show_warning(
                f"{self.current_format} cannot use {self.color_space.currentText()}."
            )

        elif restricted:
            self.show_warning(f"{self.current_format} has limited color space support.")

        else:
            self.show_warning("")

        self.update_ui()

    def validate(self):
        target = self.color_space.currentText()
        if target in self.LIMITED.get(self.current_format, set()):
            return False, f"{self.current_format} cannot use {target}."
        if target in ("Adobe RGB", "Display P3", "CMYK"):
            return True, ""
        return True, ""

    def set_defaults(self, settings):
        settings = settings or {}
        key = str(settings.get("target", "sRGB")).strip().lower().replace(" ", "_")
        target = next(
            (
                label
                for label, value in self.TARGET_KEYS.items()
                if value.lower() == key
            ),
            "sRGB",
        )
        self.color_space.setCurrentText(target)
        intent_key = (
            str(settings.get("intent", settings.get("rendering_intent", "perceptual")))
            .lower()
            .replace(" ", "_")
        )
        intent = next(
            (label for label, value in self.INTENT_KEYS.items() if value == intent_key),
            "Perceptual",
        )
        self.intent.setCurrentText(intent)
        self.update_capability()
