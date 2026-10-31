from PIL import Image


class ImageTransformer:
    def process(self, image, settings):

        return self.apply_transform(image, settings)

    def apply_transform(self, image, settings):

        rotation = settings.get("rotation", 0)

        flip = settings.get("flip", "none")

        image = self.apply_rotation(image, rotation)

        image = self.apply_flip(image, flip)

        return image

    def apply_rotation(self, image, rotation):

        if rotation in (None, "none", 0, "0"):
            return image

        try:
            angle = float(rotation)

        except Exception:
            raise ValueError(f"Invalid rotation angle: {rotation}")

        if angle < -360 or angle > 360:
            raise ValueError("Rotation angle must be between -360 and 360")

        return image.rotate(-angle, expand=True)

    def apply_flip(self, image, flip):

        if flip in (None, "none"):
            return image

        if flip == "horizontal":
            return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        if flip == "vertical":
            return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

        if flip == "both":
            image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

            return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

        raise ValueError(f"Unsupported flip mode: {flip}")
