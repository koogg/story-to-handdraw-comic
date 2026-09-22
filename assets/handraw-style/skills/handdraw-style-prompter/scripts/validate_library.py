#!/usr/bin/env python3
"""Validate source parsing, generated assets, and the deterministic prompt contract."""
from __future__ import annotations

import json
import subprocess
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from build_library import parse_styles, contact_sheets, gallery_html

ROOT = Path(__file__).resolve().parents[3]
from resolve_reference import resolve
try:
    from contact_sheet_registry import CAPACITY, STATE_FILE, parse_sheet, sheet_path
except ModuleNotFoundError as error:
    raise SystemExit(f"FAIL: 缺少校验依赖 {error.name}；请安装 Pillow 并确认脚本文件完整。") from None
from style_asset_paths import bucket_name, grid_path, single_path

SKILL = Path(__file__).resolve().parents[1]
GRAPHIC_TEXT_SUFFIX = "【如果主题直白包含画面元素那就按主题出图，文案由你来升华，但是不要直接描述画面。 如果主题比较概念化，那么文案和主题尽量保持一致，如果文案较长由你提炼，由你先设计画面隐喻（人类和非人类都行）再出图   。    文字参与构图，图文一体】"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    python = [sys.executable, "-B", "-X", "utf8"]
    styles = json.loads((SKILL / "references" / "styles.json").read_text(encoding="utf-8"))
    if styles != parse_styles():
        fail("styles.json is stale; run skills/handdraw-style-prompter/scripts/build_library.py from the library root")
    gallery_path = SKILL / "gallery" / "index.html"
    if gallery_path.read_text(encoding="utf-8") != gallery_html(styles, contact_sheets()):
        fail("gallery is stale; run skills/handdraw-style-prompter/scripts/build_library.py from the library root")
    manifest = (ROOT / "MANIFEST.md").read_text(encoding="utf-8")
    sheets = contact_sheets()
    for value in (f"拼图总数：{len(sheets)} 张", f"单图总数：{len(styles)} 张", f"风格编号覆盖：001–{len(styles):03}"):
        if value not in manifest:
            fail(f"MANIFEST.md is stale: expected {value}")
    for sheet in sheets:
        if f"`{Path(sheet['path']).name}`" not in manifest:
            fail(f"MANIFEST.md is missing {sheet['path']}")
    model_capabilities = json.loads((SKILL / "references" / "model_capabilities.json").read_text(encoding="utf-8"))
    total_styles = len(styles)
    max_num = f"{total_styles:03}"
    expected = [f"{n:03}" for n in range(1, total_styles + 1)]
    if [item["number"] for item in styles] != expected:
        fail(f"style numbering is not continuous 001–{max_num}")
    eighteen = styles[17]
    if eighteen["generation_name"] != "Minimal Deadpan Dialogue Cartoon":
        fail("018 maps to the wrong generation name")
    if model_capabilities.get("default", {}).get("name_activation") != "unknown":
        fail("the model capability default must be unknown")
    if model_capabilities.get("default", {}).get("use_reference_image") is not True:
        fail("unknown model capability must use the image fallback")
    for model, profile in model_capabilities.get("models", {}).items():
        if profile.get("name_activation") not in {None, "strong", "weak", "none", "unknown"}:
            fail(f"invalid model capability for {model}")
        if profile.get("traits_activation") not in {None, "strong", "weak", "none", "unknown"}:
            fail(f"invalid traits capability for {model}")
        for number, entry in profile.get("styles", {}).items():
            if number not in expected:
                fail(f"model capability references invalid style {number}")
            if entry.get("name_activation") not in {"strong", "weak", "none", "unknown"}:
                fail(f"invalid style capability for {model}/{number}")
            if entry.get("traits_activation") not in {None, "strong", "weak", "none", "unknown"}:
                fail(f"invalid traits style capability for {model}/{number}")
    unknown = resolve("unregistered-model", "001")
    if unknown["name_activation"] != "unknown" or not unknown["use_reference_image"]:
        fail("unknown model must use reference image")
    if resolve("gpt-image-2", "001")["use_reference_image"] is not False:
        fail("gpt-image-2 style 001 should use name activation")
    manual_name = resolve("gpt-image-2", "262")
    if manual_name["activation_source"] != "name+style" or manual_name["use_reference_image"] or manual_name["prompt_traits"]:
        fail("text-defined name-only style must use name activation without an image or traits")
    if resolve("gpt-image-2", "155")["activation_source"] != "name+style+traits" or resolve("gpt-image-2", "155")["use_reference_image"] is not False:
        fail("gpt-image-2 style with positive traits should use name+traits activation")
    synthetic = {"default": model_capabilities["default"], "models": {
        "test-model": {"name_activation": "unknown", "traits_activation": "strong", "styles": {
            "201": {"name_activation": "none"},
            "002": {"name_activation": "strong"},
            "022": {"name_activation": "none", "traits_activation": "none"},
        }},
    }}
    if resolve("test-model", "201", synthetic)["use_reference_image"] is not True:
        fail("empty traits or insufficient capability must use reference image")
    if resolve("test-model", "002", synthetic)["use_reference_image"] is not False:
        fail("strong capability must not use reference image")
    reference_with_traits = resolve("test-model", "022", synthetic)
    if (reference_with_traits["activation_source"] != "name+style+traits+reference-image"
            or not reference_with_traits["use_reference_image"]
            or not reference_with_traits["prompt_traits"]):
        fail("reference fallback with traits must preserve traits and require the image")
    traits_case = resolve("gpt-image-2", "022")
    if traits_case["activation_source"] != "name+style+traits" or not traits_case["prompt_traits"] or "避免" in traits_case["prompt_traits"]:
        fail("gpt-image-2 traits activation did not produce filtered positive traits")
    if resolve("gpt-image-2", "201")["use_reference_image"] is not True:
        fail("empty-trait style must use reference image")
    if bucket_name(1) != "001-200" or bucket_name(217) != "201-400" or bucket_name(401) != "401-600":
        fail("style asset bucket calculation is incorrect")
    reference_217 = resolve("gpt-image-2", "217")
    if (reference_217["activation_source"] != "name+style+traits+reference-image"
            or not reference_217["prompt_traits"]
            or reference_217["reference_path"] != str(grid_path(217))):
        fail("style 217 must preserve traits and use its four-panel grid reference")
    if not grid_path(217).exists():
        fail("style 217 four-panel grid is missing")
    for number in range(262, 269):
        reference = resolve("unregistered-model", f"{number:03}")
        if grid_path(number).exists() or reference["reference_path"] != str(single_path(number)):
            fail(f"single-image style {number:03} must not retain a redundant grid reference")
    if any(item["traits"] for item in styles[200:216] if item["number"] != "205"):
        fail("201–216 core visual traits may only be populated for style 205")
    style_205 = next(item for item in styles if item["number"] == "205")
    if not style_205["traits"] or "坚持伟大式轻幽默Q版漫画" not in style_205["traits"]:
        fail("style 205 core visual traits are missing")
    if any(item["group"] != "G 附件新增 / 中国当代插画补充" for item in styles[200:216]):
        fail("201–216 must remain in group G")
    if any(item["group"] != "H 其他" for item in styles[216:]):
        fail("217+ styles must belong to group H")
    individual = ROOT / "images" / "individual"
    expected_individual = [single_path(number) for number in range(1, total_styles + 1)]
    if not all(path.exists() for path in expected_individual):
        fail(f"numbered asset buckets must cover exactly 001.webp–{max_num}.webp")
    if list(individual.glob("[0-9][0-9][0-9].webp")) or list(individual.glob("[0-9][0-9][0-9]_grid.webp")):
        fail("flat individual assets must be migrated into numbered buckets")
    imported_sheets = []
    for path in (ROOT / "images").glob("[GH]_*.webp"):
        parsed = parse_sheet(path)
        if parsed:
            start, end = parsed
            if path.name.startswith("G_") and (start, end) != (201, 216):
                fail("G contact sheets may only cover 201–216")
            if path.name.startswith("H_") and start < 217:
                fail("H contact sheets must start at 217 or later")
            imported_sheets.append((*parsed, path))
    imported_sheets.sort()
    expected_imported_numbers = list(range(201, total_styles + 1))
    listed_imported_numbers = [number for start, end, _ in imported_sheets for number in range(start, end + 1)]
    if listed_imported_numbers != expected_imported_numbers:
        fail("Imported contact sheets must cover each 201+ style exactly once")
    if any(end - start + 1 != CAPACITY for start, end, _ in imported_sheets[:-1]):
        fail("only the final Imported contact sheet may be incomplete")
    if not STATE_FILE.exists():
        fail("Imported contact-sheet state is missing")
    sheet_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    last_start, last_end, last_path = imported_sheets[-1]
    last_filled = last_end - last_start + 1
    expected_next_cell = last_filled + 1 if last_filled < CAPACITY else 1
    if (sheet_state.get("capacity") != CAPACITY or sheet_state.get("active_start") != last_start
            or sheet_state.get("filled") != last_filled or sheet_state.get("next_cell") != expected_next_cell
            or last_path != sheet_path(last_start, last_end)):
        fail("Imported contact-sheet state does not match the active sheet")
    gallery = (SKILL / "gallery" / "index.html").read_text(encoding="utf-8")
    for _, _, path in imported_sheets:
        if path.name not in gallery:
            fail(f"gallery is missing contact sheet {path.name}")
    if 'data-number="217" data-group="H"' not in gallery or 'data-number="262" data-group="H"' not in gallery:
        fail("gallery does not classify 217+ style cards as H")
    if 'data-label="H · #217–#232"' not in gallery:
        fail("gallery does not classify the first H contact sheet as H")
    if "A_001-016.webp" not in gallery or "F_187-200.webp" not in gallery or "#018" not in gallery:
        fail("gallery does not cover the expected sheets and style 018")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for _, _, path in imported_sheets:
        if f"images/{path.name}" not in readme:
            fail(f"README does not reference contact sheet {path.name}")
    if "### G · 附件新增 / 中国当代插画补充（201–216）" not in readme or f"### H · 其他（217–{max_num}）" not in readme:
        fail("README does not separate G and H contact-sheet groups")
    if f"风格索引（{total_styles}）" not in gallery or f"输入 001–{max_num}" not in gallery:
        fail("gallery count or range is stale")
    # Check observable prompt/reference behavior, not headings or prose wording.
    def draft(style, theme="秋天的第一杯奶茶", *extra):
        run = subprocess.run(
            python + [str(SKILL / "scripts/prompt_style.py"), "--style", str(style),
                      "--theme", theme, "--format", "json", *extra],
            capture_output=True, text=True, encoding="utf-8", check=True)
        return json.loads(run.stdout)

    default = draft(18)
    known = draft(18, "秋天的第一杯奶茶", "--model", "gpt-image-2")
    if not default["use_reference_image"] or not default["reference_available"]:
        fail("unspecified model must return a usable reference fallback")
    if known["use_reference_image"] or known["reference_path"]:
        fail("known strong-name style must not require a reference")
    for key, prefix, label in (("chinese_prompt", "风格名称：#018", "参考作者/风格名称："),
                               ("english_prompt", "Style name: #018", "Reference author/style name:")):
        prompt = default[key]
        if not prompt.startswith(prefix) or label not in prompt or "秋天的第一杯奶茶" not in prompt:
            fail("bilingual prompt is missing selected style, catalog label, or theme")
        if default["reference_path"] not in prompt:
            fail("pure-image prompt is missing required reference upload path")
    if "所附图片仅用于参考画风" not in default["chinese_prompt"] or "Use the attached image only as a style reference" not in default["english_prompt"]:
        fail("pure-image reference is missing content-isolation guidance")

    theme = "世界就是个草台班子\n原文  空格与标点！"
    graphic = draft(217, theme, "--mode", "graphic-text")
    if not graphic["use_reference_image"] or graphic["reference_path"] != str(grid_path(217)) or not graphic["reference_available"]:
        fail("graphic-text result must expose the required grid outside its prompts")
    for key in ("chinese_prompt", "english_prompt"):
        prompt = graphic[key]
        if prompt.count(theme) != 1 or not prompt.endswith(GRAPHIC_TEXT_SUFFIX) or prompt.count(GRAPHIC_TEXT_SUFFIX) != 1:
            fail("graphic-text must preserve theme and exact final suffix in both prompts")
        if graphic["reference_path"] in prompt or "所附图片仅用于参考画风" in prompt or "Use the attached image only as a style reference" in prompt:
            fail("graphic-text copyable prompt leaked reference instructions")
    graphic_text = subprocess.run(
        python + [str(SKILL / "scripts/prompt_style.py"), "--style", "217", "--theme", "动画人物", "--mode", "graphic-text"],
        capture_output=True, text=True, encoding="utf-8", check=True)
    if "当前处于纯图模式" in graphic_text.stdout or str(grid_path(217)) not in graphic_text.stdout.split("Reference image (outside copyable prompts):", 1)[-1]:
        fail("graphic-text CLI must show its external reference without reporting pure-image mode")

    # The byte-exact suffix is a maintained asset shared by the CLI and instructions.
    mode_guide = (SKILL / "references/graphic-text.md").read_text(encoding="utf-8")
    if GRAPHIC_TEXT_SUFFIX not in mode_guide:
        fail("graphic-text reference lost the exact suffix required by the prompt contract")
    for number in (217, 267):
        result = draft(number, "动画人物", "--model", "gpt-image-2")
        if "核心风格特征：" not in result["chinese_prompt"] or "Core style traits:" not in result["english_prompt"]:
            fail(f"style {number} must retain positive traits")
        if result["use_reference_image"] != (number == 217):
            fail(f"style {number} uses the wrong reference activation path")
    blank = draft(214)
    if not blank["use_reference_image"] or "核心风格特征：" in blank["chinese_prompt"]:
        fail("blank traits must stay empty while preserving reference fallback")
    for value in (str(total_styles + 1), "0", "abc", "-1"):
        invalid = subprocess.run(
            python + [str(SKILL / "scripts/prompt_style.py"), "--style", value, "--theme", "x"],
            capture_output=True, text=True, encoding="utf-8")
        if invalid.returncode == 0 or f"001 to {max_num}" not in invalid.stderr or "Traceback" in invalid.stderr:
            fail("invalid style must fail clearly without a traceback")
    print(f"PASS: {total_styles} styles, gallery coverage, prompt contract, and invalid-number guard.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, StopIteration, subprocess.CalledProcessError) as error:
        raise SystemExit(f"FAIL: 风格库校验失败：{error}。请检查文件完整性；校验不会自动修改文件。") from None
