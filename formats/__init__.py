from abc import ABC, abstractmethod


def get_pixvault_compression(image):
    """Return PixVault's compression metadata dict for ``image``.

    PixVault processors (``ImageCompressor`` / ``TargetSizeOptimizer``) store
    their settings as a dict under ``image.info["compression"]``.  Pillow
    itself exposes the *raw* TIFF (e.g. ``"tiff_lzw"``) or BMP (e.g. ``0``)
    compression tag under the exact same key just by opening such a file.

    Callers should only interpret the value as our settings dict when it
    actually *is* a dict; this helper therefore returns an empty dict for
    every other type (string, int, ...).
    """
    info = getattr(image, "info", None)
    if not isinstance(info, dict):
        return {}
    compression = info.get("compression", {})
    if not isinstance(compression, dict):
        return {}
    return compression


class BaseEncoder(ABC):
    """
    Base interface
    for all PixVault encoders.
    """

    @abstractmethod
    def save(self, image, output_path, settings):
        """
        Save processed image.

        Parameters:

        image:
            PIL.Image object


        output_path:
            Destination file path


        settings:
            Encoder configuration dictionary

        """

        raise NotImplementedError
