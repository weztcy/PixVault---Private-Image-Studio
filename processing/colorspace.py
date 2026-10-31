"""
PixVault ICC Color Space Engine
"""

import sys
from io import BytesIO
from pathlib import Path
from typing import ClassVar

from PIL import ImageCms


def _profile_directory():
    """Resolve the bundled ICC profile directory for both source and frozen runs."""
    meipass = getattr(sys, "_MEIPASS", None)
    if getattr(sys, "frozen", False) and meipass:
        return Path(meipass) / "processing" / "profiles"
    return Path(__file__).parent / "profiles"


class ColorSpaceProcessor:
    PROFILE_DIR = _profile_directory()

    PROFILE_FILES: ClassVar[dict[str, str]] = {
        "srgb": "sRGB.icc",
        "adobe_rgb": "AdobeRGB1998.icc",
        "display_p3": "DisplayP3.icc",
        "cmyk": "FOGRA39.icc",
        "grayscale": "Gray.icc",
    }

    INTENTS: ClassVar[dict[str, ImageCms.Intent]] = {
        "perceptual": ImageCms.Intent.PERCEPTUAL,
        "relative_colorimetric": ImageCms.Intent.RELATIVE_COLORIMETRIC,
        "saturation": ImageCms.Intent.SATURATION,
        "absolute_colorimetric": ImageCms.Intent.ABSOLUTE_COLORIMETRIC,
    }

    def process(self, image, settings):
        return self.convert_colorspace(
            image, settings.get("target", "srgb"), settings.get("intent", "perceptual")
        )

    def load_profile(self, target):
        path = self.PROFILE_DIR / self.PROFILE_FILES[target]
        if not path.exists():
            raise FileNotFoundError(f"Missing ICC profile: {path}")
        return ImageCms.getOpenProfile(str(path))

    def source_profile(self, image):
        profile = image.info.get("icc_profile")
        if profile:
            return ImageCms.ImageCmsProfile(BytesIO(profile))
        return ImageCms.createProfile("sRGB")

    def convert_colorspace(self, image, target, intent):
        target = str(target).lower()

        if target == "grayscale":
            return self.convert_grayscale(image)

        if image.mode not in ("RGB", "CMYK"):
            image = image.convert("RGB")

        src = self.source_profile(image)
        dst = self.load_profile(target)

        mode = "CMYK" if target == "cmyk" else "RGB"

        transform = ImageCms.buildTransform(
            src,
            dst,
            image.mode,
            mode,
            renderingIntent=self.INTENTS.get(intent, ImageCms.Intent.PERCEPTUAL),
        )

        result = ImageCms.applyTransform(image, transform)
        result.info["icc_profile"] = dst.tobytes()
        return result

    def convert_grayscale(self, image):
        result = image.convert("L")
        try:
            profile = self.load_profile("grayscale")
            result.info["icc_profile"] = profile.tobytes()
        except FileNotFoundError:
            pass
        return result
