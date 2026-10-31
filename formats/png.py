"""PNG encoder with real 8- and 16-bit-per-channel output.

Pillow handles regular 8-bit PNG. A small standards-compliant PNG writer handles
16-bit gray/gray-alpha/RGB/RGBA because Pillow cannot encode 16-bit RGB(A).
"""

import binascii
import struct
import zlib
from pathlib import Path

from formats import BaseEncoder, get_pixvault_compression

BIT_DEPTH_INFO_KEY = "_pixvault_target_bit_depth"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _chunk(chunk_type, payload):
    checksum = binascii.crc32(chunk_type + payload) & 0xFFFFFFFF
    return (
        struct.pack(">I", len(payload))
        + chunk_type
        + payload
        + struct.pack(">I", checksum)
    )


def _color_mode(image, requested):
    requested = str(requested or "auto").strip().lower()
    if requested in ("gray", "grayscale", "greyscale", "l"):
        return "L"
    if requested == "rgb":
        return "RGB"
    if requested == "rgba":
        return "RGBA"
    if requested not in ("auto", "same", "source"):
        # Compatibility with older conversion pages: previously any
        # unrecognized explicit color_type fell back to RGBA.
        return "RGBA"
    if image.mode in ("L", "LA", "RGB", "RGBA"):
        return image.mode
    if image.mode == "P":
        return "RGBA" if "transparency" in image.info else "RGB"
    if image.mode.startswith("I;") or image.mode in ("I", "F", "1"):
        return "L"
    return "RGBA" if "A" in image.mode else "RGB"


def _samples_16bit(image, mode):
    """Return a uint16 sample array, scaling 8-bit sources to full range."""
    import numpy as np

    if mode == "L" and image.mode.startswith("I;16"):
        data = np.asarray(image, dtype=np.uint16)
    elif mode == "L" and image.mode == "I":
        data = np.clip(np.asarray(image), 0, 65535).astype(np.uint16)
    elif mode == "L" and image.mode == "F":
        floats = np.nan_to_num(
            np.asarray(image, dtype=np.float64), nan=0.0, posinf=65535, neginf=0.0
        )
        # Normalized floating point values [0,1] map to [0,65535].
        if floats.size and floats.min() >= 0 and floats.max() <= 1:
            floats *= 65535.0
        data = np.clip(np.rint(floats), 0, 65535).astype(np.uint16)
    else:
        data = np.asarray(image.convert(mode), dtype=np.uint8).astype(np.uint16) * 257
    return np.ascontiguousarray(data.astype(">u2", copy=False))


def _save_16bit_png(image, output, mode, compression, icc, dpi):
    data = _samples_16bit(image, mode)
    width, height = image.size
    png_color_type = {"L": 0, "RGB": 2, "LA": 4, "RGBA": 6}[mode]
    channels = {"L": 1, "LA": 2, "RGB": 3, "RGBA": 4}[mode]
    row_bytes = width * channels * 2
    raw = data.tobytes()
    filtered = b"".join(
        b"\x00" + raw[i * row_bytes : (i + 1) * row_bytes] for i in range(height)
    )
    header = struct.pack(">IIBBBBB", width, height, 16, png_color_type, 0, 0, 0)
    with output.open("wb") as file:
        file.write(PNG_SIGNATURE)
        file.write(_chunk(b"IHDR", header))
        if icc:
            file.write(_chunk(b"iCCP", b"ICC Profile\x00\x00" + zlib.compress(icc)))
        if dpi is not None:
            x_dpi, y_dpi = (dpi, dpi) if isinstance(dpi, (int, float)) else dpi
            ppm = (int(round(float(x_dpi) / 0.0254)), int(round(float(y_dpi) / 0.0254)))
            file.write(_chunk(b"pHYs", struct.pack(">IIB", *ppm, 1)))
        file.write(_chunk(b"IDAT", zlib.compress(filtered, compression)))
        file.write(_chunk(b"IEND", b""))


class PNGEncoder(BaseEncoder):
    def save(self, image, output_path, settings):
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        # Target size metadata is handled by TargetSizeOptimizer before final save.

        compression = get_pixvault_compression(image)
        if compression.get("mode") == "target_size":
            settings["compression"] = 9

        depth = int(settings.get("bit_depth", image.info.get(BIT_DEPTH_INFO_KEY, 8)))
        if depth not in (8, 16):
            raise ValueError("PNG supports 8 or 16 bits per channel, not 32.")
        compression = int(settings.get("compression", 6))
        if not 0 <= compression <= 9:
            raise ValueError("PNG compression must be between 0 and 9.")
        mode = _color_mode(image, settings.get("color_type", "RGBA"))
        icc = image.info.get("icc_profile")
        dpi = settings.get("dpi")

        if depth == 16:
            _save_16bit_png(image, output, mode, compression, icc, dpi)
        else:
            if mode == "L" and image.mode.startswith("I;16"):
                # Pixel down-conversion must scale; Pillow normally clips.
                import numpy as np

                pixels = np.asarray(image, dtype=np.uint16)
                pixels = ((pixels.astype(np.uint32) + 128) // 257).astype(np.uint8)
                from PIL import Image

                converted = Image.fromarray(pixels, mode="L")
            else:
                converted = image.convert(mode)
            converted.save(
                output,
                format="PNG",
                compress_level=compression,
                icc_profile=icc,
                **({"dpi": dpi} if dpi is not None else {}),
            )
        return output
