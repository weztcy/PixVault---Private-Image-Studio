from ui.components.format_options.base_format_options import BaseFormatOptions
from ui.components.format_options.common.checkbox_field import CheckboxField
from ui.components.format_options.common.dropdown_field import DropdownField
from ui.components.format_options.common.slider_field import SliderField


class SVGOptions(BaseFormatOptions):
    def __init__(self):

        super().__init__()

    def setup_ui(self):

        super().setup_ui()

        # =====================
        # SVG VERSION
        # =====================

        self.version = DropdownField("SVG Version", ["1.0", "1.1", "2.0"], "1.1")

        self.add_widget(self.version)

        # =====================
        # PRECISION
        # =====================

        self.precision = SliderField("Decimal Precision", 0, 10, 3)

        self.add_widget(self.precision)

        # =====================
        # OPTIMIZE PATH
        # =====================

        self.optimize_path = CheckboxField("Optimize SVG Paths", True)

        self.add_widget(self.optimize_path)

        # =====================
        # REMOVE METADATA
        # =====================

        self.remove_metadata = CheckboxField("Remove Metadata", True)

        self.add_widget(self.remove_metadata)

        # =====================
        # EMBED IMAGES
        # =====================

        self.embed_images = CheckboxField("Embed Raster Images", False)

        self.add_widget(self.embed_images)

        # =====================
        # TEXT PATH
        # =====================

        self.text_as_path = CheckboxField("Convert Text To Path", False)

        self.add_widget(self.text_as_path)

    def get_settings(self):

        return {
            "version": self.version.value(),
            "precision": self.precision.value(),
            "optimize_path": self.optimize_path.value(),
            "remove_metadata": self.remove_metadata.value(),
            "embed_images": self.embed_images.value(),
            "text_as_path": self.text_as_path.value(),
        }

    def reset(self):

        self.version.set_value("1.1")

        self.precision.set_value(3)

        self.optimize_path.set_value(True)

        self.remove_metadata.set_value(True)

        self.embed_images.set_value(False)

        self.text_as_path.set_value(False)
