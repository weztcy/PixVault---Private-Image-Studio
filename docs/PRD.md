Saya pahami perubahan spesifikasi:
---

# Product Requirements Document (PRD)

# Project Name

## PixVault
### Privacy-First Local Image Processing & Optimization Tool

**Version:** 1.0  
**Platform:** Desktop Application  
**Technology:** Python  
**Category:** Image Processing Software

---

# 1. Product Overview

## 1.1 Product Description

PixVault adalah aplikasi desktop berbasis Python untuk melakukan pengolahan gambar secara lokal tanpa mengunggah file pengguna ke server atau cloud.

Aplikasi memungkinkan pengguna:

- Convert format gambar
- Compress image
- Resize image
- Crop image
- Rotate image
- Flip image
- Mengatur DPI
- Mengubah Color Space
- Mengubah Bit Depth
- Menghapus metadata
- Batch processing

Semua proses dilakukan langsung pada perangkat pengguna.

---

# 2. Product Vision

## Vision Statement

> Menjadi aplikasi image processing lokal yang aman, cepat, dan profesional dengan fokus utama pada privacy pengguna.

---

# 3. Product Mission

Menyediakan alternatif terhadap converter online dengan memberikan:

- Keamanan data
- Kontrol processing tingkat lanjut
- Performa desktop
- Workflow sederhana
- Dukungan batch processing

---

# 4. Core Product Principles

---

## 4.1 Privacy First

Prinsip utama:

> Your images never leave your device.

Aplikasi:

- Tidak upload gambar
- Tidak menggunakan cloud processing
- Tidak menyimpan file pengguna
- Tidak mengirim data gambar keluar aplikasi

---

## 4.2 Image Processing, Not Image Editing

PixVault bukan software editing.

Tidak menyediakan:

❌ Brightness  
❌ Contrast  
❌ Saturation  
❌ Filter  
❌ Effects  
❌ Drawing  
❌ Text overlay  
❌ Watermark  
❌ AI editing  
❌ Background removal  

Fokus:

✅ Conversion  
✅ Optimization  
✅ Transformation  
✅ Technical processing

---

## 4.3 Pipeline Architecture

Semua proses menggunakan konsep pipeline:

```
INPUT IMAGE

      ↓

FORMAT DETECTION

      ↓

IMAGE PROCESSING PIPELINE

      ↓

FORMAT ENCODER

      ↓

OUTPUT IMAGE
```

---

# 5. Target User

---

# 5.1 Photographer

Kebutuhan:

- Convert RAW
- Resize batch
- Export WebP/AVIF
- Remove metadata GPS

---

# 5.2 Developer

Kebutuhan:

- Optimize website assets
- Convert image formats
- Reduce file size

---

# 5.3 Designer

Kebutuhan:

- Export berbagai format
- Kontrol kualitas output

---

# 5.4 Business User

Kebutuhan:

- Compress dokumen gambar
- Privacy protection

---

# 5.5 General User

Kebutuhan:

- Convert foto
- Mengecilkan ukuran file
- Menghapus informasi pribadi

---

# 6. Technology Specification

## 6.1 Development Language

Primary:

```
Python
```

---

# 6.2 Desktop Framework

Recommended:

## GUI Layer

Pilihan:

### Option A

```
PySide6 / Qt
```

Kelebihan:

- Professional UI
- Cross platform
- Modern desktop application


### Option B

```
CustomTkinter
```

Kelebihan:

- Lightweight
- Simple development


Rekomendasi:

```
Python + PySide6
```

---

# 6.3 Image Processing Engine

Recommended stack:

## Core

```
Pillow (PIL)
```

Untuk:

- JPG
- PNG
- WebP
- GIF
- BMP
- TIFF


---

## Advanced Format Support

### AVIF

```
pillow-avif-plugin
```

---

### HEIC/HEIF

```
pillow-heif
```

---

### RAW

```
rawpy
```

---

# 6.4 Processing Architecture

Struktur:

```
PixVault

│
├── UI Layer
│
├── Processing Engine
│
├── Format Handler
│
├── Encoder Module
│
├── Metadata Module
│
└── Export Manager

```

