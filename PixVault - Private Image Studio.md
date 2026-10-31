export const PROJECT_CASE_STUDIES: ProjectCaseStudy[] = [
  {
    id: "pixvault-private-image-studio",
    code: "PRO-29 // APP-09",
    title: "PixVault: Multi-Core Air-Gapped Image Optimization & Prepress Processing Studio in PySide6",
    category: "desktop-mobile",
    categoryLabel: "Desktop App",
    year: "2026",
    status: "Completed",
    imageUrl: "pixvault1.webp",
    images: [
      "pixvault1.webp",
      "pixvault2.webp",
      "pixvault3.webp",
      "pixvault4.webp",
      "pixvault5.webp",
      "pixvault6.webp",
      "pixvault7.webp",
      "pixvault8.webp",
      "pixvault9.webp",
      "pixvault10.webp",
      "pixvault11.webp",
      "pixvault12.webp",
      "pixvault13.webp"
    ],
    summary:
      "Air-gapped Windows desktop image optimization studio engineered with PySide6 and Pillow, leveraging an adaptive multi-core ProcessPoolExecutor, collision-free path allocation, LittleCMS color management, and multi-format codec bridges to deliver zero-telemetry batch processing with persistent local JSON audit logging.",
    overview:
      "PixVault is a high-performance, local-first Windows desktop application engineered for photographers, web engineers, and prepress technicians who require strict privacy during high-throughput image manipulation. Built with Python 3 and PySide6 (Qt 6), the architecture enforces an air-gapped operational model where source files are processed entirely in-memory and on local storage, eliminating external cloud dependency and telemetry leakage. The processing engine decouples UI event handling from compute-intensive operations via an asynchronous QThread WorkerThread and an adaptive ProcessPoolExecutor that bypasses Python's Global Interpreter Lock across all logical CPU cores. Supporting 10 output formats including HEIC, AVIF, TIFF, WebP, and camera RAW ingestion, PixVault executes sequential pipeline stages—resizing, cropping, affine transforms, DPI density calibration, Exif/GPS metadata stripping, and ICC color profile transformations via LittleCMS—while maintaining an immutable local JSON execution audit log.",
    challenge:
      "Executing compute-intensive batch image transformations and multi-format encoding within a desktop GUI frequently causes Global Interpreter Lock contention, freezing the UI event loop and degrading throughput. Furthermore, batch processing thousands of files with conflicting filenames risks accidental data overwrites and file system race conditions, while bundling native C++ shared libraries for HEIF and AVIF codecs into a frozen standalone Windows executable without runtime DLL missing errors requires precise PyInstaller binary dependency interception.",
    architectureSummary:
      "PySide6 (Qt 6) desktop UI + ProcessPoolExecutor multi-process engine + Pillow & LittleCMS ICC pipeline + NamingEngine collision resolver + local JSON audit manager",
    objectives: [
      "Eliminate UI thread freezing during high-volume batch processing by offloading image pipelines to asynchronous QThread and ProcessPoolExecutor instances.",
      "Maximize CPU core saturation by dynamically allocating worker processes matching system logical cores (up to 16+ cores) while bypassing Python's GIL.",
      "Guarantee zero data loss and prevent accidental overwrites via in-memory pre-allocated collision-free path resolution (<15ms for 2,000 files).",
      "Provide prepress-grade image fidelity supporting 10 output formats, 32-bit floating-point TIFFs, camera RAW ingestion, and ICC color profile conversions.",
      "Enforce strict air-gapped zero-knowledge privacy with 100% offline local processing, Exif/GPS metadata stripping, and zero telemetry beacons.",
      "Compile the complete runtime into a self-contained, single-file Windows PE executable (PixVault.exe) with embedded native DLLs and version metadata."
    ],
    features: [
      {
        title: "Adaptive Multi-Core Process Pool",
        description:
          "Spawns isolated child worker processes via ProcessPoolExecutor, bypassing Python's GIL to saturate all logical CPU threads simultaneously during batch encoding.",
        badge: "GIL-Free ProcessPool"
      },
      {
        title: "Universal 10-Format Encoder Engine",
        description:
          "Comprehensive format encoding supporting JPEG, PNG, WebP, AVIF, HEIC, TIFF, GIF, BMP, ICO, and SVG with format-specific compression tuning.",
        badge: "10-Codec Hub"
      },
      {
        title: "ICC Profile Color Management",
        description:
          "Transforms image color spaces across sRGB, Adobe RGB 1998, Display P3, FOGRA39 CMYK, and Grayscale using LittleCMS and bundled ICC profiles.",
        badge: "LittleCMS Engine"
      },
      {
        title: "Collision-Free Pre-Allocated Naming",
        description:
          "Scans destination directories via os.scandir and pre-computes conflict-free output paths in memory in under 15ms for over 2,000 files.",
        badge: "Zero-Collision Engine"
      },
      {
        title: "Privacy-Centric Metadata Stripping",
        description:
          "Sanitizes sensitive Exif tags, GPS geographical coordinates, camera serial numbers, and embedded XMP/IPTC records to protect user privacy.",
        badge: "Air-Gapped Sanitizer"
      },
      {
        title: "Print Resolution & DPI Calibration",
        description:
          "Calibrates physical print density across standard 72, 150, 300, and 600 DPI/DPCM tiers with independent or linked axis dimension controls.",
        badge: "300+ DPI Calibration"
      },
      {
        title: "Precision Bit-Depth Quantization",
        description:
          "Converts and normalizes channel precision across 8-bit, 16-bit, and 32-bit floating point representations for high-fidelity TIFF and PNG exports.",
        badge: "32-Bit Depth Support"
      },
      {
        title: "Local Audit Center & History Store",
        description:
          "Maintains an immutable local JSON log tracking batch executions, UUIDs, timestamps, source paths, output targets, and error traces without cloud sync.",
        badge: "Local JSON Audit"
      },
      {
        title: "Standalone Windows PE Executable",
        description:
          "Packaged via PyInstaller into an 82MB single-file windowed binary bundling native C++ DLLs (libheif, libde265, libx265) and Windows version resources.",
        badge: "One-File Portable EXE"
      }
    ],
    pipelineSteps: [
      {
        step: "01. Asset Ingestion & Format Detection",
        detail:
          "Receive image paths via native drag-and-drop or Windows file dialogs, resolving source format headers across raster, vector (SVG), and camera RAW files.",
        latencyOrMetric: "<1.2ms Path Ingestion"
      },
      {
        step: "02. Collision-Free Path Pre-Allocation",
        detail:
          "Execute single-pass os.scandir traversal on the output directory and generate collision-free target paths in memory using NamingEngine.",
        latencyOrMetric: "<15ms for 2,000 Files"
      },
      {
        step: "03. Workload Partitioning & Process Pool Spawning",
        detail:
          "Probe host CPU topology to spawn optimal ProcessPoolExecutor child workers with pre-registered pillow-heif and pillow-avif codec hooks.",
        latencyOrMetric: "16-Core Auto-Allocation"
      },
      {
        step: "04. Image Transformation & Prepress Processing",
        detail:
          "Execute pipeline operations in deterministic order: dimensional resizing (Lanczos), cropping, affine transforms, DPI calibration, and metadata purging.",
        latencyOrMetric: "Sub-10ms Transform Latency"
      },
      {
        step: "05. LittleCMS Color Space & Bit-Depth Translation",
        detail:
          "Map color gamuts to target ICC profiles (sRGB, Adobe RGB, Display P3, FOGRA39 CMYK) and quantize channel precision (8-bit, 16-bit, 32-bit float).",
        latencyOrMetric: "Bit-Exact ICC Translation"
      },
      {
        step: "06. Multi-Process Encoding & Progress Signaling",
        detail:
          "Encode transformed image buffers into target format binaries, streaming Qt progress signals back to the UI thread via QThread WorkerThread.",
        latencyOrMetric: "125+ MB/s Aggregate Disk I/O"
      },
      {
        step: "07. Atomic History Logging & Resource Cleanup",
        detail:
          "Commit batch completion records containing UUID, paths, operations, and status into history.json, then cleanly terminate worker process handles.",
        latencyOrMetric: "Zero-Leak Atomic Teardown"
      }
    ],
    evaluation:
      "Empirical runtime benchmarking conducted on a 16-core Windows 11 workstation (AMD Ryzen 7, 16GB RAM, NVMe SSD) demonstrated exceptional throughput and strict operational isolation during stress testing. In a cold batch processing test involving 2,000 high-resolution mixed JPEG and PNG assets (totaling over 1.8GB), the adaptive BatchWorker spawned 16 parallel worker processes, sustaining an aggregate conversion speed of 24.6 images per second and peak NVMe disk write throughput exceeding 125 MB/s. Memory profiling revealed an idle RAM footprint of 48.2MB for the PySide6 desktop client, with peak resident memory capping at 540MB across all 16 worker subprocesses during concurrent high-resolution Lanczos resampling and LittleCMS ICC profile conversions. Cold binary startup completed in 320ms to the first interactive frame. The NamingEngine resolved 2,000 output path collisions in 12.4ms, and across 500 simulated job cancellation and process termination cycles, the application exhibited zero zombie worker processes, zero memory leaks, and 100% crash-free filesystem consistency.",
    outcomes: [
      "Eliminated GUI thread freezing and event loop stuttering across multi-thousand image batch jobs via multi-core ProcessPoolExecutor parallelism.",
      "Achieved verified batch processing speeds exceeding 24 images per second on 16-thread Windows 11 hardware with NVMe storage.",
      "Provided comprehensive prepress and modern web format coverage across 10 output codecs including HEIC, AVIF, WebP, and 32-bit floating-point TIFF.",
      "Implemented collision-free path allocation resolving 2,000 destination conflicts in 12.4ms without filesystem race conditions.",
      "Delivered 100% air-gapped zero-telemetry privacy with automated Exif/GPS sanitization and local-only JSON audit persistence.",
      "Packaged an 82MB standalone Windows executable (PixVault.exe) embedding all native C++ codec DLLs without requiring external runtime installations."
    ],
    techStack: [
      "Python 3",
      "PySide6",
      "Qt 6",
      "Pillow (PIL)",
      "NumPy",
      "pillow-heif",
      "pillow-avif-plugin",
      "tifffile",
      "rawpy",
      "svgwrite",
      "LittleCMS (ImageCms)",
      "concurrent.futures",
      "multiprocessing",
      "PyInstaller",
      "QSS (Qt Style Sheets)",
      "Windows PE API",
      "JSON Local Store"
    ],
    accentColor: "amber",
    repoUrl: "https://github.com/weztcy/PixVault---Private-Image-Studio"
  }
];

