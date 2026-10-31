from pathlib import Path

from formats import BaseEncoder


class BMPEncoder(BaseEncoder):
    def save(self, image, output_path, settings):

        output = Path(output_path)

        output.parent.mkdir(parents=True, exist_ok=True)

        bit_depth = settings.get("bit_depth", 24)

        alpha = settings.get("alpha", False)

        try:
            bit_depth = int(bit_depth)

        except Exception:
            raise ValueError("Invalid BMP bit depth")

        prepared = self.prepare_image(image, bit_depth, alpha)

        prepared.save(output, format="BMP")

        return output

    def prepare_image(self, image, bit_depth, alpha):

        if bit_depth == 32:
            if alpha:
                return image.convert("RGBA")

            return image.convert("RGB")

        if bit_depth == 24:
            return image.convert("RGB")

        if bit_depth == 8:
            return image.convert("P", colors=256)

        if bit_depth == 4:
            return image.convert("P", colors=16)

        if bit_depth == 1:
            return image.convert("1")

        if bit_depth == 16:
            raise ValueError("BMP 16-bit output is not supported by this encoder")

        raise ValueError(f"Unsupported BMP bit depth: {bit_depth}")
