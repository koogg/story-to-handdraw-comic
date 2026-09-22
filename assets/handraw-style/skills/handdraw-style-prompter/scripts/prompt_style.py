#!/usr/bin/env python3
"""Create a deterministic bilingual prompt draft from a validated style number."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from resolve_reference import resolve

SKILL = Path(__file__).resolve().parents[1]

REFERENCE_ISOLATION_ZH = (
    "所附图片仅用于参考画风。只提取参考图的风格特征，例如线条、笔触、媒介、材质、色彩倾向和整体视觉语言；"
    "不要使用、复制或延续参考图中的任何主体、人物、动物、服装、道具、动作、姿态、场景、背景、构图、布局、文字或故事。"
    "最终画面内容完全以用户提供的主题为准。"
)
REFERENCE_ISOLATION_EN = (
    "Use the attached image only as a style reference. Extract only its stylistic qualities, such as linework, brushwork, medium, "
    "material texture, color tendencies, and overall visual language. Do not use, copy, or carry over any subject, person, animal, "
    "clothing, prop, action, pose, setting, background, composition, layout, text, or story from the reference image. "
    "The user's written theme is the sole source for the image content."
)
GRAPHIC_TEXT_SUFFIX = "【如果主题直白包含画面元素那就按主题出图，文案由你来升华，但是不要直接描述画面。 如果主题比较概念化，那么文案和主题尽量保持一致，如果文案较长由你提炼，由你先设计画面隐喻（人类和非人类都行）再出图   。    文字参与构图，图文一体】"


def resolve_color(query: str) -> dict[str, str]:
    colors = json.loads((SKILL / "references" / "colors.json").read_text(encoding="utf-8"))
    value = query.strip().lower()
    number = value.removeprefix("c-").lstrip("0") if value.startswith("c-") else ""
    for color in colors:
        if (value == color["id"].lower() or (number and number == color["id"].removeprefix("C-").lstrip("0"))
                or value in color["name_zh"].lower() or value in color["name_en"].lower()):
            return color
    if value.startswith("c-"):
        raise ValueError(f"Unknown color ID: {query}. Use C-01 to C-30 or a color name.")
    return {"id": "", "name_zh": query.strip(), "name_en": query.strip(),
            "prompt_zh": f"主题色：{query.strip()}。", "prompt_en": f"Theme color: {query.strip()}."}


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    styles = json.loads((SKILL / "references" / "styles.json").read_text(encoding="utf-8"))
    max_num = len(styles)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--style", required=True, help=f"Style number from 001 to {max_num:03}")
    parser.add_argument("--color", help="Optional color ID (C-01 to C-30) or color name.")
    parser.add_argument("--theme", required=True)
    parser.add_argument("--ratio")
    parser.add_argument("--subject")
    parser.add_argument("--text")
    parser.add_argument("--model", default="unknown", help="Known image model; unknown uses reference fallback.")
    parser.add_argument("--mode", choices=("pure-image", "graphic-text"), default="pure-image")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    number = f"{int(args.style):03}" if args.style.isascii() and args.style.isdigit() else ""
    selected = next((item for item in styles if item["number"] == number), None)
    if selected is None:
        parser.error(f"Style must be a number from 001 to {max_num:03}.")
    try:
        color = resolve_color(args.color) if args.color else None
    except (OSError, ValueError, KeyError) as error:
        parser.error(f"Color resolution failed: {error}")
    try:
        decision = resolve(args.model, number)
    except (OSError, ValueError, KeyError) as error:
        parser.error(f"Style resolution failed: {error}")
    traits = decision["prompt_traits"]
    zh = [f"风格名称：#{number} · {selected['generation_name']}。"]
    en = [f"Style name: #{number} · {selected['generation_name']}."]
    if color:
        zh.append(color["prompt_zh"])
        en.append(color["prompt_en"])
    zh.extend((f"主题：{args.theme}。", f"参考作者/风格名称：{selected['reference']}。"))
    en.extend((f"Theme: {args.theme}.", f"Reference author/style name: {selected['reference']}."))
    if traits:
        zh.append(f"核心风格特征：{traits}。")
        en.append(f"Core style traits: {traits}.")
    for value, label_zh, label_en in ((args.ratio, "画幅", "Aspect ratio"),
                                      (args.subject, "主体限制", "Subject constraints"),
                                      (args.text, "文字要求", "Text requirement")):
        if value:
            zh.append(f"{label_zh}：{value}。")
            en.append(f"{label_en}: {value}.")
    reference = decision.get("reference_path") if decision["use_reference_image"] else None
    if args.mode == "pure-image" and reference:
        zh.append(f"参考图：请上传本地参考图 {reference}。{REFERENCE_ISOLATION_ZH}")
        en.append(f"Reference image: upload local reference image {reference}. {REFERENCE_ISOLATION_EN}")
    if args.mode == "graphic-text":
        zh.append(GRAPHIC_TEXT_SUFFIX)
        en.append(GRAPHIC_TEXT_SUFFIX)
    result = {"style": number, "generation_name": selected["generation_name"],
              "color": color["id"] if color else None,
              "mode": args.mode, "model": args.model,
              "activation_source": decision["activation_source"],
              "use_reference_image": decision["use_reference_image"],
              "reference_path": reference,
              "reference_available": bool(reference and Path(reference).is_file()),
              "chinese_prompt": "".join(zh), "english_prompt": " ".join(en)}
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"Selected style: #{number} · {selected['generation_name']}")
    print("\n中文提示词：\n" + result["chinese_prompt"])
    print("\nEnglish prompt:\n" + result["english_prompt"])
    print("\nPaste either prompt into an image AI; this script does not generate an image.")
    if reference and args.mode == "graphic-text":
        print(f"Reference image (outside copyable prompts): {reference}")
    if reference and not result["reference_available"]:
        print("Required reference is missing; prompts are drafts awaiting that asset.")
    if args.mode == "pure-image":
        print("当前处于纯图模式，可切换为图文模式。")


if __name__ == "__main__":
    main()
