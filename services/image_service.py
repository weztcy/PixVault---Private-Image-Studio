from pathlib import Path

from PIL import Image

from core.pipeline import ImagePipeline


class ImageService:
    def __init__(self):

        pass

    def process_image(self, source_path, output_path, config):

        source = Path(source_path)

        output = Path(output_path)

        if not self.validate_input(source):
            raise ValueError(f"Invalid input image: {source}")

        if not config:
            raise ValueError("Processing configuration missing")

        pipeline = ImagePipeline()

        result = pipeline.run(source, output, config)

        return result

    def validate_input(self, file_path):

        path = Path(file_path)

        if not path.exists():
            return False

        if not path.is_file():
            return False

        if path.stat().st_size <= 0:
            return False

        try:
            with Image.open(path) as image:
                image.verify()

        except Exception:
            return False

        return True
