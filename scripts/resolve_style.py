#!/usr/bin/env python3
"""Portable wrapper around the bundled handraw-style resolver."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_ROOT = SKILL_ROOT / "assets" / "handraw-style"
UPSTREAM_RESOLVER = (
    UPSTREAM_ROOT
    / "skills"
    / "handdraw-style-prompter"
    / "scripts"
    / "resolve_reference.py"
)
STYLE_INDEX = (
    UPSTREAM_ROOT
    / "skills"
    / "handdraw-style-prompter"
    / "references"
    / "styles.json"
)


def resolve(model: str, style: str) -> dict:
    styles = json.loads(STYLE_INDEX.read_text(encoding="utf-8"))
    number = f"{int(style):03}" if style.isascii() and style.isdigit() else ""
    if not any(item["number"] == number for item in styles):
        raise ValueError(f"风格编号 {style!r} 无效；请输入 001–{len(styles):03}")
    if not UPSTREAM_RESOLVER.is_file():
        raise FileNotFoundError(f"Bundled resolver not found: {UPSTREAM_RESOLVER}")

    child_env = os.environ.copy()
    child_env["PYTHONUTF8"] = "1"
    completed = subprocess.run(
        [
            sys.executable,
            str(UPSTREAM_RESOLVER),
            "--model",
            model,
            "--style",
            style,
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=child_env,
    )
    result = json.loads(completed.stdout)
    record = next(item for item in styles if item["number"] == result["style"])
    result["reference_label"] = record["reference"]
    result["generation_name"] = record["generation_name"]
    reference = result.get("reference_path")
    if reference:
        path = Path(reference).resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Resolved style reference is missing: {path}")
        result["reference_path"] = str(path)
    result["style_library_root"] = str(UPSTREAM_ROOT.resolve())
    return result


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        description="Resolve a numbered hand-drawn style and its reference-image policy."
    )
    parser.add_argument("--model", default="unknown")
    parser.add_argument("--style", required=True)
    args = parser.parse_args()
    try:
        result = resolve(args.model, args.style)
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or error.stdout or "子进程未返回详细原因").strip().splitlines()[-1]
        parser.exit(1, f"错误：风格解析失败：{detail}\n")
    except (OSError, ValueError, KeyError, StopIteration) as error:
        parser.exit(1, f"错误：{error}；请检查编号及本地风格库完整性。\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
