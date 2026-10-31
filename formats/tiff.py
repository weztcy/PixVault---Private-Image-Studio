"""TIFF encoder supporting true 8-, 16- and 32-bit-per-channel samples."""

from pathlib import Path

from formats import BaseEncoder, get_pixvault_compression

BIT_DEPTH_INFO_KEY = "_pixvault_target_bit_depth"


def _compression_name(value):
    aliases = {
        "none": "none",
        "raw": "none",
        "uncompressed": "none",
        "lzw": "lzw",
        "tiff_lzw": "lzw",
        "deflate": "deflate",
        "zip": "deflate",
        "adobe_deflate": "deflate",
        "tiff_adobe_deflate": "deflate",
        "packbits": "packbits",
    }
    key = str(value).strip().lower()
    if key not in aliases:
        raise ValueError(f"Unsupported TIFF compression: {value}")
    return aliases[key]


def _tiff_mode(image):
    if image.mode in ("L", "LA", "RGB", "RGBA"):
        return image.mode
    if image.mode == "P":
        return "RGBA" if "transparency" in image.info else "RGB"
    if image.mode.startswith("I;") or image.mode in ("I", "F", "1"):
        return "L"
    return "RGBA" if "A" in image.mode else "RGB"


def _convert_array(image, mode, depth):
    import numpy as np

    if mode == "L" and image.mode.startswith("I;16"):
        source = np.asarray(image, dtype=np.uint16)
        kind = "uint16"
    elif mode == "L" and image.mode == "I":
        source = np.asarray(image, dtype=np.int32)
        kind = "int32"
    elif mode == "L" and image.mode == "F":
        source = np.asarray(image, dtype=np.float32)
        kind = "float32"
    else:
        source = np.asarray(image.convert(mode), dtype=np.uint8)
        kind = "uint8"

    if depth == 16:
        if kind == "uint8":
            return source.astype(np.uint16) * 257
        if kind == "float32":
            source = np.nan_to_num(source, nan=0, posinf=65535, neginf=0)
            if source.size and source.min() >= 0 and source.max() <= 1:
                source = source * 65535.0
        return np.clip(np.rint(source), 0, 65535).astype(np.uint16)
    if depth == 32:
        if kind == "uint8":
            return source.astype(np.float32) / 255.0
        if kind == "uint16":
            return source.astype(np.float32) / 65535.0
        return source.astype(np.float32)
    raise ValueError(f"Unsupported high-bit TIFF bit depth: {depth}")


def _write_with_tifffile(output, data, mode, compression, dpi, icc):
    try:
        import tifffile
    except ImportError as exc:
        raise RuntimeError(
            "16/32-bit color TIFF requires 'tifffile' and 'numpy'. "
            "Install with: pip install tifffile numpy"
        ) from exc

    import importlib.util

    requested_compression = compression
    if compression == "lzw" and importlib.util.find_spec("imagecodecs") is None:
        # tifffile's LZW codec needs the optional imagecodecs package;
        # Deflate is an equally lossless stdlib-backed fallback.
        compression = "deflate"
    if compression == "packbits" and importlib.util.find_spec("imagecodecs") is None:
        raise RuntimeError(
            "PackBits TIFF compression requires: pip install imagecodecs"
        )

    resolution = (float(dpi), float(dpi)) if isinstance(dpi, (int, float)) else dpi
    kwargs = {
        "photometric": "rgb" if mode in ("RGB", "RGBA") else "minisblack",
        "compression": None if compression == "none" else compression,
        "metadata": None,
        "resolution": resolution,
        "resolutionunit": "INCH",
    }
    if mode in ("RGBA", "LA"):
        kwargs["extrasamples"] = ["UNASSALPHA"]
    if icc:
        kwargs["extratags"] = [(34675, "B", len(icc), icc, False)]
    try:
        tifffile.imwrite(output, data, **kwargs)
    except Exception as exc:
        raise RuntimeError(
            f"Cannot encode {data.dtype} {mode} TIFF with {requested_compression} "
            f"compression: {exc}"
        ) from exc


class TIFFEncoder(BaseEncoder):
    def save(self, image, output_path, settings):
        from PIL import Image

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        # Target size metadata is handled by TargetSizeOptimizer before final save.
        depth = int(settings.get("bit_depth", image.info.get(BIT_DEPTH_INFO_KEY, 8)))
        if depth not in (8, 16, 32):
            raise ValueError("TIFF bit depth must be 8, 16 or 32 bits per channel.")
        compression_info = get_pixvault_compression(image)
        if compression_info.get("mode") == "target_size":
            settings["compression"] = "deflate"

        compression = _compression_name(settings.get("compression", "LZW"))
        dpi = settings.get("dpi", 300)
        dpi = (float(dpi), float(dpi)) if isinstance(dpi, (int, float)) else tuple(dpi)
        icc = image.info.get("icc_profile")
        mode = _tiff_mode(image)

        if depth == 8:
            if image.mode.startswith("I;16"):
                import numpy as np

                pix = np.asarray(image, dtype=np.uint16)
                pixels = ((pix.astype(np.uint32) + 128) // 257).astype(np.uint8)
                result = Image.fromarray(pixels, mode="L")
            elif image.mode in ("I", "F"):
                import numpy as np

                pixels = np.asarray(image)
                if image.mode == "F":
                    pixels = np.nan_to_num(pixels, nan=0, posinf=255, neginf=0)
                    if pixels.size and pixels.min() >= 0 and pixels.max() <= 1:
                        pixels = pixels * 255
                result = Image.fromarray(
                    np.clip(np.rint(pixels), 0, 255).astype(np.uint8), mode="L"
                )
            else:
                result = image.convert(mode)
            pillow_comp = {
                "none": "raw",
                "lzw": "tiff_lzw",
                "deflate": "tiff_adobe_deflate",
                "packbits": "packbits",
            }
            result.save(
                output,
                format="TIFF",
                compression=pillow_comp[compression],
                dpi=dpi,
                icc_profile=icc,
            )
            return output

        data = _convert_array(image, mode, depth)
        if mode == "L":
            # Pillow natively writes 16-bit integer and 32-bit float grayscale
            # with LZW, without relying on tifffile / imagecodecs.
            result = Image.fromarray(data)
            pillow_comp = {
                "none": "raw",
                "lzw": "tiff_lzw",
                "deflate": "tiff_adobe_deflate",
                "packbits": "packbits",
            }
            result.save(
                output,
                format="TIFF",
                compression=pillow_comp[compression],
                dpi=dpi,
                icc_profile=icc,
            )
        else:
            _write_with_tifffile(output, data, mode, compression, dpi, icc)
        return output
