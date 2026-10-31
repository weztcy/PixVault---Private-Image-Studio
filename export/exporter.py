from pathlib import Path

from formats import get_pixvault_compression
from export.naming import NamingEngine
from formats.encoder import EncoderManager


class Exporter:
    def __init__(self):

        self.encoder = EncoderManager()

        self.naming = NamingEngine()

    def export(self, image, source_path, output_folder, settings):

        if image is None:
            raise ValueError("Image data is missing")

        if not settings:
            raise ValueError("Export settings missing")

        output_folder = Path(output_folder)

        output_folder.mkdir(parents=True, exist_ok=True)

        format_name = settings.get("format")

        if not format_name:
            raise ValueError("Output format missing")

        format_name = self.encoder.normalize_format(format_name)

        if not self.encoder.is_supported(format_name):
            raise ValueError(f"Unsupported output format: {format_name}")

        # clone settings

        export_settings = dict(settings)

        export_settings["format"] = format_name

        compression = get_pixvault_compression(image)
        if compression:
            export_settings.update(compression)

        if export_settings.get("target_path"):
            output_path = Path(export_settings["target_path"])
            output_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            output_path = self.naming.generate(source_path, output_folder, export_settings)
            output_path = Path(output_path)

        result = self.encoder.save(image, output_path, export_settings)

        result = Path(result)

        if not result.exists():
            raise RuntimeError(f"Encoder failed creating file: {result}")

        return {"path": result, "format": format_name, "size": result.stat().st_size}
