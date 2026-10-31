from pathlib import Path

from formats import BaseEncoder

try:
    import pillow_heif
    from PIL import Image

    pillow_heif.register_heif_opener()

    HEIF_AVAILABLE = True


except ImportError:
    HEIF_AVAILABLE = False


class HEICEncoder(BaseEncoder):
    def save(self, image, output_path, settings):

        if not HEIF_AVAILABLE:
            raise RuntimeError("HEIC support requires pillow-heif package")

        output = Path(output_path)

        output.parent.mkdir(parents=True, exist_ok=True)

        quality = settings.get("quality", 85)

        lossless = settings.get("lossless", False)

        chroma = settings.get("chroma", "4:2:0")

        alpha = settings.get("alpha", True)

        try:
            quality = int(quality)

        except Exception:
            raise ValueError("Invalid HEIC quality")

        quality = max(0, min(100, quality))

        image = self.prepare_image(image, alpha)

        save_settings = {
            "format": "HEIF",
            "quality": quality,
            "lossless": bool(lossless),
            "chroma": self.map_chroma(chroma),
        }

        if alpha and image.mode == "RGBA":
            save_settings["save_alpha"] = True

        try:
            image.save(output, **save_settings)

        except TypeError as error:
            raise RuntimeError(
                "Unsupported HEIC encoder option in current pillow-heif version"
            ) from error

        return output

    def prepare_image(self, image, alpha):

        if alpha and "A" in image.getbands():
            return image.convert("RGBA")

        return image.convert("RGB")

    def map_chroma(self, chroma):

        mapping = {"4:4:4": "444", "4:2:2": "422", "4:2:0": "420"}

        return mapping.get(str(chroma), "420")
