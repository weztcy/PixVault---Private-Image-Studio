import base64
import html
import io
from pathlib import Path

from formats import BaseEncoder


class SVGEncoder(BaseEncoder):
    def save(self, image, output_path, settings):

        output = Path(output_path)

        output.parent.mkdir(parents=True, exist_ok=True)

        width = settings.get("width", image.width)

        height = settings.get("height", image.height)

        viewbox = settings.get("viewbox", f"0 0 {image.width} {image.height}")

        preserve_aspect = settings.get("preserve_aspect_ratio", True)

        optimize = settings.get("optimize", True)

        minify = settings.get("minify", True)

        try:
            width = int(width)

            height = int(height)

        except Exception:
            raise ValueError("Invalid SVG dimensions")

        # =====================
        # CREATE PNG EMBED
        # =====================

        buffer = io.BytesIO()

        image.save(buffer, format="PNG", optimize=True)

        encoded = base64.b64encode(buffer.getvalue()).decode("ascii")

        href = "data:image/png;base64," + encoded

        # =====================
        # ASPECT
        # =====================

        aspect = ""

        if preserve_aspect:
            aspect = 'preserveAspectRatio="xMidYMid meet"'

        # XML SAFE

        safe_viewbox = html.escape(str(viewbox))

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
width="{width}"
height="{height}"
viewBox="{safe_viewbox}"
{aspect}>
<image
width="{width}"
height="{height}"
href="{href}"
/>
</svg>"""

        if optimize:
            svg = self.optimize_svg(svg)

        if minify:
            svg = svg.replace("\n", "").replace("  ", "")

        output.write_text(svg, encoding="utf-8")

        return output

    def optimize_svg(self, svg):

        replacements = [("> <", "><"), ("\n\n", "\n")]

        for old, new in replacements:
            svg = svg.replace(old, new)

        return svg
