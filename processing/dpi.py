class DPIProcessor:
    def process(self, image, settings):

        horizontal, vertical = self.get_dpi(settings)

        result = image.copy()

        result.info["dpi"] = (horizontal, vertical)

        return result

    def get_dpi(self, settings):

        unit = str(settings.get("unit", "dpi")).lower()

        linked = settings.get("linked", True)

        horizontal = settings.get("horizontal")

        vertical = settings.get("vertical")

        if horizontal is None:
            horizontal = settings.get("value", settings.get("dpi", 300))

        if linked or vertical is None:
            vertical = horizontal

        try:
            horizontal = float(horizontal)

            vertical = float(vertical)

        except Exception:
            raise ValueError("Invalid DPI value")

        if horizontal <= 0 or vertical <= 0:
            raise ValueError("DPI must be greater than zero")

        if unit == "dpcm":
            horizontal *= 2.54

            vertical *= 2.54

        elif unit != "dpi":
            raise ValueError(f"Unsupported DPI unit: {unit}")

        return (horizontal, vertical)
