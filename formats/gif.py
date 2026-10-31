from pathlib import Path

from PIL import Image

from formats import BaseEncoder


class GIFEncoder(BaseEncoder):
    def save(self, image, output_path, settings):

        output = Path(output_path)

        output.parent.mkdir(parents=True, exist_ok=True)

        colors = settings.get("colors", 256)

        dithering = str(settings.get("dithering", "floyd")).lower()

        transparency = settings.get("transparency", True)

        animation = settings.get("animation", False)

        loop_mode = settings.get("loop", "infinite")

        duration = settings.get("duration", 100)

        frames = settings.get("frames")

        try:
            colors = int(colors)

            duration = int(duration)

        except Exception:
            raise ValueError("Invalid GIF settings")

        colors = max(2, min(256, colors))

        duration = max(10, duration)

        if dithering == "none":
            dither = Image.Dither.NONE

        else:
            dither = Image.Dither.FLOYDSTEINBERG

        def prepare_frame(frame):

            rgba = frame.convert("RGBA")

            return rgba.convert("P", colors=colors, dither=dither)

        processed_frames = []

        if animation and frames:
            for frame in frames:
                processed_frames.append(prepare_frame(frame))

        else:
            processed_frames.append(prepare_frame(image))

        save_settings = {"format": "GIF", "duration": duration}

        if animation and len(processed_frames) > 1:
            save_settings.update(
                {"save_all": True, "append_images": processed_frames[1:]}
            )

        if loop_mode == "infinite":
            save_settings["loop"] = 0

        else:
            loop_count = settings.get("loop_count", 1)

            try:
                loop_count = max(0, int(loop_count))

            except Exception:
                loop_count = 1

            save_settings["loop"] = loop_count

        if transparency:
            save_settings["transparency"] = 0

        processed_frames[0].save(output, **save_settings)

        return output
