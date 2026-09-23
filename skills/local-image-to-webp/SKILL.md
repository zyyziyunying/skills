---
name: local-image-to-webp
description: Convert local raster images to WebP and clean transparent or faint alpha margins by default. Supports configurable threshold cropping, preserving canvas dimensions, and explicitly requested in-place WebP processing while retaining transparency.
---

# Local Image To WebP

Use for local image conversion and transparent-margin cleanup, including terse file paths. Do not integrate assets into Flutter or app builds unless requested.

## Default behavior and intent

- Convert at color quality 95, `alpha_quality=100`, `method=6`; preserve the original PNG/JPEG/etc. Write the same basename with `.webp` beside the source unless a `webp` subfolder is requested.
- **Clean alpha margins by default**, including faint outer pixels: crop to the bounding box of pixels with `alpha > 64` (8-bit alpha). This is this user's preferred asset-cleanup default, not a universally safe shadow threshold.
- The threshold selects the rectangular crop only. Preserve every original alpha value inside it; do not erase interior transparency, flatten edges, or fill a background. Pixels outside the crop, including faint shadows, are discarded. Do not claim that all visible content is unchanged.
- “去掉多余 alpha”, “去透明边距”, “还有空白”, or marked border screenshots mean margin cleanup in this workflow. They do **not** authorize removing the alpha channel or filling white.
- Only flatten transparency when the user explicitly requests an opaque background. If its color is unspecified, clarify it. The conversion script does not implement flattening.
- Honor “保留尺寸/不裁剪” with `--no-trim-transparent`. Honor “仅裁完全透明/保留所有阴影” with `--alpha-threshold 0`. Choose another threshold when the user's visual reference or instruction calls for it; do not blindly increase thresholds until a subject is clipped.

## Conversion and cropping

Use `scripts/convert_to_webp.py` with a Python runtime containing Pillow and WebP support (prefer the bundled runtime over system Python).

```bash
# Default: quality 95, threshold 64 margin cleanup, same-directory output
<python> <skill-dir>/scripts/convert_to_webp.py /path/to/image.png
# Preserve the canvas
<python> <skill-dir>/scripts/convert_to_webp.py --no-trim-transparent /path/to/image.png
# Strictly transparent margins only
<python> <skill-dir>/scripts/convert_to_webp.py --alpha-threshold 0 /path/to/image.png
# Inspect candidate bounds without writes
<python> <skill-dir>/scripts/convert_to_webp.py --diagnose /path/to/image.png
# Explicitly authorized replacement of an existing WebP
<python> <skill-dir>/scripts/convert_to_webp.py --in-place /path/to/image.webp
# Preserve existing WebP and write into its webp subfolder
<python> <skill-dir>/scripts/convert_to_webp.py --output-mode subdir /path/to/image.webp
```

- `--trim-transparent` remains an explicit synonym for the default. `--alpha-threshold` accepts 0–254; default 64. Alpha equal to the threshold does not determine the bounds.
- Apply EXIF orientation before cropping. Alpha images use RGBA; others use RGB. Images without alpha are not cropped. Entirely transparent images, or images with no alpha above the threshold, retain their dimensions and report the reason.
- If cleanup still seems insufficient or threatens intentional soft shadows, use `--diagnose` to compare bounds at 0, 16, 32, 64 and the selected threshold. Inspect a crop preview when needed. Do not confuse faint pixels with absence of margins.
- Existing WebP inputs are encoded losslessly to avoid repeated color degradation; sizes can increase. In-place replacement requires `--in-place` and explicit user authorization such as “直接替换”. Use the supplied source; do not silently substitute a similarly named PNG.
- Directory inputs recursively include common raster formats but skip existing WebPs and generated `webp` subtrees. Supply WebPs explicitly to process them. Animated/multipage inputs are rejected rather than silently reduced to a single frame.
- `same-dir` writes beside each source. `subdir` writes into a `webp` folder, retaining relative paths for directory inputs. Explicit source symlinks preserve their lexical location in subdir mode; same-dir keeps the existing resolved-target behavior for non-WebP sources.
- Keep collision, output-symlink, generated-subtree, and hard-link checks. In-place mode accepts explicit non-symlink WebP files only. Write a temporary output, verify it, then atomically replace the destination; a failed conversion leaves any existing destination intact.

## Verification and report

Reopen outputs and verify WebP format and expected dimensions. Compare the **cropped source alpha** to the decoded output alpha pixel-for-pixel. For lossless WebP processing also compare all cropped pixel channels. Report failures and leave successful outputs in place.

State output directory, successful/failed counts, quality or lossless mode, byte size, EXIF-corrected `prepared` dimensions, `output` dimensions, threshold, and removed margins in left/top/right/bottom order. Say whether dimensions changed and whether the source was preserved or explicitly replaced. Do not say “alpha removed” when only margins were cropped.
