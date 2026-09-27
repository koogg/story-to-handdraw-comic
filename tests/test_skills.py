"""Structural regressions that can make packaged skills undiscoverable or unusable."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_skills import validate


class SkillStructureTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="skill metadata ")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.skill = self.root / "SKILL.md"
        self.valid = "---\nname: sample-skill\ndescription: A working sample.\n---\n\nUse the supplied text.\n"

    def test_frontmatter_rejects_overlong_delimiter(self):
        self.skill.write_text(self.valid.replace("\n---\n", "\n--------\n"), encoding="utf-8")
        self.assertTrue(validate(self.root))
        self.skill.write_text(self.valid, encoding="utf-8")
        self.assertEqual(validate(self.root), [])

    def test_local_reference_must_be_packaged(self):
        self.skill.write_text(self.valid + "[Mode](references/mode.md)\n", encoding="utf-8")
        self.assertTrue(validate(self.root))
        refs = self.root / "references"
        refs.mkdir()
        (refs / "mode.md").write_text("Use this mode only when requested.\n", encoding="utf-8")
        self.assertEqual(validate(self.root), [])

    def test_ui_prompt_must_point_to_its_skill(self):
        self.skill.write_text(self.valid, encoding="utf-8")
        agents = self.root / "agents"
        agents.mkdir()
        ui = agents / "openai.yaml"
        ui.write_text('interface:\n  default_prompt: "Use $wrong-skill"\n', encoding="utf-8")
        self.assertTrue(validate(self.root))
        ui.write_text('interface:\n  default_prompt: "Use $sample-skill"\n', encoding="utf-8")
        self.assertEqual(validate(self.root), [])

    def test_discovered_skills_have_unique_names(self):
        self.skill.write_text(self.valid, encoding="utf-8")
        nested = self.root / "nested"
        nested.mkdir()
        child = nested / "SKILL.md"
        child.write_text(self.valid, encoding="utf-8")
        self.assertTrue(any("duplicate skill name" in error for error in validate(self.root)))
        child.write_text(self.valid.replace("sample-skill", "nested-skill"), encoding="utf-8")
        self.assertEqual(validate(self.root), [])

    def test_ui_metadata_reports_invalid_shapes_without_crashing(self):
        self.skill.write_text(self.valid, encoding="utf-8")
        agents = self.root / "agents"
        agents.mkdir()
        ui = agents / "openai.yaml"
        for content in ("[]", "null", "interface: []", "interface:\n  default_prompt: 123"):
            with self.subTest(content=content):
                ui.write_text(content, encoding="utf-8")
                self.assertTrue(any("invalid UI metadata" in error for error in validate(self.root)))

    def test_ui_prompt_rejects_another_skill_with_same_prefix(self):
        self.skill.write_text(self.valid, encoding="utf-8")
        agents = self.root / "agents"
        agents.mkdir()
        (agents / "openai.yaml").write_text(
            'interface:\n  default_prompt: "Use $sample-skill-extra"\n', encoding="utf-8"
        )
        self.assertTrue(validate(self.root))


if __name__ == "__main__":
    unittest.main()