---

# 7. Supported Input Formats

Aplikasi mendukung:

```
.jpg
.jpeg
.png
.webp
.avif
.gif
.svg
.bmp
.tiff
.tif
.heic
.heif
.ico
.raw
```

---

# 8. Supported Output Formats

User memilih satu output format:

```
JPG

PNG

WebP

AVIF

GIF

SVG

BMP

TIFF

HEIC

HEIF

ICO
```

---

# 9. Main Application Workflow

```
SELECT IMAGE

↓

IMAGE PREVIEW

↓

IMAGE INFORMATION

↓

OUTPUT FORMAT

↓

FORMAT SETTINGS

↓

IMAGE PROCESSING

↓

OUTPUT NAMING

↓

EXPORT LOCATION

↓

PROCESS

↓

RESULT
```

---

# 10. Feature Requirements

---

# 10.1 Image Input

## Requirements

User dapat:

### Single File

```
photo.jpg
```

---

### Multiple Files

```
photo1.jpg
photo2.png
photo3.webp
```

---

### Folder

```
/Photos
   /2026
      image.jpg
```

---

Optional:

```
☐ Include Subfolders
```

---

# 10.2 Automatic Format Detection

Aplikasi membaca:

- File type
- Resolution
- File size
- Color profile
- Bit depth
- Metadata


Example:

```
image.jpg


Format:
JPEG


Resolution:
4000×3000


Size:
3.2 MB


Color:
sRGB


Bit:
8-bit
```

---

# 10.3 Preview System

Requirement:

- Thumbnail preview
- Fixed container
- Scroll support


Specification:

```
Preview Container:

Height:
400px


Thumbnail:
120×120 px
```

---

# 10.4 Selected Image Manager

Fitur:

- Select image
- Select all
- Remove selected
- Clear all


Display:

```
SELECTED IMAGES (100)


☑ image001.jpg

4000×3000

2.5 MB

```

---

# 11. Output Format Module

---

# 11.1 JPEG

Options:

```
Quality:
0-100

Progressive:
ON/OFF

Optimize:
ON/OFF

Subsampling:

4:4:4
4:2:2
4:2:0
```

---

# 11.2 PNG

Options:

```
Compression:
0-9

Interlacing:
ON/OFF

Bit Depth:

8-bit
16-bit

Color:

RGB
RGBA
Grayscale
```

---

# 11.3 WebP

Options:

```
Mode:

Lossy
Lossless


Quality:

0-100


Method:

0-6


Alpha Quality:

0-100
```

---

# 11.4 AVIF

Options:

```
Mode:

Lossy
Lossless


Quality

Speed

Chroma:

4:4:4
4:2:2
4:2:0


Alpha
```

---

# 11.5 GIF

Options:

```
Colors:

2-256


Dithering


Transparency


Animation


Loop


Frame Delay
```

---

# 11.6 TIFF

Options:

```
Compression:

None

LZW

Deflate

PackBits

JPEG


Bit Depth:

8

16

32


DPI
```

---

# 11.7 HEIC/HEIF

Options:

```
Lossy

Lossless


Quality


Bit Depth:

8-bit

10-bit


Chroma:

4:4:4

4:2:0
```

---

# 11.8 ICO

Options:

```
Size:

16x16

32x32

48x48

64x64

128x128

256x256


Transparency

Bit Depth
```

---

# 12. Image Processing Module

Semua fitur dapat aktif bersamaan.

---

# 12.1 Resize

Methods:

```
Exact Dimensions

Width

Height

Longest Side

Shortest Side

Percentage
```

Options:

```
Keep Aspect Ratio
```

Resampling:

```
Nearest

Bilinear

Bicubic

Lanczos
```

---

# 12.2 Crop

Mode:

```
Aspect Ratio

Fixed Dimensions

Percentage

Custom Coordinates
```

Parameter:

```
Width

Height

X

Y
```

---

# 12.3 Rotate

Options:

```
90° Clockwise

180°

90° Counterclockwise

Custom Angle
```

