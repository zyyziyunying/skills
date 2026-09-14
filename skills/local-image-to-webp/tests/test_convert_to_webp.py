from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from PIL import Image, ImageChops


SCRIPT = Path(__file__).parents[1] / "scripts" / "convert_to_webp.py"


def load_converter_module():
    spec = importlib.util.spec_from_file_location("convert_to_webp_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load converter: {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CONVERTER = load_converter_module()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ConvertToWebpTest(unittest.TestCase):
    def run_converter(self, *args: Path | str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *(str(arg) for arg in args)],
            check=False,
            capture_output=True,
            text=True,
        )

    def assert_webp(self, path: Path, size: tuple[int, int]) -> None:
        self.assertTrue(path.is_file(), path)
        with Image.open(path) as image:
            self.assertEqual("WEBP", image.format)
            self.assertEqual(size, image.size)

    def test_multiple_explicit_files_use_each_parent_subdir(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first = root / "first" / "one.png"
            second = root / "second" / "two.jpg"
            first.parent.mkdir()
            second.parent.mkdir()
            Image.new("RGBA", (13, 17), (1, 2, 3, 128)).save(first)
            Image.new("RGB", (19, 23), (4, 5, 6)).save(second)
            originals = {first: digest(first), second: digest(second)}

            result = self.run_converter("--output-mode", "subdir", first, second)

            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            self.assert_webp(first.parent / "webp" / "one.webp", (13, 17))
            self.assert_webp(second.parent / "webp" / "two.webp", (19, 23))
            self.assertEqual(originals, {first: digest(first), second: digest(second)})
            self.assertIn("converted=2 failed=0", result.stdout)

    def test_trim_transparent_crops_outer_alpha_and_preserves_alpha_exactly(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "trim.png"
            canvas = Image.new("RGBA", (12, 10), (0, 0, 0, 0))
            content = Image.new("RGBA", (5, 4), (20, 40, 60, 128))
            content.putpixel((0, 0), (20, 40, 60, 1))
            content.putpixel((4, 3), (20, 40, 60, 255))
            canvas.paste(content, (3, 2))
            canvas.save(source)
            original_digest = digest(source)

            result = self.run_converter(
                "--trim-transparent", "--output-mode", "subdir", source
            )

            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            output = root / "webp" / "trim.webp"
            self.assert_webp(output, (5, 4))
            with Image.open(output) as generated:
                actual_alpha = generated.convert("RGBA").getchannel("A").tobytes()
            self.assertEqual(content.getchannel("A").tobytes(), actual_alpha)
            self.assertEqual(original_digest, digest(source))
            self.assertIn("prepared=12x10", result.stdout)
            self.assertIn("output=5x4", result.stdout)
            self.assertIn("trim=trimmed", result.stdout)
            self.assertIn("margins=3,2,4,4", result.stdout)
            self.assertIn("alpha=exact", result.stdout)

    def test_trim_transparent_supports_pa_tiff_without_losing_alpha(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "palette-alpha.tiff"
            image = Image.new("PA", (8, 6), (0, 0))
            image.putpalette([0, 0, 0, 20, 40, 60] + [0, 0, 0] * 254)
            for y in range(1, 4):
                for x in range(2, 6):
                    image.putpixel((x, y), (1, 128))
            image.putpixel((2, 1), (1, 1))
            image.putpixel((5, 3), (1, 255))
            image.save(source)
            original_digest = digest(source)

            result = self.run_converter(
                "--trim-transparent", "--output-mode", "subdir", source
            )

            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            output = root / "webp" / "palette-alpha.webp"
            self.assert_webp(output, (4, 3))
            with Image.open(source) as reopened:
                expected_alpha = (
                    reopened.convert("RGBA").crop((2, 1, 6, 4)).getchannel("A")
                )
            with Image.open(output) as generated:
                actual_alpha = generated.convert("RGBA").getchannel("A")
            self.assertEqual(expected_alpha.tobytes(), actual_alpha.tobytes())
            self.assertEqual(original_digest, digest(source))
            self.assertIn("prepared=8x6", result.stdout)
            self.assertIn("output=4x3", result.stdout)
            self.assertIn("trim=trimmed", result.stdout)
            self.assertIn("margins=2,1,2,2", result.stdout)
            self.assertIn("alpha=exact", result.stdout)

    def test_trim_transparent_supports_png_color_key_transparency(self) -> None:
        cases = (
            ("L", 0, 128),
            ("RGB", (1, 2, 3), (20, 40, 60)),
        )
        for mode, transparent_color, visible_color in cases:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                source = root / f"color-key-{mode}.png"
                image = Image.new(mode, (6, 5), transparent_color)
                for y in range(1, 4):
                    for x in range(2, 5):
                        image.putpixel((x, y), visible_color)
                image.save(source, transparency=transparent_color)

                result = self.run_converter(
                    "--trim-transparent", "--output-mode", "subdir", source
                )

                self.assertEqual(0, result.returncode, result.stderr + result.stdout)
                output = root / "webp" / f"color-key-{mode}.webp"
                self.assert_webp(output, (3, 3))
                with Image.open(output) as generated:
                    self.assertEqual(
                        {255},
                        set(generated.convert("RGBA").getchannel("A").tobytes()),
                    )
                self.assertIn("prepared=6x5", result.stdout)
                self.assertIn("margins=2,1,1,1", result.stdout)
                self.assertIn("alpha=exact", result.stdout)

    def test_alpha_verification_failure_preserves_existing_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.png"
            Image.new("RGBA", (7, 9), (20, 40, 60, 128)).save(source)
            output_dir = root / "webp"
            output_dir.mkdir()
            output = output_dir / "source.webp"
            Image.new("RGB", (3, 5), (1, 2, 3)).save(output, "WEBP")
            original_output_digest = digest(output)
            stdout = io.StringIO()
            argv = [
                str(SCRIPT),
                "--output-mode",
                "subdir",
                str(source),
            ]

            with (
                mock.patch.object(
                    ImageChops,
                    "difference",
                    return_value=Image.new("L", (7, 9), 255),
                ),
                mock.patch.object(sys, "argv", argv),
                contextlib.redirect_stdout(stdout),
            ):
                returncode = CONVERTER.main()

            self.assertEqual(1, returncode)
            self.assertEqual(original_output_digest, digest(output))
            self.assertIn("alpha verification failed", stdout.getvalue())
            self.assertIn("converted=0 failed=1", stdout.getvalue())
            self.assertEqual([], list(output_dir.glob(".source.webp.*.tmp")))

    def test_alpha_verification_failure_leaves_no_new_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.png"
            Image.new("RGBA", (7, 9), (20, 40, 60, 128)).save(source)
            output = root / "webp" / "source.webp"
            stdout = io.StringIO()
            argv = [
                str(SCRIPT),
                "--output-mode",
                "subdir",
                str(source),
            ]

            with (
                mock.patch.object(
                    ImageChops,
                    "difference",
                    return_value=Image.new("L", (7, 9), 255),
                ),
                mock.patch.object(sys, "argv", argv),
                contextlib.redirect_stdout(stdout),
            ):
                returncode = CONVERTER.main()

            self.assertEqual(1, returncode)
            self.assertFalse(output.exists())
            self.assertIn("alpha verification failed", stdout.getvalue())
            self.assertEqual([], list(output.parent.glob(".source.webp.*.tmp")))

    def test_new_output_uses_normal_umask_permissions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.png"
            Image.new("RGB", (7, 9), (20, 40, 60)).save(source)

            result = self.run_converter("--output-mode", "subdir", source)

            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            output = root / "webp" / "source.webp"
            self.assertEqual(
                stat.S_IMODE(source.stat().st_mode),
                stat.S_IMODE(output.stat().st_mode),
            )

    def test_replaced_output_preserves_existing_permissions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.png"
            Image.new("RGB", (7, 9), (20, 40, 60)).save(source)
            output_dir = root / "webp"
            output_dir.mkdir()
            output = output_dir / "source.webp"
            Image.new("RGB", (3, 5), (1, 2, 3)).save(output, "WEBP")
            output.chmod(0o664)

            result = self.run_converter("--output-mode", "subdir", source)

            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            self.assertEqual(0o664, stat.S_IMODE(output.stat().st_mode))

    @unittest.skipUnless(sys.platform == "darwin", "macOS ACL behavior")
    def test_replaced_output_preserves_existing_acl(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.png"
            Image.new("RGB", (7, 9), (20, 40, 60)).save(source)
            output_dir = root / "webp"
            output_dir.mkdir()
            output = output_dir / "source.webp"
            Image.new("RGB", (3, 5), (1, 2, 3)).save(output, "WEBP")
            subprocess.run(
                ["chmod", "+a", "everyone allow read", str(output)],
                check=True,
            )
            original_acl = subprocess.run(
                ["ls", "-le", str(output)],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.splitlines()[1:]

            result = self.run_converter("--output-mode", "subdir", source)

            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            converted_acl = subprocess.run(
                ["ls", "-le", str(output)],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.splitlines()[1:]
            self.assertEqual(original_acl, converted_acl)

    def test_non_macos_metadata_copy_keeps_generated_timestamp(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            existing = root / "existing.webp"
            generated = root / "generated.webp"
            existing.write_bytes(b"old")
            generated.write_bytes(b"new")
            old_time_ns = 946684800_000_000_000
            generated_time_ns = 1_800_000_000_000_000_000
            os.utime(existing, ns=(old_time_ns, old_time_ns))
            os.utime(generated, ns=(generated_time_ns, generated_time_ns))

            with mock.patch.object(CONVERTER.sys, "platform", "linux"):
                CONVERTER.copy_output_metadata(existing, generated)

            self.assertEqual(generated_time_ns, generated.stat().st_mtime_ns)

    def test_exif_oriented_dimensions_are_reported_as_prepared_dimensions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "oriented.jpg"
            exif = Image.Exif()
            exif[274] = 6
            Image.new("RGB", (8, 4), (20, 40, 60)).save(source, exif=exif)

            result = self.run_converter("--output-mode", "subdir", source)

            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            self.assert_webp(root / "webp" / "oriented.webp", (4, 8))
            self.assertIn("prepared=4x8", result.stdout)
            self.assertIn("output=4x8", result.stdout)
            self.assertIn("trim=off", result.stdout)

    def test_transparent_margins_are_preserved_without_trim_flag(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "unchanged.png"
            canvas = Image.new("RGBA", (12, 10), (0, 0, 0, 0))
            canvas.paste(Image.new("RGBA", (5, 4), (20, 40, 60, 128)), (3, 2))
            canvas.save(source)

            result = self.run_converter("--output-mode", "subdir", source)

            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            self.assert_webp(root / "webp" / "unchanged.webp", (12, 10))
            self.assertIn("trim=off", result.stdout)
            self.assertIn("margins=0,0,0,0", result.stdout)

    def test_trim_transparent_preserves_fully_transparent_canvas(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "empty.png"
            Image.new("RGBA", (9, 11), (0, 0, 0, 0)).save(source)

            result = self.run_converter(
                "--trim-transparent", "--output-mode", "subdir", source
            )

            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            output = root / "webp" / "empty.webp"
            self.assert_webp(output, (9, 11))
            with Image.open(output) as generated:
                self.assertEqual(
                    {0},
                    set(generated.convert("RGBA").getchannel("A").tobytes()),
                )
            self.assertIn("trim=fully-transparent-preserved", result.stdout)

    def test_trim_transparent_is_noop_for_non_alpha_image(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "opaque.jpg"
            Image.new("RGB", (13, 17), (20, 40, 60)).save(source)

            result = self.run_converter(
                "--trim-transparent", "--output-mode", "subdir", source
            )

            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            output = root / "webp" / "opaque.webp"
            self.assert_webp(output, (13, 17))
            with Image.open(output) as generated:
                self.assertEqual("RGB", generated.mode)
            self.assertIn("trim=no-alpha", result.stdout)
            self.assertIn("alpha=n/a", result.stdout)

    def test_directory_input_preserves_relative_tree_in_subdir(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "images"
            nested = root / "nested"
            nested.mkdir(parents=True)
            first = root / "one.png"
            second = nested / "two.jpg"
            Image.new("RGB", (7, 11), (10, 20, 30)).save(first)
            Image.new("RGB", (29, 31), (40, 50, 60)).save(second)

            result = self.run_converter("--output-mode", "subdir", root)

            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            self.assert_webp(root / "webp" / "one.webp", (7, 11))
            self.assert_webp(root / "webp" / "nested" / "two.webp", (29, 31))
            self.assertIn("converted=2 failed=0", result.stdout)

    def test_directory_input_keeps_external_file_symlink_lexical(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            root = temp_root / "images"
            outside = temp_root / "outside"
            root.mkdir()
            outside.mkdir()
            real = root / "real.jpg"
            external = outside / "external.png"
            linked = root / "linked.png"
            Image.new("RGB", (7, 9), (1, 2, 3)).save(real)
            Image.new("RGBA", (11, 13), (4, 5, 6, 128)).save(external)
            linked.symlink_to(external)

            result = self.run_converter("--output-mode", "subdir", root)

            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            self.assert_webp(root / "webp" / "real.webp", (7, 9))
            self.assert_webp(root / "webp" / "linked.webp", (11, 13))
            self.assertTrue(linked.is_symlink())
            self.assertIn("converted=2 failed=0", result.stdout)

    def test_directory_input_can_convert_internal_file_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "images"
            root.mkdir()
            real = root / "real.png"
            alias = root / "alias.png"
            Image.new("RGB", (13, 17), (1, 2, 3)).save(real)
            alias.symlink_to(real)

            result = self.run_converter("--output-mode", "subdir", root)

            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            self.assert_webp(root / "webp" / "real.webp", (13, 17))
            self.assert_webp(root / "webp" / "alias.webp", (13, 17))
            self.assertTrue(alias.is_symlink())
            self.assertIn("converted=2 failed=0", result.stdout)

    def test_explicit_file_symlink_preserves_lexical_output_location(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            supplied = root / "supplied"
            target = root / "target"
            supplied.mkdir()
            target.mkdir()
            real = target / "real.png"
            alias = supplied / "alias.png"
            Image.new("RGBA", (23, 29), (4, 5, 6, 128)).save(real)
            original_digest = digest(real)
            alias.symlink_to(real)

            result = self.run_converter("--output-mode", "subdir", alias)

            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            self.assert_webp(supplied / "webp" / "alias.webp", (23, 29))
            self.assertFalse((target / "webp" / "real.webp").exists())
            self.assertTrue(alias.is_symlink())
            self.assertEqual(original_digest, digest(real))
            self.assertIn("converted=1 failed=0", result.stdout)

    def test_same_dir_file_symlink_preserves_legacy_target_location(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            supplied = root / "supplied"
            target = root / "target"
            supplied.mkdir()
            target.mkdir()
            real = target / "real.png"
            alias = supplied / "alias.png"
            Image.new("RGBA", (23, 29), (4, 5, 6, 128)).save(real)
            alias.symlink_to(real)

            result = self.run_converter("--output-mode", "same-dir", alias)

            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            self.assert_webp(target / "real.webp", (23, 29))
            self.assertFalse((supplied / "alias.webp").exists())
            self.assertTrue(alias.is_symlink())
            self.assertIn("converted=1 failed=0", result.stdout)

    def test_symlinked_source_parent_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            physical_parent = root / "physical"
            supplied_parent = root / "supplied"
            physical_parent.mkdir()
            supplied_parent.symlink_to(physical_parent, target_is_directory=True)
            source = supplied_parent / "source.png"
            Image.new("RGB", (31, 37), (7, 8, 9)).save(source)

            result = self.run_converter("--output-mode", "subdir", source)

            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            output = supplied_parent / "webp" / "source.webp"
            self.assert_webp(output, (31, 37))
            self.assertTrue(supplied_parent.is_symlink())
            self.assertTrue(output.samefile(physical_parent / "webp" / "source.webp"))
            self.assertIn("converted=1 failed=0", result.stdout)

    def test_colliding_explicit_outputs_fail_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            png = root / "same.png"
            jpg = root / "same.jpg"
            Image.new("RGB", (5, 5), (1, 1, 1)).save(png)
            Image.new("RGB", (5, 5), (2, 2, 2)).save(jpg)

            result = self.run_converter("--output-mode", "subdir", png, jpg)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("multiple sources map to the same output", result.stderr)
            self.assertFalse((root / "webp").exists())

    def test_case_variant_outputs_fail_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            lower = root / "same.jpg"
            upper = root / "SAME.png"
            Image.new("RGB", (11, 13), (1, 2, 3)).save(lower)
            Image.new("RGB", (17, 19), (4, 5, 6)).save(upper)

            result = self.run_converter("--output-mode", "subdir", lower, upper)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("multiple sources map to the same output", result.stderr)
            self.assertFalse((root / "webp").exists())

    def test_output_symlink_is_rejected_without_touching_its_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.png"
            Image.new("RGB", (37, 41), (7, 8, 9)).save(source)
            original_digest = digest(source)
            output_dir = root / "webp"
            output_dir.mkdir()
            output = output_dir / "source.webp"
            output.symlink_to(source)

            result = self.run_converter("--output-mode", "subdir", source)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("refusing to replace symlink output", result.stderr)
            self.assertTrue(output.is_symlink())
            self.assertEqual(original_digest, digest(source))

    def test_symlinked_generated_webp_directory_is_rejected_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "images"
            outside = Path(temp_dir) / "outside"
            root.mkdir()
            outside.mkdir()
            source = root / "source.png"
            Image.new("RGB", (31, 37), (7, 8, 9)).save(source)
            external_output = outside / "source.webp"
            Image.new("RGB", (3, 5), (10, 11, 12)).save(external_output, "WEBP")
            original_output_digest = digest(external_output)
            (root / "webp").symlink_to(outside, target_is_directory=True)

            result = self.run_converter("--output-mode", "subdir", source)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("refusing symlink in generated output path", result.stderr)
            self.assertTrue((root / "webp").is_symlink())
            self.assertEqual(original_output_digest, digest(external_output))

    def test_nested_generated_output_symlink_is_rejected_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "images"
            nested = root / "nested"
            outside = Path(temp_dir) / "outside"
            nested.mkdir(parents=True)
            outside.mkdir()
            source = nested / "source.png"
            Image.new("RGB", (31, 37), (7, 8, 9)).save(source)
            external_output = outside / "source.webp"
            Image.new("RGB", (3, 5), (10, 11, 12)).save(external_output, "WEBP")
            original_output_digest = digest(external_output)
            output_base = root / "webp"
            output_base.mkdir()
            (output_base / "nested").symlink_to(outside, target_is_directory=True)

            result = self.run_converter("--output-mode", "subdir", root)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("refusing symlink in generated output path", result.stderr)
            self.assertTrue((output_base / "nested").is_symlink())
            self.assertEqual(original_output_digest, digest(external_output))

    def test_runtime_parent_creation_failure_continues_and_summarizes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first = root / "first" / "one.png"
            second = root / "second" / "two.jpg"
            first.parent.mkdir()
            second.parent.mkdir()
            Image.new("RGB", (13, 15), (1, 2, 3)).save(first)
            Image.new("RGB", (17, 19), (4, 5, 6)).save(second)
            failed_parent = first.parent / "webp"
            real_mkdir = Path.mkdir

            def mkdir_with_first_failure(path: Path, *args, **kwargs) -> None:
                if path == failed_parent:
                    raise OSError("simulated mkdir failure")
                real_mkdir(path, *args, **kwargs)

            stdout = io.StringIO()
            argv = [
                str(SCRIPT),
                "--output-mode",
                "subdir",
                str(first),
                str(second),
            ]
            with (
                mock.patch.object(Path, "mkdir", new=mkdir_with_first_failure),
                mock.patch.object(sys, "argv", argv),
                contextlib.redirect_stdout(stdout),
            ):
                returncode = CONVERTER.main()

            output = stdout.getvalue()
            self.assertEqual(1, returncode)
            self.assertIn(f"FAIL\t{first}\tsimulated mkdir failure", output)
            self.assertFalse(failed_parent.exists())
            self.assert_webp(second.parent / "webp" / "two.webp", (17, 19))
            self.assertIn("converted=1 failed=1", output)

    def test_hard_linked_outputs_fail_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first = root / "first" / "one.png"
            second = root / "second" / "two.jpg"
            first.parent.mkdir()
            second.parent.mkdir()
            Image.new("RGB", (13, 15), (1, 2, 3)).save(first)
            Image.new("RGB", (17, 19), (4, 5, 6)).save(second)
            first_output = first.parent / "webp" / "one.webp"
            second_output = second.parent / "webp" / "two.webp"
            first_output.parent.mkdir()
            second_output.parent.mkdir()
            Image.new("RGB", (3, 5), (7, 8, 9)).save(first_output, "WEBP")
            os.link(first_output, second_output)
            original_output_digest = digest(first_output)

            result = self.run_converter("--output-mode", "subdir", first, second)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("multiple outputs alias the same file", result.stderr)
            self.assertEqual(original_output_digest, digest(first_output))
            self.assertEqual(original_output_digest, digest(second_output))

    def test_single_hard_linked_output_is_rejected_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.png"
            Image.new("RGB", (31, 37), (7, 8, 9)).save(source)
            output_dir = root / "webp"
            output_dir.mkdir()
            unrelated = root / "unrelated.bin"
            unrelated.write_bytes(b"unrelated data")
            original_digest = digest(unrelated)
            output = output_dir / "source.webp"
            os.link(unrelated, output)

            result = self.run_converter("--output-mode", "subdir", source)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("refusing hard-linked output", result.stderr)
            self.assertEqual(original_digest, digest(unrelated))
            self.assertEqual(original_digest, digest(output))


if __name__ == "__main__":
    unittest.main()
