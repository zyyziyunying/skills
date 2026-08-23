---
name: local-image-to-webp
description: Convert local image folders or provided image files to WebP, usually quality 95, preserving originals and optionally placing outputs in a webp subfolder.
---

# Local Image To WebP

## Scope

Use this skill for terse local conversion requests such as:

- "把这个路径下的图片处理为质量95的web/webp"
- "建立 webp 子文件夹，整理进去"
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
   - Use `quality=95`, `alpha_quality=95`, and `method=6` unless the user gives a different quality.
   - Apply EXIF orientation correction.
   - Preserve alpha by converting alpha images to `RGBA`, otherwise use `RGB`.

3. Convert and verify.
   - Print each output path and byte size.
   - Re-open generated `.webp` files and report format, dimensions, and count.
   - If any file fails, report failures and leave successful outputs in place.

## Script

Use `scripts/convert_to_webp.py` when possible:

```bash
<python-with-pillow> <skill-dir>/scripts/convert_to_webp.py --quality 95 --output-mode subdir /path/to/images
<python-with-pillow> <skill-dir>/scripts/convert_to_webp.py --quality 95 --output-mode subdir /path/to/one.png /another/path/two.jpg
```

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

State the output directory, converted count, failed count, and verification result.
