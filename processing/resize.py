from PIL import Image


class ImageResizer:
    RESAMPLING = {
        "nearest": Image.Resampling.NEAREST,
        "bilinear": Image.Resampling.BILINEAR,
        "bicubic": Image.Resampling.BICUBIC,
        "lanczos": Image.Resampling.LANCZOS,
    }

    def process(self, image, settings):

        return self.resize_image(image, settings)

    def resize_image(self, image, settings):

        method = settings.get("method")

        if not method:
            raise ValueError("Resize method missing")

        keep_ratio = settings.get("keep_ratio", True)

        resampling = self.RESAMPLING.get(
            settings.get("resampling", "lanczos"), Image.Resampling.LANCZOS
        )

        width, height = image.size

        new_width = None

        new_height = None

        # =====================
        # EXACT DIMENSION
        # =====================

        if method == "exact":
            new_width = settings.get("width")

            new_height = settings.get("height")

            self.validate_size(new_width, new_height)

        # =====================
        # WIDTH
        # =====================

        elif method == "width":
            value = settings.get("value")

            if value is None:
                raise ValueError("Resize width missing")

            new_width = int(value)

            if new_width <= 0:
                raise ValueError("Resize width must be positive")

            if keep_ratio:
                ratio = new_width / width

                new_height = round(height * ratio)

            else:
                new_height = height

        # =====================
        # HEIGHT
        # =====================

        elif method == "height":
            value = settings.get("value")

            if value is None:
                raise ValueError("Resize height missing")

            new_height = int(value)

            if new_height <= 0:
                raise ValueError("Resize height must be positive")

            if keep_ratio:
                ratio = new_height / height

                new_width = round(width * ratio)

            else:
                new_width = width

        # =====================
        # PERCENTAGE
        # =====================

        elif method == "percentage":
            value = settings.get("value")

            if value is None:
                raise ValueError("Resize percentage missing")

            value = float(value)

            if value <= 0 or value > 1000:
                raise ValueError("Resize percentage must be between 0 and 1000")

            ratio = value / 100

            new_width = round(width * ratio)

            new_height = round(height * ratio)

        # =====================
        # LONGEST SIDE
        # =====================

        elif method == "longest_side":
            target = settings.get("value")

            if target is None:
                raise ValueError("Longest side value missing")

            target = int(target)

            if target <= 0:
                raise ValueError("Longest side must be positive")

            ratio = target / max(width, height)

            new_width = round(width * ratio)

            new_height = round(height * ratio)

        # =====================
        # SHORTEST SIDE
        # =====================

        elif method == "shortest_side":
            target = settings.get("value")

            if target is None:
                raise ValueError("Shortest side value missing")

            target = int(target)

            if target <= 0:
                raise ValueError("Shortest side must be positive")

            ratio = target / min(width, height)

            new_width = round(width * ratio)

            new_height = round(height * ratio)

        else:
            raise ValueError(f"Unsupported resize method: {method}")

        self.validate_size(new_width, new_height)

        return image.resize((int(new_width), int(new_height)), resampling)

    def validate_size(self, width, height):

        if width is None or height is None:
            raise ValueError("Resize dimensions missing")

        width = int(width)

        height = int(height)

        if width <= 0 or height <= 0:
            raise ValueError("Resize dimensions must be positive")
