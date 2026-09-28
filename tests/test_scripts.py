"""Offline behavioral checks; all mutation tests run in temporary library copies."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "assets" / "handraw-style"
COUNT = len(json.loads((LIB / "skills/handdraw-style-prompter/references/styles.json").read_text(encoding="utf-8")))


def snapshot(root):
    return {str(p.relative_to(root)): (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


class ScriptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="comic skill test ")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.lib = self.base / "relocated library"
        shutil.copytree(LIB, self.lib, ignore=shutil.ignore_patterns("__pycache__", "downloads", ".style-import.lock"))
        self.image = self.base / "sample.png"
        Image.new("RGB", (64, 64), "white").save(self.image)
        self.importer = self.lib / "scripts/import_manual_style.py"
        self.validator = self.lib / "skills/handdraw-style-prompter/scripts/validate_library.py"

    def run_python(self, *args):
        return subprocess.run([sys.executable, "-B", "-X", "utf8", *map(str, args)],
                              cwd=self.base, capture_output=True, text=True, encoding="utf-8",
                              env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})

    def args(self, image=None):
        return ["--source-name", "测试画风", "--generation-name", "Test Style",
                "--traits", "柔和线条", "--image", str(image or self.image)]

    def test_dry_run_is_read_only(self):
        styles_before = (self.lib / "styles_200_reorganized.md").read_bytes()
        result = self.run_python(self.importer, *self.args(), "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.lib / "styles_200_reorganized.md").read_bytes(), styles_before)
        self.assertFalse((self.lib / f"images/individual/201-400/{COUNT + 1:03}.webp").exists())

    def test_preflight_rejects_bad_images_and_metadata(self):
        bad = self.base / "bad.png"
        bad.write_text("not an image")
        wide = self.base / "wide.png"
        Image.new("RGB", (64, 32)).save(wide)
        before = snapshot(self.lib)
        for path, message in ((self.base / "missing.png", "不存在"), (bad, "无法读取"), (wide, "正方形")):
            result = self.run_python(self.importer, *self.args(path), "--dry-run")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(message, result.stderr)
            self.assertNotIn("Traceback", result.stderr)
        result = self.run_python(self.importer, *self.args(), "--source-name", "bad|name", "--dry-run")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("竖线", result.stderr)
        self.assertEqual(snapshot(self.lib), before)

    def test_successful_import(self):
        result = self.run_python(self.importer, *self.args())
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((self.lib / "skills/handdraw-style-prompter/references/styles.json").read_text(encoding="utf-8"))
        self.assertEqual(data[-1]["reference"], "测试画风")
        self.assertEqual(len(data), COUNT + 1)
        self.assertTrue(list((self.lib / "images/individual").glob(f"*/{COUNT + 1:03}.webp")))
        self.assertFalse((self.lib / ".style-import.lock").exists())
        check = self.run_python(self.validator)
        self.assertEqual(check.returncode, 0, check.stderr)

    def test_rollback_after_partial_write(self):
        before = snapshot(self.lib)
        code = """
import sys
sys.path.insert(0, sys.argv.pop(1))
import import_manual_style as importer
def fail():
    raise RuntimeError('injected build failure')
importer.rebuild_and_validate = fail
importer.main()
"""
        result = self.run_python("-c", code, self.lib / "scripts", *self.args())
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("已恢复", result.stderr)
        self.assertEqual(snapshot(self.lib), before)

    def test_stale_index_is_auto_repaired(self):
        index = self.lib / "skills/handdraw-style-prompter/references/styles.json"
        data = json.loads(index.read_text(encoding="utf-8"))
        data[0]["generation_name"] = "stale value"
        index.write_text(json.dumps(data), encoding="utf-8")
        before = snapshot(self.lib)
        result = self.run_python(self.validator)
        self.assertEqual(result.returncode, 0)
        self.assertNotIn("stale", result.stderr)
        self.assertNotEqual(snapshot(self.lib), before)

    def test_existing_lock_is_respected(self):
        (self.lib / ".style-import.lock").write_text("another importer")
        before = snapshot(self.lib)
        result = self.run_python(self.importer, *self.args())
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("已有导入进行中", result.stderr)
        self.assertEqual(snapshot(self.lib), before)

    def test_stale_gallery_is_auto_repaired(self):
        gallery = self.lib / "skills/handdraw-style-prompter/gallery/index.html"
        gallery.write_text("stale", encoding="utf-8")
        before = snapshot(self.lib)
        result = self.run_python(self.validator)
        self.assertEqual(result.returncode, 0)
        self.assertNotEqual(snapshot(self.lib), before)
        self.assertNotEqual(gallery.read_text(encoding="utf-8"), "stale")

    def test_invalid_style_and_portable_resolver(self):
        for value in (str(COUNT + 1), "0", "abc"):
            result = self.run_python(ROOT / "scripts/resolve_style.py", "--style", value)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(f"001–{COUNT:03}", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
        result = self.run_python(ROOT / "scripts/resolve_style.py", "--style", str(COUNT))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(Path(json.loads(result.stdout)["reference_path"]).is_file())


if __name__ == "__main__":
    unittest.main()
