from pathlib import Path

from formats import BaseEncoder

try:
    import pillow_avif  # noqa: F401  (registers the Pillow AVIF plugin)

    AVIF_AVAILABLE = True


except ImportError:
    AVIF_AVAILABLE = False


class AVIFEncoder(BaseEncoder):
    def save(self, image, output_path, settings):

        if not AVIF_AVAILABLE:
            raise RuntimeError("AVIF support requires pillow-avif-plugin package")

        output = Path(output_path)

        output.parent.mkdir(parents=True, exist_ok=True)

        lossless = settings.get("lossless", False)

        quality = settings.get("quality", 80)

        alpha = settings.get("alpha", True)

        try:
            quality = int(quality)

        except Exception:
            raise ValueError("Invalid AVIF quality")

        quality = max(0, min(100, quality))

        # =====================
        # IMAGE MODE
        # =====================

        has_alpha = "A" in image.getbands()

        if alpha and has_alpha:
            image = image.convert("RGBA")

        else:
            if image.mode != "RGB":
                image = image.convert("RGB")

        save_settings = {"format": "AVIF", "lossless": bool(lossless)}

        if not lossless:
            save_settings["quality"] = quality

        icc_profile = image.info.get("icc_profile")

        if icc_profile:
            save_settings["icc_profile"] = icc_profile

        try:
            image.save(output, **save_settings)

        except TypeError as error:
            raise RuntimeError(
                "AVIF encoder options are not supported by current Pillow build"
            ) from error

        return output
