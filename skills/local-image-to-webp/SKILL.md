---
name: local-image-to-webp
description: Convert local raster images to WebP, usually color quality 95, and optionally remove fully transparent outer alpha margins without changing visible content. Use for individual files or folders while preserving originals.
---

# Local Image To WebP

## Scope

Use this skill for terse local conversion requests such as:

- "把这个路径下的图片处理为质量95的web/webp"
- "建立 webp 子文件夹，整理进去"
- "去掉图片多余的透明/alpha 外边距"
- converting PNG/JPEG/GIF/TIFF/BMP assets for local use

Do not use for app builds or Flutter asset registration unless the user explicitly asks for repo integration.

## Workflow

1. Resolve source paths.
   - Accept a directory or explicit files.
   - For directories, convert common raster images recursively unless the user says only top-level.
   - Preserve originals.
   - If the user asks for a `webp` subfolder, put outputs there with the same base name.
   - Otherwise default to same-directory outputs.

2. Choose encoder.
   - Prefer bundled Python/Pillow when available; system `python3` on this machine may not have Pillow.
   - If needed, locate the bundled Python runtime or install Pillow into a local temporary target instead of modifying system Python.
   - Check WebP support before converting.
   - Use color `quality=95` unless the user gives a different color quality. Keep `alpha_quality=100` and `method=6`; alpha quality 100 keeps the alpha plane lossless.
   - Apply EXIF orientation correction.
   - Preserve alpha by converting alpha images to `RGBA`, otherwise use `RGB`.

3. Optionally remove excess transparent margins.
   - When the user asks to clean, crop, or remove excess transparent/alpha space, pass `--trim-transparent`.
   - Determine the crop from the alpha channel's non-zero bounding box. Remove only outer rows and columns whose alpha is exactly zero; do not use a tolerance, trim internal transparent regions, or discard faint antialiasing/shadow pixels.
   - Treat trimming as opt-in because it changes pixel dimensions. Ordinary WebP conversion preserves the EXIF-corrected, pre-trim dimensions.
   - If the image has no alpha channel, trimming is a no-op. If the whole canvas is transparent, preserve its dimensions rather than creating a zero-sized image.

4. Convert and verify.
   - Print each output path and byte size.
   - Re-open generated `.webp` files and verify format and dimensions.
   - For alpha images, compare the prepared source alpha plane with the decoded WebP alpha plane pixel-for-pixel. A mismatch is a conversion failure.
   - Report `prepared` as the EXIF-corrected, pre-trim dimensions and `output` as the generated WebP dimensions. When trimming, also report removed margins in left, top, right, bottom order; those margins use the prepared orientation.
   - If any file fails, report failures and leave successful outputs in place.

## Script

Use `scripts/convert_to_webp.py` when possible:

```bash
<python-with-pillow> <skill-dir>/scripts/convert_to_webp.py --quality 95 --output-mode subdir /path/to/images
<python-with-pillow> <skill-dir>/scripts/convert_to_webp.py --quality 95 --output-mode subdir /path/to/one.png /another/path/two.jpg
<python-with-pillow> <skill-dir>/scripts/convert_to_webp.py --quality 95 --trim-transparent --output-mode subdir /path/to/image.png
```

`--trim-transparent` is safe for mixed batches: alpha images are cropped to their exact non-zero alpha bounds, while JPEG and other non-alpha images keep their dimensions.

Output modes:

- `same-dir`: write beside each source
- `subdir`: for a directory input, write into its `webp` folder while preserving
  the relative tree; for explicit files, write each output into a `webp` folder
  under that file's parent directory

In `subdir` mode, the script rejects pre-existing symlinks and non-directory
components within the generated `webp` subtree. A source parent may itself be an
intentional directory symlink, and an explicitly supplied file symlink keeps its
lexical parent and filename for output placement.

In either mode, the script rejects an existing output file with multiple hard
links before conversion so overwriting it cannot mutate another pathname.

## Output

State the output directory, converted count, failed count, verification result, prepared/output dimensions, and whether trimming changed each image's dimensions. Preserve the source files.
