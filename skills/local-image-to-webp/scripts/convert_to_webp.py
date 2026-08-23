#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import stat
import unicodedata
from pathlib import Path
from typing import Iterable

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
    if output_mode == "same-dir":
        return src.with_suffix(".webp")
    if root.is_file():
        return src.parent / "webp" / src.with_suffix(".webp").name
    rel = src.relative_to(root).with_suffix(".webp")
    return root / "webp" / rel


def generated_output_base(root: Path, output_mode: str) -> Path | None:
    if output_mode == "same-dir":
        return None
    return (root.parent if root.is_file() else root) / "webp"


def validate_generated_output_parent(base: Path, output: Path) -> None:
    """Reject unsafe existing components inside a generated output subtree."""
    component = base
    components = [component]
    for part in output.parent.relative_to(base).parts:
        component /= part
        components.append(component)

    for component in components:
        if component.is_symlink():
            raise SystemExit(
                f"refusing symlink in generated output path: {component}"
            )
        if component.exists() and not component.is_dir():
            raise SystemExit(
                f"refusing non-directory in generated output path: {component}"
            )


def portable_output_key(path: Path) -> str:
    """Use a conservative identity that is safe on case-insensitive filesystems."""
    return unicodedata.normalize("NFC", str(path.resolve())).casefold()


def plan_conversions(
    roots: Iterable[Path], output_mode: str
) -> list[tuple[Path, Path]]:
    conversions: list[tuple[Path, Path]] = []
    outputs: dict[str, tuple[Path, Path, Path]] = {}
    source_identities: set[Path] = set()
    planned_pairs: set[tuple[Path, str]] = set()
    generated_outputs: list[tuple[Path, Path]] = []

    for root in roots:
        output_base = generated_output_base(root, output_mode)
        for source_path in iter_sources(root):
            source_identity = source_path.resolve()
            out = output_path(source_path, root, output_mode)
            if out.is_symlink():
                raise SystemExit(f"refusing to replace symlink output: {out}")
            output_key = portable_output_key(out)
            pair = (source_identity, output_key)
            if pair in planned_pairs:
                continue

            previous_source = outputs.get(output_key)
            if previous_source is not None and previous_source[0] != source_identity:
                raise SystemExit(
                    f"multiple sources map to the same output: {out}: "
                    f"{previous_source[1]}, {source_path}"
                )

            planned_pairs.add(pair)
            source_identities.add(source_identity)
            outputs[output_key] = (source_identity, source_path, out)
            conversions.append((source_path, out))
            if output_base is not None:
                generated_outputs.append((output_base, out))

    for output_base, out in generated_outputs:
        validate_generated_output_parent(output_base, out)

    existing_outputs: list[Path] = []
    for _, out in conversions:
        if not out.exists():
            continue
        for previous_output in existing_outputs:
            if out.samefile(previous_output):
                raise SystemExit(
                    f"multiple outputs alias the same file: "
                    f"{previous_output}, {out}"
                )
        existing_outputs.append(out)
        for source in source_identities:
            if out.samefile(source):
                raise SystemExit(f"output aliases an input source: {out}: {source}")

    for out in existing_outputs:
        metadata = out.stat()
        if stat.S_ISREG(metadata.st_mode) and metadata.st_nlink > 1:
            raise SystemExit(f"refusing hard-linked output: {out}")

    return conversions


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", metavar="path", type=Path, nargs="+")
    parser.add_argument("--quality", type=int, default=95)
    parser.add_argument("--output-mode", choices=["same-dir", "subdir"], default="same-dir")
    args = parser.parse_args()

    roots = [Path(os.path.abspath(path.expanduser())) for path in args.paths]
    missing = [root for root in roots if not root.exists()]
    if missing:
        raise SystemExit(f"not found: {missing[0]}")
    if not features.check("webp"):
        raise SystemExit("Pillow WebP support is unavailable")

    planning_roots = (
        [root.resolve() for root in roots]
        if args.output_mode == "same-dir"
        else roots
    )
    conversions = plan_conversions(planning_roots, args.output_mode)

    converted: list[Path] = []
    failed: list[tuple[Path, Exception]] = []

    for src, out in conversions:
        try:
            out.parent.mkdir(parents=True, exist_ok=True)
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
