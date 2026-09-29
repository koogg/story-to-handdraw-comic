#!/usr/bin/env python3
"""Read-only validation of packaged skill metadata and local Markdown links."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

try:
    import yaml
except ModuleNotFoundError:
    raise SystemExit("Missing PyYAML; install it in the validation environment.") from None

ROOT = Path(__file__).resolve().parents[1]


def validate(root: Path) -> list[str]:
    errors = []
    names: dict[str, str] = {}
    skills = sorted(root.rglob("SKILL.md"))
    if not skills:
        return ["No skills found"]
    for path in skills:
        label = str(path.relative_to(root))
        content = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", content, re.S)
        if not match:
            errors.append(f"{label}: YAML must use exact --- delimiters")
            continue
        try:
            metadata = yaml.safe_load(match[1])
        except yaml.YAMLError as error:
            errors.append(f"{label}: {error}")
            continue
        if not isinstance(metadata, dict):
            errors.append(f"{label}: metadata must be a mapping")
            continue
        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if not isinstance(name, str) or len(name) > 64:
            errors.append(f"{label}: invalid skill name")
        else:
            names[name] = label
        if not isinstance(description, str) or not description.strip() or len(description) > 1024:
            errors.append(f"{label}: invalid description")
        ui_path = path.parent / "agents/openai.yaml"
        if ui_path.exists():
            try:
                ui = yaml.safe_load(ui_path.read_text(encoding="utf-8"))
                if not isinstance(ui, dict):
                    raise ValueError("UI metadata must be a mapping")
                interface = ui.get("interface", {})
                if not isinstance(interface, dict):
                    raise ValueError("interface must be a mapping")
                prompt = interface.get("default_prompt", "")
                if not isinstance(prompt, str):
                    raise ValueError("default_prompt must be a string")
                if prompt and not re.search(r"\$" + re.escape(str(name)) + r"(?![a-z0-9-])", prompt):
                    errors.append(f"{ui_path.relative_to(root)}: default prompt names a different skill")
            except (yaml.YAMLError, ValueError) as error:
                errors.append(f"{ui_path.relative_to(root)}: invalid UI metadata: {error}")

    for path in root.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        # Strip code blocks to avoid checking illustrative/example links
        stripped_content = re.sub(r"```[\s\S]*?```", "", content)
        for target in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", stripped_content):
            target = target.strip().strip("<>")
            if target.startswith("#") or re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", target):
                continue
            target = unquote(target.split("#", 1)[0])
            if target and not (path.parent / target).exists():
                errors.append(f"{path.relative_to(root)}: missing link target {target}")
    return errors


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    failures = validate(ROOT)
    if failures:
        raise SystemExit("\n".join(f"FAIL: {error}" for error in failures))
    print(f"PASS: {len(list(ROOT.rglob('SKILL.md')))} skill files, metadata, and local Markdown links.")
