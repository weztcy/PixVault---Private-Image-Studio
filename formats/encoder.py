from formats.avif import AVIFEncoder
from formats.bmp import BMPEncoder
from formats.gif import GIFEncoder
from formats.heic import HEICEncoder
from formats.ico import ICOEncoder
from formats.jpeg import JPEGEncoder
from formats.png import PNGEncoder
from formats.svg import SVGEncoder
from formats.tiff import TIFFEncoder
from formats.webp import WEBPEncoder


class EncoderManager:
    def __init__(self):

        self.encoder_registry = {
            "JPEG": JPEGEncoder,
            "PNG": PNGEncoder,
            "WEBP": WEBPEncoder,
            "AVIF": AVIFEncoder,
            "GIF": GIFEncoder,
            "BMP": BMPEncoder,
            "TIFF": TIFFEncoder,
            "HEIC": HEICEncoder,
            "ICO": ICOEncoder,
            "SVG": SVGEncoder,
        }

        self.aliases = {
            "JPG": "JPEG",
            "JPE": "JPEG",
            "JFIF": "JPEG",
            "TIF": "TIFF",
            "HEIF": "HEIC",
        }

    def normalize_format(self, format_name):

        if not format_name:
            raise ValueError("Output format is missing")

        format_name = str(format_name).strip().upper()

        format_name = format_name.lstrip(".")

        return self.aliases.get(format_name, format_name)

    def get_encoder(self, format_name):

        format_name = self.normalize_format(format_name)

        encoder_class = self.encoder_registry.get(format_name)

        if encoder_class is None:
            raise ValueError(f"Unsupported encoder: {format_name}")

        return encoder_class()

    def save(self, image, output_path, settings):

        if not settings:
            raise ValueError("Encoder settings are empty")

        format_name = settings.get("format")

        encoder = self.get_encoder(format_name)

        return encoder.save(image, output_path, settings)

    def available_formats(self):

        return sorted(self.encoder_registry.keys())

    def is_supported(self, format_name):

        try:
            normalized = self.normalize_format(format_name)

            return normalized in self.encoder_registry

        except Exception:
            return False
