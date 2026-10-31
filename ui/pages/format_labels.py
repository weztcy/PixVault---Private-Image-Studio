"""Display labels for the output-format dropdowns of the page workspaces.

Pages show a friendly all-caps label such as "JPG" while the rest of the
pipeline keeps working with the canonical format keys (e.g. "JPEG").
"""

JPEG_DISPLAY_LABEL = "JPG"

# Every spelling a dropdown can show for the two JPEG extensions maps back to
# the canonical format key used by encoders and the options panel.
_JPEG_ALIASES = frozenset(
    {
        "jpg",
        "jpeg",
        "jpg / jpeg",
        "jpeg / jpg",
        "jpg/jpeg",
        "jpeg/jpg",
    }
)


def output_format_key(label):
    """Map a dropdown display label back to the canonical output-format key."""
    if not isinstance(label, str):
        return label
    normalized = label.strip().casefold()
    if normalized in _JPEG_ALIASES:
        return "JPG"
    return normalized.upper()
