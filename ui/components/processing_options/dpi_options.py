"""DPI and DPCM controls (horizontal and vertical can be linked)."""

from PySide6.QtCore import QSignalBlocker

from ui.components.processing_options.base_processing_options import (
    BaseProcessingOptions,
)
from ui.components.processing_options.common.checkbox_field import CheckboxField
from ui.components.processing_options.common.dropdown_field import DropdownField
from ui.components.processing_options.common.number_field import NumberField


class DPIOptions(BaseProcessingOptions):
    def setup_ui(self):
        super().setup_ui()
        self.unit_field = self.add_widget(
            DropdownField("Resolution Unit", ["DPI", "DPCM"], "DPI")
        )
        self.horizontal_field = self.add_widget(
            NumberField("Horizontal Resolution", 1, 10000, 300)
        )
        self.vertical_field = self.add_widget(
            NumberField("Vertical Resolution", 1, 10000, 300)
        )
        self.link_field = self.add_widget(
            CheckboxField("Keep Horizontal and Vertical Linked", True)
        )
        self.unit = self.unit_field.combo
        self.horizontal = self.horizontal_field.spin
        self.vertical = self.vertical_field.spin
        self.link = self.link_field.checkbox
        self.horizontal.valueChanged.connect(self.sync_vertical)
        self.vertical.valueChanged.connect(self.sync_horizontal)
        self.link.toggled.connect(self._link_changed)
        for field in (self.unit_field, self.horizontal_field, self.vertical_field):
            field.value_changed.connect(self.emit_settings)
        self.link_field.value_changed.connect(self.emit_settings)

    def sync_vertical(self, value):
        if self.link.isChecked():
            with QSignalBlocker(self.vertical):
                self.vertical.setValue(value)

    def sync_horizontal(self, value):
        if self.link.isChecked():
            with QSignalBlocker(self.horizontal):
                self.horizontal.setValue(value)

    def _link_changed(self, checked):
        if checked:
            self.sync_vertical(self.horizontal.value())
        self.emit_settings()

    def get_settings(self):
        return {
            "type": "dpi",
            "unit": self.unit.currentText().lower(),
            "horizontal": self.horizontal.value(),
            "vertical": self.vertical.value(),
            "linked": self.link.isChecked(),
        }

    def reset(self):
        # Unlink temporarily, avoiding an intermediate change to either input.
        self.link.setChecked(False)
        self.unit.setCurrentText("DPI")
        self.horizontal.setValue(300)
        self.vertical.setValue(300)
        self.link.setChecked(True)
        self.update_capability()

    def update_capability(self):
        supported = self.current_format not in ("SVG", "ICO")
        for field in (
            self.unit_field,
            self.horizontal_field,
            self.vertical_field,
            self.link_field,
        ):
            field.setEnabled(supported)
        self.show_warning(
            "This output format does not support DPI information."
            if not supported
            else ""
        )

    def validate(self):
        if self.current_format in ("SVG", "ICO"):
            return False, "The selected output format cannot store DPI information."
        return True, ""

    def set_defaults(self, settings):
        s = settings or {}
        self.link.setChecked(False)
        self.unit.setCurrentText(str(s.get("unit", "DPI")).upper())
        value = s.get("value", s.get("dpi", 300))
        self.horizontal.setValue(int(s.get("horizontal", value)))
        self.vertical.setValue(int(s.get("vertical", s.get("horizontal", value))))
        self.link.setChecked(bool(s.get("linked", True)))
        self.update_capability()
