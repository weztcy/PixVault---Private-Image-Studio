from pathlib import Path

from formats import BaseEncoder, get_pixvault_compression


class WEBPEncoder(BaseEncoder):
    def save(self, image, output_path, settings):

        output = Path(output_path)

        output.parent.mkdir(parents=True, exist_ok=True)

        # Target size metadata is handled by TargetSizeOptimizer before final save.

        compression = get_pixvault_compression(image)
        if compression.get("mode") == "quality":
            settings["quality"] = compression.get(
                "quality", settings.get("quality", 85)
            )

        lossless = settings.get("lossless", False)

        quality = settings.get("quality", 85)

        method = settings.get("method", 4)

        alpha_quality = settings.get("alpha_quality", 100)

        try:
            quality = int(quality)

            method = int(method)

            alpha_quality = int(alpha_quality)

        except Exception:
            raise ValueError("Invalid WEBP settings")

        quality = max(0, min(100, quality))

        method = max(0, min(6, method))

        alpha_quality = max(0, min(100, alpha_quality))

        # =====================
        # COLOR MODE
        # =====================

        if image.mode not in ["RGB", "RGBA"]:
            if "A" in image.getbands():
                image = image.convert("RGBA")

            else:
                image = image.convert("RGB")

        save_settings = {
            "format": "WEBP",
            "lossless": bool(lossless),
            "method": method,
            "alpha_quality": alpha_quality,
        }

        if not lossless:
            save_settings["quality"] = quality

        icc_profile = image.info.get("icc_profile")

        if icc_profile:
            save_settings["icc_profile"] = icc_profile

        image.save(output, **save_settings)

        return output
