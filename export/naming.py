import os
from datetime import datetime
from pathlib import Path


class NamingEngine:
    FORMAT_EXTENSION = {
        "JPEG": "jpg",
        "PNG": "png",
        "WEBP": "webp",
        "AVIF": "avif",
        "GIF": "gif",
        "BMP": "bmp",
        "TIFF": "tiff",
        "HEIC": "heic",
        "ICO": "ico",
        "SVG": "svg",
    }

    def generate(
        self,
        source_path,
        output_folder,
        settings,
        reserved_paths=None,
        existing_filenames=None,
    ):
        source = Path(source_path)
        output_folder = Path(output_folder)

        filename = self.create_filename(source, settings)

        return self.resolve_collision(
            output_folder / filename,
            reserved_paths=reserved_paths,
            existing_filenames=existing_filenames,
        )

    def normalize_extension(self, format_name):
        if not format_name:
            return None

        format_name = str(format_name).upper().strip().lstrip(".")
        extension = self.FORMAT_EXTENSION.get(format_name)

        if extension:
            return extension

        return format_name.lower()

    def create_filename(self, source, settings):
        extension = self.normalize_extension(settings.get("format"))

        if not extension:
            extension = source.suffix.replace(".", "")

        pattern = settings.get("pattern")
        suffix = settings.get("suffix")

        if pattern:
            try:
                filename = pattern.format(
                    name=source.stem,
                    format=extension,
                    date=datetime.now().strftime("%Y-%m-%d"),
                )
            except KeyError as error:
                raise ValueError(f"Invalid filename pattern: {error}")

            if not filename.lower().endswith(f".{extension}"):
                filename += f".{extension}"

            return filename

        name = source.stem

        if suffix:
            suffix = self.sanitize_name(suffix)
            if suffix:
                name += "_" + suffix

        return name + "." + extension

    def sanitize_name(self, value):
        value = str(value)
        forbidden = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]

        for char in forbidden:
            value = value.replace(char, "_")

        return value.strip()

    def resolve_collision(
        self,
        output_path,
        reserved_paths=None,
        existing_filenames=None,
    ):
        output_path = Path(output_path)
        norm_key = os.path.normcase(os.path.normpath(str(output_path)))

        def is_taken(path, key):
            if reserved_paths is not None:
                if key in reserved_paths or str(path) in reserved_paths:
                    return True
            if existing_filenames is not None:
                return os.path.normcase(path.name) in existing_filenames
            return path.exists()

        if not is_taken(output_path, norm_key):
            if reserved_paths is not None:
                reserved_paths.add(norm_key)
            if existing_filenames is not None:
                existing_filenames.add(os.path.normcase(output_path.name))
            return output_path

        counter = 1
        stem = output_path.stem
        suffix = output_path.suffix
        parent = output_path.parent

        while True:
            new_path = parent / f"{stem}_{counter:03d}{suffix}"
            new_key = os.path.normcase(os.path.normpath(str(new_path)))

            if not is_taken(new_path, new_key):
                if reserved_paths is not None:
                    reserved_paths.add(new_key)
                if existing_filenames is not None:
                    existing_filenames.add(os.path.normcase(new_path.name))
                return new_path

            counter += 1
