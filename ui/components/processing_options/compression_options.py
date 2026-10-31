"""Compression configuration and format capability logic."""

from ui.components.processing_options.base_processing_options import (
    BaseProcessingOptions,
)
from ui.components.processing_options.common.dropdown_field import DropdownField
from ui.components.processing_options.common.number_field import NumberField
from ui.components.processing_options.common.slider_field import SliderField


class CompressionOptions(BaseProcessingOptions):
    PRIORITY_KEYS = {
        "Prioritize Size": "size",
        "Balanced": "balanced",
        "Prioritize Quality": "quality",
    }

    QUALITY_SUPPORTED = {
        "JPEG",
        "WEBP",
        "AVIF",
        "HEIC",
        "TIFF",
    }

    TARGET_SIZE_SUPPORTED = {
        "JPEG",
        "PNG",
        "WEBP",
        "TIFF",
        "AVIF",
        "HEIC",
    }

    def setup_ui(self):

        super().setup_ui()

        self.mode_field = self.add_widget(
            DropdownField(
                "Compression Mode",
                [
                    "Quality",
                    "Target File Size",
                ],
                "Quality",
            )
        )

        self.quality_field = self.add_widget(
            SliderField(
                "Quality",
                1,
                100,
                85,
            )
        )

        self.size_field = self.add_widget(
            NumberField(
                "Target Size",
                1,
                1000000,
                1024,
            )
        )

        self.unit_field = self.add_widget(
            DropdownField(
                "Size Unit",
                [
                    "KB",
                    "MB",
                ],
                "KB",
            )
        )

        self.accuracy_field = self.add_widget(
            DropdownField(
                "Target Accuracy",
                list(self.PRIORITY_KEYS),
                "Balanced",
            )
        )

        # ==========================================
        # Compatibility references
        # Used by compress_page.py
        # ==========================================

        self.mode = self.mode_field.combo

        self.quality = self.quality_field.slider

        self.quality_label = self.quality_field.label

        self.size = self.size_field.spin

        self.size_label = self.size_field.label

        self.unit = self.unit_field.combo

        self.accuracy = self.accuracy_field.combo

        self.mode.currentTextChanged.connect(self._on_mode_changed)

        for control in (
            self.quality_field,
            self.size_field,
            self.unit_field,
            self.accuracy_field,
        ):
            control.value_changed.connect(self.emit_settings)

        self.update_ui()

    def _on_mode_changed(self, *_args):

        self.update_capability()

        self.update_ui()

        self.emit_settings()

    def update_ui(self):

        quality_mode = self.mode.currentText() == "Quality"

        self.quality_field.setVisible(quality_mode)

        self.size_field.setVisible(not quality_mode)

        self.unit_field.setVisible(not quality_mode)

        self.accuracy_field.setVisible(not quality_mode)

    def get_settings(self):

        if self.mode.currentText() == "Quality":
            return {
                "type": "compression",
                "mode": "quality",
                "quality": self.quality.value(),
                "optimize": True,
            }

        return {
            "type": "compression",
            "mode": "target_size",
            "size": self.size.value(),
            "unit": self.unit.currentText().lower(),
            "priority": self.PRIORITY_KEYS[self.accuracy.currentText()],
        }

    def reset(self):

        self.mode.setCurrentText("Quality")

        self.quality.setValue(85)

        self.size.setValue(1024)

        self.unit.setCurrentText("KB")

        self.accuracy.setCurrentText("Balanced")

        self.update_capability()

        self.update_ui()


def update_capability(self):

    format_name = self.current_format or ""

    model = self.mode.model()

    quality_item = model.item(0)

    target_item = model.item(1)

    quality_supported = format_name in self.QUALITY_SUPPORTED

    target_supported = format_name in self.TARGET_SIZE_SUPPORTED

    if quality_item:
        quality_item.setEnabled(quality_supported)

    if target_item:
        target_item.setEnabled(target_supported)

    current_mode = self.mode.currentText()

    if current_mode == "Quality":
        if not quality_supported:
            self.show_warning(f"{format_name} does not support quality compression.")

        else:
            self.show_warning("")

    elif current_mode == "Target File Size":
        if not target_supported:
            self.show_warning(
                f"{format_name} does not support target file size compression."
            )

        else:
            self.show_warning("Target size compression enabled.")

    self.update_ui()

    def validate(self):

        format_name = self.current_format or ""

        mode = self.mode.currentText()

        if mode == "Quality" and format_name not in self.QUALITY_SUPPORTED:
            return (False, f"{format_name} does not support quality compression.")

        if mode == "Target File Size" and format_name not in self.TARGET_SIZE_SUPPORTED:
            return (
                False,
                f"{format_name} does not support target file size compression.",
            )

        return True, ""

    def set_defaults(self, settings):

        s = settings or {}

        self.mode.setCurrentText(
            "Target File Size" if s.get("mode") == "target_size" else "Quality"
        )

        self.quality.setValue(int(s.get("quality", 85)))

        self.size.setValue(int(s.get("size", 1024)))

        self.unit.setCurrentText(str(s.get("unit", "KB")).upper())

        priority = str(s.get("priority", "balanced")).lower()

        label = next(
            (name for name, value in self.PRIORITY_KEYS.items() if value == priority),
            "Balanced",
        )

        self.accuracy.setCurrentText(label)

        self.update_capability()

        self.update_ui()
