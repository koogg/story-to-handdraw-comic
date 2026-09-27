"""Style IDs must not collide with layout/color IDs; resolution stays portable."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from resolve_style import resolve


class ResolverTests(unittest.TestCase):
    def test_explicit_style_notation_resolves_to_the_same_record(self):
        for value in ("16", "016", "#016", " 画风：#016 ", "风格编号 16"):
            with self.subTest(value=value):
                result = resolve("unknown", value)
                self.assertEqual(result["style"], "016")
                self.assertTrue(result["generation_name"])
                self.assertTrue(result["use_reference_image"])
                self.assertTrue(Path(result["reference_path"]).is_absolute())
                self.assertTrue(Path(result["reference_path"]).is_file())

    def test_other_id_namespaces_and_malformed_numbers_are_rejected(self):
        for value in ("SC-016", "IG-016", "SB-016", "C-16", "-16", "16.5",
                      "016/017", "016–020", "abc16", "0", "999", "", "自动选择"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                resolve("unknown", value)

    def test_unknown_model_uses_reference_and_known_policy_does_not(self):
        fallback = resolve("unlisted-test-model", "277")
        self.assertTrue(fallback["use_reference_image"])
        self.assertTrue(Path(fallback["reference_path"]).is_file())
        # This verifies local configured policy, not model quality or availability.
        configured = resolve("gpt-image-2", "277")
        self.assertFalse(configured["use_reference_image"])
        self.assertIsNone(configured["reference_path"])

    def test_cli_is_independent_of_working_directory(self):
        with tempfile.TemporaryDirectory(prefix="style resolver cwd ") as folder:
            result = subprocess.run(
                [sys.executable, "-B", "-X", "utf8", str(ROOT / "scripts/resolve_style.py"),
                 "--style", "#016"], cwd=folder, capture_output=True, text=True,
                encoding="utf-8",
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(Path(json.loads(result.stdout)["reference_path"]).is_file())


if __name__ == "__main__":
    unittest.main()
