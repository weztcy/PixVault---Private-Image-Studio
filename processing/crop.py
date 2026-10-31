class ImageCropper:
    def process(self, image, settings):

        return self.crop_image(image, settings)

    def crop_image(self, image, settings):

        mode = settings.get("mode")

        if not mode:
            raise ValueError("Crop mode missing")

        width, height = image.size

        crop_width = None

        crop_height = None

        left = None

        top = None

        # =====================
        # FIXED DIMENSIONS
        # =====================

        if mode in ("fixed", "fixed_dimensions"):
            crop_width = int(settings.get("width"))

            crop_height = int(settings.get("height"))

        # =====================
        # PERCENTAGE
        # =====================

        elif mode == "percentage":
            value = settings.get("value")

            if value is None:
                raise ValueError("Crop percentage missing")

            value = float(value)

            if value <= 0 or value > 100:
                raise ValueError("Crop percentage must be between 1 and 100")

            ratio = value / 100

            crop_width = round(width * ratio)

            crop_height = round(height * ratio)

        # =====================
        # ASPECT RATIO
        # =====================

        elif mode == "aspect_ratio":
            ratio = settings.get("ratio")

            if not ratio:
                raise ValueError("Crop ratio missing")

            try:
                ratio_w, ratio_h = map(float, ratio.split(":"))

            except Exception:
                raise ValueError(f"Invalid crop ratio: {ratio}")

            if ratio_w <= 0 or ratio_h <= 0:
                raise ValueError("Invalid ratio")

            target_ratio = ratio_w / ratio_h

            current_ratio = width / height

            if current_ratio > target_ratio:
                crop_height = height

                crop_width = round(height * target_ratio)

            else:
                crop_width = width

                crop_height = round(width / target_ratio)

        # =====================
        # CUSTOM COORDINATES
        # =====================

        elif mode == "coordinates":
            left = int(settings.get("x", 0))

            top = int(settings.get("y", 0))

            crop_width = int(settings.get("width"))

            crop_height = int(settings.get("height"))

        else:
            raise ValueError(f"Unsupported crop mode: {mode}")

        self.validate_crop_size(crop_width, crop_height, width, height)

        # default center crop

        if left is None:
            left = (width - crop_width) // 2

        if top is None:
            top = (height - crop_height) // 2

        if left < 0 or top < 0:
            raise ValueError("Crop position cannot be negative")

        if left + crop_width > width:
            raise ValueError("Crop exceeds image width")

        if top + crop_height > height:
            raise ValueError("Crop exceeds image height")

        return image.crop((left, top, left + crop_width, top + crop_height))

    def validate_crop_size(self, crop_width, crop_height, image_width, image_height):

        if crop_width is None or crop_height is None:
            raise ValueError("Crop dimensions missing")

        if crop_width <= 0 or crop_height <= 0:
            raise ValueError("Crop dimensions must be positive")

        if crop_width > image_width:
            raise ValueError("Crop width exceeds image width")

        if crop_height > image_height:
            raise ValueError("Crop height exceeds image height")