---

# 12.4 Flip

Options:

```
Horizontal

Vertical

Both
```

---

# 12.5 Compression

Mode:

```
Quality

Target File Size
```

---

Quality:

```
Quality:
0-100
```

---

Target Size:

```
Target:

KB / MB


Accuracy:

Prioritize Size

Balanced

Prioritize Quality
```

---

# 12.6 DPI / Resolution

Options:

```
Unit:

DPI

DPCM
```

Parameters:

```
Horizontal

Vertical
```

---

# 12.7 Color Space Conversion

Support:

```
sRGB

Adobe RGB

Display P3

CMYK

Grayscale
```

Advanced:

```
Rendering Intent:

Perceptual

Relative Colorimetric

Saturation

Absolute Colorimetric
```

---

# 12.8 Bit Depth Conversion

Options:

```
8-bit

16-bit

32-bit
```

---

# 12.9 Metadata Removal

Modes:

```
Remove All Metadata


Custom
```

Custom:

```
EXIF

GPS Location

IPTC

XMP

ICC Profile

Maker Notes

Software Information

Copyright
```

---

# 13. Export System

---

# 13.1 Output Naming

Options:

```
Keep Original Filename

Add Suffix

Custom Pattern
```

Example:

Input:

```
photo.jpg
```

Output:

```
photo.webp

atau

photo_converted.webp
```

---

# 13.2 Export Location

Default:

```
Same directory as source
```

Example:

```
Photos

├── photo.jpg

└── photo.webp
```


Custom:

```
Select Folder
```

---

# 14. Processing Engine Requirements

## Batch Processing

Support:

```
1 image

10 images

1000+ images
```

---

Processing harus:

- Memory efficient
- Thread capable
- Tidak freeze UI


---

# 15. Progress & Result

Saat proses:

```
PROCESSING


████████░░ 80%


80 / 100 Images


Current:

photo080.jpg


Success:
79

Failed:
1
```

---

Selesai:

```
COMPLETE


100 Successful

0 Failed


Original:

500 MB


Output:

180 MB


Saved:

320 MB
```

---

# 16. Error Handling

Jika gagal:

```
97 Successful

3 Failed


View Errors
```

Detail:

```
image01.raw

Reason:

Unsupported format
```

---

# 17. Security Requirements

Mandatory:

- Local processing only
- No cloud upload
- No image telemetry
- No image analytics
- No permanent storage


---

# 18. Non Functional Requirements

## Performance

Target:

- 1000+ images batch
- Stable memory usage
- Responsive UI


---

## Reliability

Harus:

- Handle corrupted files
- Skip failed files
- Continue batch processing


---

## Compatibility

Target:

```
Windows 10+

Windows 11
```

Future:

```
macOS

Linux
```

---

# 19. MVP Scope

## Include

✅ Python Desktop Application  
✅ Local processing  
✅ Convert format  
✅ Batch processing  
✅ Resize  
✅ Crop  
✅ Rotate  
✅ Flip  
✅ Compression  
✅ DPI  
✅ Color Space  
✅ Bit Depth  
✅ Metadata Removal  
✅ Export management  
✅ Progress system  


---

## Exclude

❌ Cloud processing  
❌ Image editing  
❌ AI features  
❌ Background removal  
❌ Filters  
❌ Watermark  
❌ Drawing tools  


---

# 20. Brand Positioning

## Product Name Recommendation

## PixVault

Meaning:

- Pixel
- Vault
- Security


Tagline:

> Private image processing. Completely local.

---

# 21. Final Product Statement

> PixVault is a Python-based privacy-first desktop image processing application that allows users to convert, optimize, and transform images locally without uploading their data to the cloud.

---

Dokumen ini sudah menjadi PRD yang lebih sesuai untuk **implementasi nyata menggunakan Python**, dan bisa langsung dilanjutkan ke:
1. Software Architecture Document (SAD)
2. Folder/project structure Python
3. Database/config design
4. UI wireframe
5. Development roadmap MVP
6. Technical specification (PySide6 + Pillow pipeline)