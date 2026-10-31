from pathlib import Path

from PIL import Image

from formats import BaseEncoder


class ICOEncoder(BaseEncoder):
    VALID_SIZES = [16, 24, 32, 48, 64, 128, 256]

    def save(self, image, output_path, settings):

        output = Path(output_path)

        output.parent.mkdir(parents=True, exist_ok=True)

        sizes = settings.get("sizes", self.VALID_SIZES)

        bit_depth = int(settings.get("bit_depth", 32))

        transparency = settings.get("transparency", True)

        sizes = self.validate_sizes(sizes)

        image = self.prepare_image(image, transparency, bit_depth)

        ico_sizes = [(size, size) for size in sizes]

        image.save(output, format="ICO", sizes=ico_sizes)

        return output

    def validate_sizes(self, sizes):

        result = []

        for size in sizes:
            try:
                size = int(size)

            except Exception:
                continue

            if size in self.VALID_SIZES:
                result.append(size)

        if not result:
            result = [256]

        return sorted(set(result))

    def prepare_image(self, image, transparency, bit_depth):

        if bit_depth == 32:
            image = image.convert("RGBA")

        elif bit_depth == 24:
            image = image.convert("RGB")

        elif bit_depth == 8:
            image = image.convert("P", colors=256)

        else:
            raise ValueError(f"Unsupported ICO bit depth: {bit_depth}")

        if not transparency and image.mode == "RGBA":
            background = Image.new("RGB", image.size, "white")

            background.paste(image, mask=image.getchannel("A"))

            image = background

        return image
