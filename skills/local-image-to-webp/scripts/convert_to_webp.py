#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps, features


EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".gif"}


def iter_sources(path: Path) -> list[Path]:
    if path.is_file():
        return [path] if path.suffix.lower() in EXTENSIONS else []
    return sorted(
        p
        for p in path.rglob("*")
        if p.is_file()
        and p.suffix.lower() in EXTENSIONS
        and "webp" not in p.relative_to(path).parts
    )


def output_path(src: Path, root: Path, output_mode: str) -> Path:
    if output_mode == "same-dir" or root.is_file():
        return src.with_suffix(".webp")
    rel = src.relative_to(root).with_suffix(".webp")
    return root / "webp" / rel


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--quality", type=int, default=95)
    parser.add_argument("--output-mode", choices=["same-dir", "subdir"], default="same-dir")
    args = parser.parse_args()

    root = args.path.expanduser().resolve()
    if not root.exists():
        raise SystemExit(f"not found: {root}")
    if not features.check("webp"):
        raise SystemExit("Pillow WebP support is unavailable")

    converted: list[Path] = []
    failed: list[tuple[Path, Exception]] = []

    for src in iter_sources(root):
        out = output_path(src, root, args.output_mode)
        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            with Image.open(src) as image:
                image = ImageOps.exif_transpose(image)
                has_alpha = image.mode in ("RGBA", "LA") or (
                    image.mode == "P" and "transparency" in image.info
                )
                image = image.convert("RGBA" if has_alpha else "RGB")
                image.save(
                    out,
                    "WEBP",
                    quality=args.quality,
                    alpha_quality=args.quality,
                    method=6,
                )
            converted.append(out)
            print(f"OK\t{out}\t{out.stat().st_size} bytes")
        except Exception as exc:  # noqa: BLE001
            failed.append((src, exc))
            print(f"FAIL\t{src}\t{exc}")

    for out in converted:
        with Image.open(out) as image:
            print(
                f"VERIFY\t{out}\t{image.format}\t"
                f"{image.size[0]}x{image.size[1]}\t{out.stat().st_size} bytes"
            )

    print(f"converted={len(converted)} failed={len(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
