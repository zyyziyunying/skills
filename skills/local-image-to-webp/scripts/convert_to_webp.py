#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ctypes
import os
import shutil
import stat
import sys
import tempfile
import unicodedata
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageChops, ImageOps, features


EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".gif"}


def image_has_alpha(image: Image.Image) -> bool:
    return "A" in image.getbands() or "transparency" in image.info


def default_output_mode() -> int:
    current_umask = os.umask(0)
    os.umask(current_umask)
    return 0o666 & ~current_umask


def copy_output_metadata(source: Path, destination: Path) -> None:
    metadata = source.stat()
    if hasattr(os, "chown"):
        os.chown(destination, metadata.st_uid, metadata.st_gid)
    os.chmod(destination, stat.S_IMODE(metadata.st_mode))

    if sys.platform == "darwin":
        copyfile = ctypes.CDLL(None, use_errno=True).copyfile
        copyfile.argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_void_p,
            ctypes.c_uint,
        ]
        copyfile.restype = ctypes.c_int
        copyfile_acl_and_xattrs = (1 << 0) | (1 << 2)
        if copyfile(
            os.fsencode(source),
            os.fsencode(destination),
            None,
            copyfile_acl_and_xattrs,
        ) != 0:
            error_number = ctypes.get_errno()
            raise OSError(error_number, os.strerror(error_number), source)
    else:
        generated_times = destination.stat()
        shutil.copystat(source, destination)
        os.utime(
            destination,
            ns=(generated_times.st_atime_ns, generated_times.st_mtime_ns),
        )


def trim_transparent_edges(
    image: Image.Image,
) -> tuple[Image.Image, tuple[int, int, int, int], str]:
    """Crop fully transparent outer rows and columns without using a tolerance."""
    alpha_bbox = image.getchannel("A").getbbox()
    if alpha_bbox is None:
        return image, (0, 0, 0, 0), "fully-transparent-preserved"

    left, top, right, bottom = alpha_bbox
    margins = (left, top, image.width - right, image.height - bottom)
    if margins == (0, 0, 0, 0):
        return image, margins, "none"
    return image.crop(alpha_bbox), margins, "trimmed"


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
    parser.add_argument(
        "--trim-transparent",
        action="store_true",
        help="crop only fully transparent outer rows and columns",
    )
    parser.add_argument("--output-mode", choices=["same-dir", "subdir"], default="same-dir")
    args = parser.parse_args()

    if not 0 <= args.quality <= 100:
        parser.error("--quality must be between 0 and 100")

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

    converted: list[tuple[Path, str, tuple[int, int], int]] = []
    failed: list[tuple[Path, Exception]] = []

    for src, out in conversions:
        temporary_output: Path | None = None
        try:
            out.parent.mkdir(parents=True, exist_ok=True)
            output_exists = out.exists()
            with Image.open(src) as image:
                image = ImageOps.exif_transpose(image)
                has_alpha = image_has_alpha(image)
                icc_profile = image.info.get("icc_profile")
                image = image.convert("RGBA" if has_alpha else "RGB")
                prepared_size = image.size
                margins = (0, 0, 0, 0)
                trim_status = "off"
                if args.trim_transparent:
                    if has_alpha:
                        image, margins, trim_status = trim_transparent_edges(image)
                    else:
                        trim_status = "no-alpha"

                expected_alpha = image.getchannel("A").copy() if has_alpha else None
                save_options: dict[str, object] = {
                    "quality": args.quality,
                    "method": 6,
                }
                if has_alpha:
                    save_options.update(
                        alpha_quality=100,
                        exact=True,
                    )
                if icc_profile:
                    save_options["icc_profile"] = icc_profile
                with tempfile.NamedTemporaryFile(
                    prefix=f".{out.name}.",
                    suffix=".tmp",
                    dir=out.parent,
                    delete=False,
                ) as temporary_file:
                    temporary_output = Path(temporary_file.name)
                image.save(temporary_output, "WEBP", **save_options)

                with Image.open(temporary_output) as generated:
                    generated.load()
                    if generated.format != "WEBP":
                        raise ValueError(f"unexpected output format: {generated.format}")
                    if generated.size != image.size:
                        raise ValueError(
                            f"output size mismatch: {generated.size} != {image.size}"
                        )
                    if expected_alpha is not None:
                        actual_alpha = generated.convert("RGBA").getchannel("A")
                        alpha_difference = ImageChops.difference(
                            expected_alpha, actual_alpha
                        ).getbbox()
                        if alpha_difference is not None:
                            raise ValueError(
                                f"alpha verification failed: {alpha_difference}"
                            )
                    generated_format = generated.format
                    generated_size = generated.size

                if output_exists:
                    copy_output_metadata(out, temporary_output)
                else:
                    temporary_output.chmod(default_output_mode())
                os.replace(temporary_output, out)
                temporary_output = None
                output_bytes = out.stat().st_size

            converted.append((out, generated_format, generated_size, output_bytes))
            print(
                f"OK\t{out}\t{output_bytes} bytes\t"
                f"prepared={prepared_size[0]}x{prepared_size[1]}\t"
                f"output={image.size[0]}x{image.size[1]}\t"
                f"trim={trim_status}\t"
                f"margins={','.join(map(str, margins))}\t"
                f"alpha={'exact' if has_alpha else 'n/a'}"
            )
        except Exception as exc:  # noqa: BLE001
            failed.append((src, exc))
            print(f"FAIL\t{src}\t{exc}")
        finally:
            if temporary_output is not None:
                temporary_output.unlink(missing_ok=True)

    for out, generated_format, generated_size, output_bytes in converted:
        print(
            f"VERIFY\t{out}\t{generated_format}\t"
            f"{generated_size[0]}x{generated_size[1]}\t{output_bytes} bytes"
        )

    print(f"converted={len(converted)} failed={len(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
