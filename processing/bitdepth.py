"""Bit-depth conversion operation.

The processor keeps Pillow images for compatibility with the batch pipeline.
Pillow cannot represent 16/32-bit *multichannel* images, so the target depth is
carried in ``image.info`` until the PNG/TIFF encoder writes actual high-bit data.
Output settings also carry ``bit_depth`` in case another operation copies the image.
"""

from PIL import Image

BIT_DEPTH_INFO_KEY = "_pixvault_target_bit_depth"


class BitDepthProcessor:
    def process(self, image, settings):
        value = settings.get("value", settings.get("bit_depth", 8))
        try:
            depth = int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("Invalid bit depth value") from exc
        return self.convert_bitdepth(image, depth)

    def convert_bitdepth(self, image, bit_depth):
        if bit_depth == 8:
            return self.convert_8bit(image)
        if bit_depth == 16:
            return self.convert_16bit(image)
        if bit_depth == 32:
            return self.convert_32bit(image)
        raise ValueError(f"Unsupported bit depth: {bit_depth}")

    @staticmethod
    def _mark(image, depth):
        result = image.copy()
        result.info[BIT_DEPTH_INFO_KEY] = depth
        return result

    def convert_8bit(self, image):
        mode = image.mode
        if mode in ("RGB", "RGBA", "L", "LA"):
            return self._mark(image, 8)
        import numpy as np

        if mode == "P":
            return self._mark(
                image.convert("RGBA" if "transparency" in image.info else "RGB"),
                8,
            )
        if mode.startswith("I;16"):
            # Pillow's .convert('L') clips 16-bit samples instead of scaling.
            pixels = np.asarray(image, dtype=np.uint16)
            pixels = ((pixels.astype(np.uint32) + 128) // 257).astype(np.uint8)
            return self._mark(Image.fromarray(pixels, mode="L"), 8)
        if mode in ("I", "F"):
            pixels = np.asarray(image)
            if mode == "F":
                pixels = np.nan_to_num(pixels, nan=0, posinf=255, neginf=0)
                # Floating-point grayscale generally uses normalized [0, 1].
                if pixels.size and pixels.min() >= 0 and pixels.max() <= 1:
                    pixels = pixels * 255.0
            pixels = np.clip(np.rint(pixels), 0, 255).astype(np.uint8)
            return self._mark(Image.fromarray(pixels, mode="L"), 8)
        if "A" in mode:
            return self._mark(image.convert("RGBA"), 8)
        return self._mark(image.convert("RGB"), 8)

    def convert_16bit(self, image):
        # Intentionally do NOT use Image.merge('RGB', I;16 channels): Pillow's
        # RGB mode is always 8 bits/channel. The encoder creates 16-bit samples.
        return self._mark(image, 16)

    def convert_32bit(self, image):
        # TIFF stores 32-bit float/channel; keep color channels until encoding.
        # Converting an RGB image to 'F' here would discard the color channels.
        return self._mark(image, 32)
