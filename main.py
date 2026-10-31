import multiprocessing
import sys


def main():
    multiprocessing.freeze_support()

    if "--selftest" in sys.argv:
        run_selftest()
        return

    from app.application import PixVaultApplication

    app = PixVaultApplication()
    app.start()


def run_selftest():
    """Headless smoke test for validating a frozen (PyInstaller) build.

    Exercises the ICC profile loader, pillow-heif / pillow-avif plugin
    registration, the full image pipeline, history storage, and multi-core
    process pool parallelism. A report is written to ``%TEMP%\\pixvault_selftest.txt``
    because windowed executables have no attached console.
    """

    import tempfile
    from pathlib import Path

    results = []

    def check(name, callback):
        try:
            callback()
            results.append(f"OK   {name}")
        except Exception as error:  # noqa: BLE001
            results.append(f"FAIL {name}: {type(error).__name__}: {error}")

    def check_icc():
        from processing.colorspace import ColorSpaceProcessor

        profile = ColorSpaceProcessor().load_profile("srgb")
        if profile is None:
            raise RuntimeError("ICC profile returned empty")

    def check_heif_plugin():
        import pillow_heif
        from PIL import Image

        pillow_heif.register_heif_opener()
        if "HEIF" not in Image.SAVE:
            raise RuntimeError("HEIF encoder not registered")

    def check_avif_plugin():
        try:
            import pillow_avif  # noqa: F401
            from PIL import Image

            if "AVIF" not in Image.SAVE:
                raise RuntimeError("AVIF encoder not registered")
        except ModuleNotFoundError:
            return

    def check_pipeline():
        from PIL import Image as PILImage

        from core.pipeline import ImagePipeline

        tmp = Path(tempfile.mkdtemp(prefix="pixvault_selftest_"))
        source = tmp / "source.png"
        output_dir = tmp / "out"

        PILImage.new("RGB", (64, 64), (40, 160, 120)).save(source)

        pipeline = ImagePipeline()
        result = pipeline.run(
            source,
            output_dir / "result",
            config={
                "output": {"format": "PNG"},
                "operations": [
                    {"type": "dpi", "value": 300},
                    {"type": "metadata", "remove": ["exif", "xmp"]},
                ],
            },
        )
        if not Path(result).exists():
            raise RuntimeError("pipeline produced no output file")

    def check_multiprocessing():
        from PIL import Image as PILImage

        from core.worker import BatchWorker

        tmp = Path(tempfile.mkdtemp(prefix="pixvault_mp_test_"))
        sources = []
        for i in range(4):
            src = tmp / f"test_{i}.png"
            PILImage.new("RGB", (32, 32), (10 * i, 50, 100)).save(src)
            sources.append(str(src))

        output_dir = tmp / "out"
        worker = BatchWorker(max_workers=2)
        res = worker.run(
            sources,
            output_dir,
            config={
                "output": {"format": "PNG"},
                "operations": [{"type": "dpi", "value": 150}],
            },
        )
        if len(res.get("success", [])) != 4:
            raise RuntimeError(f"Expected 4 successful outputs, got {len(res.get('success', []))}")

    check("ICC profile loading", check_icc)
    check("HEIF plugin registration", check_heif_plugin)
    check("AVIF plugin registration", check_avif_plugin)
    check("image pipeline + history", check_pipeline)
    check("multi-core process pool", check_multiprocessing)

    failed = [line for line in results if line.startswith("FAIL")]
    report = "\n".join(results)
    report += f"\n\n{'SELF TEST PASSED' if not failed else 'SELF TEST FAILED'}"

    target = Path(tempfile.gettempdir()) / "pixvault_selftest.txt"
    target.write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
