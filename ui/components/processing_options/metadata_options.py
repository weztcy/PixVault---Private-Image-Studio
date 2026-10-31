"""Metadata removal UI using reusable DropdownField / CheckboxField controls."""

from ui.components.processing_options.base_processing_options import (
    BaseProcessingOptions,
)
from ui.components.processing_options.common.checkbox_group_field import (
    CheckboxGroupField,
)
from ui.components.processing_options.common.dropdown_field import DropdownField


class MetadataOptions(BaseProcessingOptions):
    METADATA_TYPES = [
        "EXIF",
        "GPS Location",
        "IPTC",
        "XMP",
        "ICC Profile",
        "Maker Notes",
        "Software Information",
        "Copyright Information",
    ]
    # Must match processing/metadata.py rather than user-facing descriptions.
    METADATA_KEYS = {
        "EXIF": "exif",
        "GPS Location": "gps",
        "IPTC": "iptc",
        "XMP": "xmp",
        "ICC Profile": "icc_profile",
        "Maker Notes": "maker_notes",
        "Software Information": "software",
        "Copyright Information": "copyright",
    }

    def setup_ui(self):
        super().setup_ui()
        self.mode_field = self.add_widget(
            DropdownField(
                "Metadata Removal Mode",
                ["Remove All Metadata", "Custom"],
                "Remove All Metadata",
            )
        )
        self.mode = self.mode_field.combo
        self.custom_container = self.add_widget(
            CheckboxGroupField("Metadata Types", self.METADATA_TYPES, True)
        )
        self.checkbox_fields = self.custom_container.fields
        self.checkboxes = (
            self.custom_container.checkboxes
        )  # native QCheckBox attributes
        self.types_label = self.custom_container.title_label
        self.custom_container.changed.connect(self.emit_settings)
        self.mode.currentTextChanged.connect(self._mode_changed)
        self.update_ui()

    def _mode_changed(self, *_args):
        self.update_ui()
        self.emit_settings()

    def update_ui(self):
        self.custom_container.setVisible(self.mode.currentText() == "Custom")

    def get_settings(self):
        if self.mode.currentText() == "Remove All Metadata":
            return {"type": "metadata", "mode": "all"}
        remove = [
            self.METADATA_KEYS[name]
            for name, checkbox in self.checkboxes.items()
            if checkbox.isChecked()
        ]
        return {"type": "metadata", "mode": "custom", "remove": remove}

    def reset(self):
        self.mode.setCurrentText("Remove All Metadata")
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(True)
        self.update_ui()

    def update_capability(self):
        self.show_warning(
            "SVG metadata is XML-based; EXIF removal does not apply."
            if self.current_format == "SVG"
            else ""
        )

    def set_defaults(self, settings):
        s = settings or {}
        self.mode.setCurrentText(
            "Custom" if s.get("mode") == "custom" else "Remove All Metadata"
        )
        selected = set(str(x).lower().replace(" ", "_") for x in s.get("remove", []))
        if s.get("mode") != "custom":
            selected = set(self.METADATA_KEYS.values())
        for name, checkbox in self.checkboxes.items():
            checkbox.setChecked(
                self.METADATA_KEYS[name] in selected
                or name.lower().replace(" ", "_") in selected
            )
        self.update_ui()
