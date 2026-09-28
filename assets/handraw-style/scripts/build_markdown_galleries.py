#!/usr/bin/env python3
"""Generate bilingual STYLES.md and LAYOUTS.md for GitHub-native visual browsing."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "handdraw-style-prompter"
SOURCE_MD = ROOT / "styles_200_reorganized.md"
LAYOUTS_JSON = SKILL / "references" / "layouts.json"
COLORS_JSON = SKILL / "references" / "colors.json"

def get_sheet_groups():
    h_sheets = sorted([p.name for p in (ROOT / "images").glob("H_*.webp")])
    max_num = 274
    for sheet_name in h_sheets:
        m = re.search(r"H_\d{3}-(\d{3})\.webp", sheet_name)
        if m:
            max_num = max(max_num, int(m.group(1)))
    return [
        ("A", "国际社论漫画与幽默手绘（001–035）", "Editorial & Humorous (001–035)", ["A_001-016.webp", "A_017-032.webp", "A_033-035.webp"]),
        ("B", "国际绘本与叙事型手绘（036–054）", "Picture Book & Narrative (036–054)", ["B_036-048.webp", "B_049-054.webp"]),
        ("C", "现代平面与艺术化人物体系（055–082）", "Graphic & Stylized Figure (055–082)", ["C_055-070.webp", "C_071-082.webp"]),
        ("D", "日本作者与当代插画体系（083–123）", "Japanese Contemporary Illustration (083–123)", ["D_083-098.webp", "D_099-114.webp", "D_115-123.webp"]),
        ("E", "中国作者与当代插画体系（124–154）", "Chinese Contemporary Illustration (124–154)", ["E_124-139.webp", "E_140-154.webp"]),
        ("F", "通用网感、媒介与地域手绘（155–200）", "Internet Culture, Medium & Regional (155–200)", ["F_155-170.webp", "F_171-186.webp", "F_187-200.webp"]),
        ("G", "中国当代插画补充（201–216）", "Contemporary Chinese Illustration Supplement (201–216)", ["G_201-216.webp"]),
        ("H", f"其他精选风格（217–{max_num:03}）", f"Other Curated Styles (217–{max_num:03})", h_sheets),
    ], max_num

LAYOUT_CATEGORIES = [
    ("social-card", "1. 社媒卡（19 种）", "1. Social Cards (19 Layouts)",
     "适合小红书、朋友圈、公众号配图及观点金句卡片。结构包含上下图文、文案主导、双格对照等。",
     "Ideal for Xiaohongshu, Instagram, newsletter hero images, and quote cards. Includes top-bottom split, text-driven cards, two-column contrasts, and sticky notes."),
    ("infographic", "2. 信息图（31 种）", "2. Infographics (31 Layouts)",
     "适合知识科普、对比清单、流程步骤及数据架构展示。结构包含金字塔层级、中心主图标注、多行多列对比等。",
     "Ideal for knowledge sharing, comparison charts, process workflows, and structured data visuals. Includes hierarchy pyramids, central icons, matrices, and multi-column comparison tables."),
    ("comic-storyboard", "3. 漫画分镜（68 种）", "3. Comic Storyboards (68 Layouts)",
     "适合多格叙事、剧情转折、条漫分镜及动态视觉表现。结构包含规则四格、起承转合、大格冲击、对角切割等专业分镜。",
     "Ideal for multi-panel narratives, webtoons, emotional storylines, and cinematic pacing. Includes standard 4-panel grids, dramatic wide-angle focus, diagonal cuts, and manga storyboards."),
]


def build_styles_md() -> None:
    sheet_groups, max_num = get_sheet_groups()
    total_styles_str = f"{max_num:03}"

    # 1. Chinese STYLES.md
    zh_lines = [
        '<p align="center">',
        '  <strong>中文</strong> | <a href="STYLES_en.md">English</a>',
        '</p>',
        '',
        f"# 手绘风格完整图鉴（001–{total_styles_str}）",
        "",
        f"> 这里汇总了本库收录的 **001–{total_styles_str} 种手绘风格**的全部拼图大表。每张拼图包含对应风格编号与画面参考，供在 GitHub 上直接图文浏览选款。详细的英文生图名称与提示词特征对照表见 [styles_200_reorganized.md](styles_200_reorganized.md)。",
        "",
        "## 目录导航",
        "",
    ]
    for letter, title_zh, _, _ in sheet_groups:
        zh_lines.append(f"- [{letter} · {title_zh}](#group-{letter.lower()})")
    zh_lines.extend(["", "---", ""])

    for letter, title_zh, _, sheets in sheet_groups:
        zh_lines.append(f'<a id="group-{letter.lower()}"></a>')
        zh_lines.append(f"## {letter} · {title_zh}")
        zh_lines.append("")
        for sheet in sheets:
            label = sheet.replace(".webp", "").replace("_", " ")
            zh_lines.append(f"![{label}](images/{sheet})")
            zh_lines.append("")
        zh_lines.append("---")
        zh_lines.append("")

    (ROOT / "STYLES.md").write_text("\n".join(zh_lines).strip() + "\n", encoding="utf-8")
    print("Built STYLES.md")

    # 2. English STYLES_en.md
    en_lines = [
        '<p align="center">',
        '  <a href="STYLES.md">中文</a> | <strong>English</strong>',
        '</p>',
        '',
        f"# Hand-drawn Style Visual Sheet (001–{total_styles_str})",
        "",
        f"> Visual contact sheets for all **{total_styles_str} hand-drawn illustration styles** (001–{total_styles_str}). Each sheet displays style numbers and visual references for easy browsing and selection directly on GitHub. For detailed generation names and prompt traits, see [styles_200_reorganized.md](styles_200_reorganized.md).",
        "",
        "## Table of Contents",
        "",
    ]
    for letter, _, title_en, _ in sheet_groups:
        en_lines.append(f"- [{letter} · {title_en}](#group-{letter.lower()})")
    en_lines.extend(["", "---", ""])

    for letter, _, title_en, sheets in sheet_groups:
        en_lines.append(f'<a id="group-{letter.lower()}"></a>')
        en_lines.append(f"## {letter} · {title_en}")
        en_lines.append("")
        for sheet in sheets:
            label = sheet.replace(".webp", "").replace("_", " ")
            en_lines.append(f"![{label}](images/{sheet})")
            en_lines.append("")
        en_lines.append("---")
        en_lines.append("")

    (ROOT / "STYLES_en.md").write_text("\n".join(en_lines).strip() + "\n", encoding="utf-8")
    print("Built STYLES_en.md")


def build_layouts_md() -> None:
    layouts = json.loads(LAYOUTS_JSON.read_text(encoding="utf-8"))
    anchor_map = {
        "social-card": "social-cards",
        "infographic": "infographics",
        "comic-storyboard": "comic-storyboards",
    }
    cols = 3
    counts = {
        "social-card": sum(l["category"] == "social-card" for l in layouts),
        "infographic": sum(l["category"] == "infographic" for l in layouts),
        "comic-storyboard": sum(l["category"] == "comic-storyboard" for l in layouts),
    }
    categories = [
        ("social-card", f"1. 社媒卡（{counts['social-card']} 种）", f"1. Social Cards ({counts['social-card']} Layouts)",
         "适合小红书、朋友圈、公众号配图及观点金句卡片。结构包含上下图文、文案主导、双格对照等。",
         "Ideal for Xiaohongshu, Instagram, newsletter hero images, and quote cards. Includes top-bottom split, text-driven cards, two-column contrasts, and sticky notes."),
        ("infographic", f"2. 信息图（{counts['infographic']} 种）", f"2. Infographics ({counts['infographic']} Layouts)",
         "适合知识科普、对比清单、流程步骤及数据架构展示。结构包含金字塔层级、中心主图标注、多行多列对比等。",
         "Ideal for knowledge sharing, comparison charts, process workflows, and structured data visuals. Includes hierarchy pyramids, central icons, matrices, and multi-column comparison tables."),
        ("comic-storyboard", f"3. 漫画分镜（{counts['comic-storyboard']} 种）", f"3. Comic Storyboards ({counts['comic-storyboard']} Layouts)",
         "适合多格叙事、剧情转折、条漫分镜及动态视觉表现。结构包含规则四格、起承转合、大格冲击、对角切割等专业分镜。",
         "Ideal for multi-panel narratives, webtoons, emotional storylines, and cinematic pacing. Includes standard 4-panel grids, dramatic wide-angle focus, diagonal cuts, and manga storyboards."),
    ]

    # 1. Chinese LAYOUTS.md
    zh_lines = [
        '<p align="center">',
        '  <strong>中文</strong> | <a href="LAYOUTS_en.md">English</a>',
        '</p>',
        '',
        f"# 排版图型完整图鉴（{len(layouts)} 种）",
        "",
        f"> 这里收录了本库全部 **{len(layouts)} 种排版图型**（社媒卡、信息图、漫画分镜）的图片预览与排版提示词。在 AI 生图时直接指定图型编号（如 `SC-001`、`IG-003`、`SB-002`），即可精确控制画面的构图版式与排版层次。",
        "",
        "> 💡 **排版图型架构机制**：",
        "> - **确定性静态排版（纯文本直接拼接型）**：包括 `SC-001`~`SC-020`、`IG` 系列与 `SB` 系列等绝大多数图型，拓扑单一固定，模板直接拼接画风与主题；",
        "> - **高维动态解析型排版（Skill 级动态决策型）**：以 `SC-021`（自适应双拼照片转译）为代表，属于高维视觉语法系统，由 AI 助手充当设计总监先进行构图决策（越界破框/微缩浮岛/记忆图谱等）与背景净化编译，输出单义强约束提示词。",
        "",
        "## 目录导航",
        "",
        f"- [1. 社媒卡（{counts['social-card']} 种）](#social-cards)",
        f"- [2. 信息图（{counts['infographic']} 种）](#infographics)",
        f"- [3. 漫画分镜（{counts['comic-storyboard']} 种）](#comic-storyboards)",
        "",
        "---",
        "",
    ]

    for cat_id, cat_title_zh, _, cat_desc_zh, _ in categories:
        cat_layouts = [l for l in layouts if l["category"] == cat_id]
        anchor = anchor_map.get(cat_id, cat_id)
        zh_lines.append(f'<a id="{anchor}"></a>')
        zh_lines.append(f"## {cat_title_zh}")
        zh_lines.append("")
        zh_lines.append(cat_desc_zh)
        zh_lines.append("")
        zh_lines.append("| 效果预览 | 效果预览 | 效果预览 |")
        zh_lines.append("| :---: | :---: | :---: |")
        for i in range(0, len(cat_layouts), cols):
            chunk = cat_layouts[i:i + cols]
            row_cells = []
            for l in chunk:
                rel_img = str(l["image"]).replace("../../../", "")
                prompt_file = SKILL / "references" / l["prompt_file"]
                prompt_zh = ""
                if prompt_file.exists():
                    content = prompt_file.read_text(encoding="utf-8")
                    if "<!-- zh -->" in content:
                        zh_part = content.split("<!-- en -->")[0].replace("<!-- zh -->", "").strip()
                    else:
                        zh_part = content.strip()
                    prompt_zh = zh_part.replace("|", "&#124;").replace("\n", "<br>")
                name = l["name"]
                cell = f"<img src='{rel_img}' width='260' alt='{l['id']} {name}'><br>**{l['id']}** · {name}"
                if prompt_zh:
                    cell += f"<br><details><summary>查看排版提示词</summary><br>{prompt_zh}</details>"
                row_cells.append(cell)
            while len(row_cells) < cols:
                row_cells.append("")
            zh_lines.append(f"| {' | '.join(row_cells)} |")
        zh_lines.append("")
        zh_lines.append("---")
        zh_lines.append("")

    (ROOT / "LAYOUTS.md").write_text("\n".join(zh_lines).strip() + "\n", encoding="utf-8")
    print("Built LAYOUTS.md")

    # 2. English LAYOUTS_en.md
    en_lines = [
        '<p align="center">',
        '  <a href="LAYOUTS.md">中文</a> | <strong>English</strong>',
        '</p>',
        '',
        f"# Layout Composition Visual Sheet ({len(layouts)} Layouts)",
        "",
        f"> Visual previews and layout prompts for all **{len(layouts)} layout compositions** (Social Cards, Infographics, Comic Storyboards). Specify layout IDs (e.g. `SC-001`, `IG-003`, `SB-002`) during AI image generation to control compositions, text placements, and visual hierarchy.",
        "",
        "> 💡 **Layout Architecture Modes**:",
        "> - **Deterministic Static Layouts (Direct Template Concatenation)**: Covers most layouts (`SC-001`~`SC-020`, `IG` series, `SB` series) with fixed topologies directly assembled with chosen styles;",
        "> - **Dynamic Generative Frameworks (Skill-level Reasoning & Resolution)**: Exemplified by `SC-021` (Adaptive Split Photo-to-Art), functioning as an expressive visual syntax system where the AI assistant acts as Art Director to resolve specific composition mechanics (e.g. Boundary Break, Miniature Diorama, Memory Knolling) and enforce background purging before outputting singular, high-contrast prompts.",
        "",
        "## Table of Contents",
        "",
        f"- [1. Social Cards ({counts['social-card']} Layouts)](#social-cards)",
        f"- [2. Infographics ({counts['infographic']} Layouts)](#infographics)",
        f"- [3. Comic Storyboards ({counts['comic-storyboard']} Layouts)](#comic-storyboards)",
        "",
        "---",
        "",
    ]

    for cat_id, _, cat_title_en, _, cat_desc_en in categories:
        cat_layouts = [l for l in layouts if l["category"] == cat_id]
        anchor = anchor_map.get(cat_id, cat_id)
        en_lines.append(f'<a id="{anchor}"></a>')
        en_lines.append(f"## {cat_title_en}")
        en_lines.append("")
        en_lines.append(cat_desc_en)
        en_lines.append("")
        en_lines.append("| Preview | Preview | Preview |")
        en_lines.append("| :---: | :---: | :---: |")
        for i in range(0, len(cat_layouts), cols):
            chunk = cat_layouts[i:i + cols]
            row_cells = []
            for l in chunk:
                rel_img = str(l["image"]).replace("../../../", "")
                prompt_file = SKILL / "references" / l["prompt_file"]
                prompt_en = ""
                if prompt_file.exists():
                    content = prompt_file.read_text(encoding="utf-8")
                    if "<!-- en -->" in content:
                        en_part = content.split("<!-- en -->")[1].strip()
                    else:
                        en_part = ""
                    prompt_en = en_part.replace("|", "&#124;").replace("\n", "<br>")
                name_en = l.get("name_en") or l.get("name", "")
                cell = f"<img src='{rel_img}' width='260' alt='{l['id']} {name_en}'><br>**{l['id']}** · {name_en}"
                if prompt_en:
                    cell += f"<br><details><summary>View Layout Prompt</summary><br>{prompt_en}</details>"
                row_cells.append(cell)
            while len(row_cells) < cols:
                row_cells.append("")
            en_lines.append(f"| {' | '.join(row_cells)} |")
        en_lines.append("")
        en_lines.append("---")
        en_lines.append("")

    (ROOT / "LAYOUTS_en.md").write_text("\n".join(en_lines).strip() + "\n", encoding="utf-8")
    print("Built LAYOUTS_en.md")


def build_colors_md() -> None:
    if not COLORS_JSON.exists():
        return
    colors = json.loads(COLORS_JSON.read_text(encoding="utf-8"))
    sheets = [
        (1, "经典蓝系（6 种）", "Classic Blue (6 Colors)", "沉静理性、跨越时光的纯粹蓝调，适合科技、思考、静夜与海洋题材。", "Calm, rational, and timeless pure blue tones, ideal for tech, reflection, nocturnal, and ocean themes."),
        (2, "清新绿系（6 种）", "Fresh Green (6 Colors)", "自然治愈、盛夏微风的清新绿意，适合生活方式、健康、植物与轻食题材。", "Natural, healing, and breezy green tones, ideal for lifestyle, wellness, flora, and food themes."),
        (3, "古典红绿（6 种）", "Classic Red & Vintage (6 Colors)", "历史沉淀、浓郁厚重的东方与古典艺术色，适合节庆、传统文化、复古与叙事题材。", "Historical and rich classical tones, ideal for festivals, heritage, vintage, and narrative themes."),
        (4, "浪漫粉紫（6 种）", "Romantic Pink & Purple (6 Colors)", "温柔优雅、热烈浪漫的情感色系，适合女性生活、诗意、美妆与自我表达题材。", "Gentle, elegant, and romantic palettes, ideal for feminine lifestyle, poetry, cosmetics, and self-expression."),
        (5, "暖阳大地（6 种）", "Warm Sun & Earth (6 Colors)", "温暖明媚、沉静质朴的大地色系，适合晨光、咖啡、穿搭、秋收与温馨日常题材。", "Warm, sunny, and grounded earth tones, ideal for morning light, coffee, autumn, and cozy daily life."),
        (6, "中性色系（6 种）", "Classic Neutral Tones (6 Colors)", "克制沉静、现代高级的黑白灰与中性色调，适合极简生活、建筑空间、沉思书房与质朴日常题材。", "Restrained, tranquil, and modern neutral tones across grey, black, cream, and taupe, ideal for minimalist lifestyle, architectural spaces, reflective studies, and serene daily life."),
    ]
    cols = 3

    # 1. Chinese COLORS.md
    zh_lines = [
        '<p align="center">',
        '  <strong>中文</strong> | <a href="COLORS_en.md">English</a>',
        '</p>',
        '',
        f"# 经典单色主题色完整图鉴（{len(colors)} 种）",
        "",
        f"> 这里收录了本库精选的 **{len(colors)} 种经典单色主题色**（涵盖经典蓝系、清新绿系、古典红绿、浪漫粉紫、暖阳大地、中性色系）。在 AI 生图时直接指定色彩编号（如 `C-01`、`C-10`、`C-15`、`C-31`）或色彩名称（如“克莱因蓝”、“鼠尾草绿”、“佩恩灰”），即可精确控制画面的主色调与情绪氛围。",
        "",
        "## 目录导航",
        "",
    ]
    for s_num, title_zh, _, _, _ in sheets:
        zh_lines.append(f"- [{s_num}. {title_zh}](#sheet-{s_num:02d})")
    zh_lines.extend(["", "---", ""])

    for s_num, title_zh, _, desc_zh, _ in sheets:
        s_colors = [c for c in colors if c["sheet"] == s_num]
        zh_lines.append(f'<a id="sheet-{s_num:02d}"></a>')
        zh_lines.append(f"## {s_num}. {title_zh}")
        zh_lines.append("")
        zh_lines.append(desc_zh)
        zh_lines.append("")
        zh_lines.append(f"![经典单色主题色库 {s_num:02d}](images/colors/sheet_{s_num:02d}.webp)")
        zh_lines.append("")
        zh_lines.append("| 效果预览 | 效果预览 | 效果预览 |")
        zh_lines.append("| :---: | :---: | :---: |")
        for i in range(0, len(s_colors), cols):
            chunk = s_colors[i:i + cols]
            row_cells = []
            for c in chunk:
                rel_img = str(c["image"]).replace("../../../", "")
                cell = f"<img src='{rel_img}' width='220' alt='{c['id']} {c['name_zh']}'><br>**{c['id']}** · {c['name_zh']}<br><small>{c['quote_zh']}</small><br><details><summary>查看色彩提示词</summary><br>`{c['prompt_zh']}`</details>"
                row_cells.append(cell)
            while len(row_cells) < cols:
                row_cells.append("")
            zh_lines.append(f"| {' | '.join(row_cells)} |")
        zh_lines.append("")
        zh_lines.append("---")
        zh_lines.append("")

    (ROOT / "COLORS.md").write_text("\n".join(zh_lines).strip() + "\n", encoding="utf-8")
    print("Built COLORS.md")

    # 2. English COLORS_en.md
    en_lines = [
        '<p align="center">',
        '  <a href="COLORS.md">中文</a> | <strong>English</strong>',
        '</p>',
        '',
        f"# Classic Monochrome Colors Visual Sheet ({len(colors)} Colors)",
        "",
        f"> Visual previews and color prompts for all **{len(colors)} curated monochrome theme colors** (Classic Blue, Fresh Green, Vintage Red & Classical, Romantic Pink & Purple, Warm Sun & Earth, Classic Neutral Tones). Specify color IDs (e.g. `C-01`, `C-10`, `C-15`, `C-31`) or color names (e.g. 'Klein Blue', 'Sage Green', 'Payne\\'s Grey') during AI image generation to precisely control color palettes and visual moods.",
        "",
        "## Table of Contents",
        "",
    ]
    for s_num, _, title_en, _, _ in sheets:
        en_lines.append(f"- [{s_num}. {title_en}](#sheet-{s_num:02d})")
    en_lines.extend(["", "---", ""])

    for s_num, _, title_en, _, desc_en in sheets:
        s_colors = [c for c in colors if c["sheet"] == s_num]
        en_lines.append(f'<a id="sheet-{s_num:02d}"></a>')
        en_lines.append(f"## {s_num}. {title_en}")
        en_lines.append("")
        en_lines.append(desc_en)
        en_lines.append("")
        en_lines.append(f"![Classic Monochrome Library {s_num:02d}](images/colors/sheet_{s_num:02d}.webp)")
        en_lines.append("")
        en_lines.append("| Visual Preview | Visual Preview | Visual Preview |")
        en_lines.append("| :---: | :---: | :---: |")
        for i in range(0, len(s_colors), cols):
            chunk = s_colors[i:i + cols]
            row_cells = []
            for c in chunk:
                rel_img = str(c["image"]).replace("../../../", "")
                cell = f"<img src='{rel_img}' width='220' alt='{c['id']} {c['name_en']}'><br>**{c['id']}** · {c['name_en']}<br><small>{c['quote_en']}</small><br><details><summary>View Color Prompt</summary><br>`{c['prompt_en']}`</details>"
                row_cells.append(cell)
            while len(row_cells) < cols:
                row_cells.append("")
            en_lines.append(f"| {' | '.join(row_cells)} |")
        en_lines.append("")
        en_lines.append("---")
        en_lines.append("")

    (ROOT / "COLORS_en.md").write_text("\n".join(en_lines).strip() + "\n", encoding="utf-8")
    print("Built COLORS_en.md")


def main() -> None:
    build_styles_md()
    build_layouts_md()
    build_colors_md()


if __name__ == "__main__":
    main()
