# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller build script for PixVault.

Produces a single-file, windowed executable named ``PixVault.exe``.

Non-trivial details handled here:

- ``processing/profiles/*.icc`` profiles are bundled as data so the color
  space engine can load them from inside the frozen bundle.
- ``pillow-heif`` installs native pyd and DLLs in site-packages.
- Safe detection of user and global site-packages across Python versions.
"""

import glob
import os
import site
import sysconfig

try:
    import pillow_heif
    has_heif = True
except ImportError:
    pillow_heif = None
    has_heif = False

try:
    import pillow_avif
    has_avif = True
except ImportError:
    pillow_avif = None
    has_avif = False

search_dirs = []
for p in site.getsitepackages() + [site.getusersitepackages()]:
    if p and os.path.isdir(p) and p not in search_dirs:
        search_dirs.append(p)

try:
    purelib = os.path.abspath(sysconfig.get_paths()["purelib"])
    if purelib not in search_dirs and os.path.isdir(purelib):
        search_dirs.append(purelib)
except Exception:
    pass

heif_binaries = []
for sp in search_dirs:
    for pattern in (
        "_pillow_heif*.pyd",
        "libheif*.dll",
        "libde265*.dll",
        "libx265*.dll",
        "libstdc++*.dll",
        "libgcc_s_seh*.dll",
        "libwinpthread*.dll",
    ):
        for path in glob.glob(os.path.join(sp, pattern)):
            heif_binaries.append((path, "."))

avif_binaries = []
if has_avif and pillow_avif and hasattr(pillow_avif, "__file__"):
    avif_pkg_dir = os.path.dirname(pillow_avif.__file__)
    for path in glob.glob(os.path.join(avif_pkg_dir, "*.pyd")):
        avif_binaries.append((path, "pillow_avif"))

binaries = heif_binaries + avif_binaries

datas = [
    (os.path.join("processing", "profiles"), "processing/profiles"),
    (os.path.join("icons", "pixvault_icon.png"), "icons"),
]

hiddenimports = [
    "PySide6.QtSvg",
    "concurrent.futures",
    "multiprocessing",
    "core.worker",
    "core.pipeline",
]
if has_heif:
    hiddenimports.extend(["pillow_heif", "pillow_heif._lib_info"])
if has_avif:
    hiddenimports.append("pillow_avif")

a = Analysis(
    ["main.py"],
    pathex=[os.path.dirname(os.path.abspath(SPECPATH))],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="PixVault",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=os.path.join("packaging", "version_info.txt"),
    icon=os.path.join("icons", "pixvault.ico"),
)
