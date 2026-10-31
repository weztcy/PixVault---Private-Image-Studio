from pathlib import Path

from PIL import Image

from formats import BaseEncoder, get_pixvault_compression


class JPEGEncoder(BaseEncoder):
    def save(self, image, output_path, settings):

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        # Target size metadata is handled by TargetSizeOptimizer before final save.

        compression = get_pixvault_compression(image)
        if compression.get("mode") == "quality":
            settings["quality"] = compression.get(
                "quality", settings.get("quality", 85)
            )

        quality = max(1, min(95, int(settings.get("quality", 85))))

        # Preserve CMYK when requested
        if image.mode in ["RGBA", "LA"]:
            bg = Image.new("RGB", image.size, "white")
            bg.paste(image, mask=image.getchannel("A"))
            image = bg

        elif image.mode not in ["RGB", "CMYK"]:
            image = image.convert("RGB")

        save_settings = {
            "format": "JPEG",
            "quality": quality,
            "progressive": bool(settings.get("progressive", False)),
            "optimize": bool(settings.get("optimize", True)),
        }

        if image.info.get("icc_profile"):
            save_settings["icc_profile"] = image.info["icc_profile"]

        image.save(output, **save_settings)
        return output
