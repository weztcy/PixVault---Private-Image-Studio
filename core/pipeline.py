from pathlib import Path

from PIL import Image

from core.svg_renderer import SVGRenderer
from export.exporter import Exporter
from history.manager import HistoryManager
from processing.bitdepth import BitDepthProcessor
from processing.colorspace import ColorSpaceProcessor
from processing.compression import ImageCompressor
from processing.crop import ImageCropper
from processing.dpi import DPIProcessor
from processing.metadata import MetadataProcessor
from processing.resize import ImageResizer
from processing.transform import ImageTransformer


class ImagePipeline:
    PROCESS_ORDER = {
        "convert": 0,
        "resize": 1,
        "crop": 2,
        "transform": 3,
        "compression": 4,
        "bitdepth": 5,
        "colorspace": 6,
        "dpi": 7,
        "metadata": 8,
    }

    def __init__(self):

        self.processors = {
            "resize": ImageResizer(),
            "crop": ImageCropper(),
            "transform": ImageTransformer(),
            "compression": ImageCompressor(),
            "dpi": DPIProcessor(),
            "colorspace": ColorSpaceProcessor(),
            "bitdepth": BitDepthProcessor(),
            "metadata": MetadataProcessor(),
        }

        self.svg_renderer = SVGRenderer()

        self.exporter = Exporter()

        self.history = HistoryManager()

    # ==================================================
    # PIPELINE RUN
    # ==================================================

    def run(self, source_path, output_path, config, record_history=True):

        source_path = Path(source_path)

        output_path = Path(output_path)

        if not source_path.exists():
            raise FileNotFoundError(f"Input file not found: {source_path}")

        if not config:
            raise ValueError("Pipeline configuration missing")

        output_settings = config.get("output")

        if not output_settings:
            raise ValueError("Output configuration missing")

        self.validate_output_format(output_settings)

        operations = config.get("operations", [])

        try:
            # ==========================================
            # LOAD IMAGE
            # ==========================================

            image = self.load_image(source_path)

            # ==========================================
            # PROCESS ORDER
            # ==========================================

            operations = self.sort_operations(operations)

            for operation in operations:
                operation_type = operation.get("type")

                if not operation_type:
                    raise ValueError("Operation type missing")

                if operation_type in ("convert", "conversion"):
                    continue

                processor = self.processors.get(operation_type)

                if not processor:
                    raise ValueError(f"Unsupported operation: {operation_type}")

                image = processor.process(image, operation)

            # ==========================================
            # EXPORT
            # ==========================================

            export_result = self.exporter.export(
                image, source_path, output_path.parent, output_settings
            )

            final_path = Path(export_result["path"])

            if record_history:
                self.history.add(
                    source=str(source_path),
                    output=str(final_path),
                    format_name=export_result.get("format"),
                    operations=operations,
                    status="success",
                )

            return final_path

        except Exception as error:
            if record_history:
                self.history.add(
                    source=str(source_path),
                    output=str(output_path),
                    format_name=output_settings.get("format"),
                    operations=operations,
                    status="failed",
                    error=str(error),
                )

            raise

    # ==================================================
    # IMAGE LOADER
    # ==================================================

    def load_image(self, source_path):

        extension = source_path.suffix.lower()

        # SVG HANDLER

        if extension == ".svg":
            image = self.svg_renderer.render(source_path)

        else:
            with Image.open(source_path) as source_image:
                image = source_image.copy()

        return self.normalize_image(image)

    # ==================================================
    # IMAGE NORMALIZATION
    # ==================================================

    def normalize_image(self, image):

        if image.mode in ("RGB", "RGBA", "L"):
            return image

        return image.convert("RGBA")

    # ==================================================
    # OPERATION SORT
    # ==================================================

    def sort_operations(self, operations):

        return sorted(
            operations, key=lambda item: self.PROCESS_ORDER.get(item.get("type"), 999)
        )

    # ==================================================
    # OUTPUT VALIDATION
    # ==================================================

    def validate_output_format(self, output_settings):

        format_name = output_settings.get("format")

        if not format_name:
            raise ValueError("Output format missing")

        if not self.exporter.encoder.is_supported(format_name):
            raise ValueError(f"Unsupported output format: {format_name}")
