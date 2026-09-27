---
name: handdraw-style-prompter
description: Resolve a local hand-drawn style number and theme into bilingual image prompts, with model-aware visual traits and reference-image handling. Generate images only on request.
---

# Hand-drawn Style Prompter

Default to prompts only; an explicit request to generate/render/preview authorizes generation. Treat the supplied theme as creative direction, not mandatory display text. Develop visible ideas that express its meaning and respect explicit constraints; create complementary copy in graphic-text mode, and preserve exact wording only when explicitly requested. Article illustration planning belongs to [article-illustration-planner](../article-illustration-planner/SKILL.md); callers needing only style resolution can use the resolver directly.

## Inputs and paths

Require a valid current style number and theme. Accept an optional theme color (`C-01`–`C-30` or color name). If a number is missing/invalid, recommend candidates and ask for a choice; choose automatically when delegated. Do not add a canvas ratio unless supplied or required by the calling workflow.

Commands below run from this skill directory. The package root is `../..`; retain it when installing, because numbered images and the authoritative [catalog](../../styles_200_reorganized.md) live there. [references/styles.json](references/styles.json) and the [gallery](gallery/index.html) are derived assets; [references/colors.json](references/colors.json) and the [color gallery](gallery/colors.html) provide the optional monochrome theme colors. Resolve only requested records instead of reading whole catalogs.

Open the gallery in a browser when requested or when visual selection helps; reuse an already-open gallery. In Codex, use `mcp__codex_app__open_in_codex` with `target.type="browser"`; otherwise offer the resolved gallery link. A known numbered request need not open a browser, and a browser failure never blocks prompting.

## Style activation policy

Run `python -B -X utf8 scripts/resolve_reference.py --model <model-or-unknown> --style <number>`. Use `unknown` when the current image model is not exposed; do not infer it from this skill or a previous image. The resolver reads [model_capabilities.json](references/model_capabilities.json), returns `prompt_traits`, `use_reference_image`, `reference_path`, and `activation_source`, and applies:

- `name_activation=strong`: indexed name and generation style name, with no added traits/reference.
- Otherwise include available positive core traits; require the configured image if text activation is insufficient or unknown.
- Empty traits stay empty. Do not invent traits, use fame/life status as a capability proxy, or treat configured capability as measured accuracy.

Take names from the matching index record. Labels identify catalog entries; they do not authorize copying an existing character or artwork. The resolver selects a numbered grid when available, otherwise a single tile in `images/individual/{bucket}/{number}.webp`. Use its actual returned path rather than reconstructing one.

When an image is required, inspect it and attach it using the native tool's supported method (for example `referenced_image_paths` for local files). A written path alone is not an attachment. If missing or unattachable, deliver text drafts with the limitation; pause rendering that requires it instead of substituting another image. A style flag never removes separately required person inputs.

Apply this isolation instruction only to the input labeled STYLE; translate it faithfully for a Chinese prompt:

> Use the image labeled STYLE only for linework, brushwork, medium, texture, palette, and shape language. Do not copy its subjects, clothing, props, actions, setting, composition, layout, text, or story. The written theme controls content; separately labeled PERSON inputs control only their assigned characters' appearance.

## Prompt modes and output

Default to `pure-image`; retain a mode already chosen in this conversation. Accept 纯图模式 / 图文模式 and CLI `--mode pure-image|graphic-text`.

- **Pure-image:** describe concrete visible content implied by the theme. Include required reference path/upload guidance and STYLE isolation inside both copyable prompts. Respect explicit text requests; otherwise do not invent on-image copy.
- **Graphic-text:** read [references/graphic-text.md](references/graphic-text.md) for theme interpretation, display-copy creation, external reference display, and actual tool-prompt assembly.

Return the selected number/name and two copyable prompts:

- Chinese starts `风格名称：#{number} · {generation_name}。` and includes `参考作者/风格名称：{reference}。`.
- English starts `Style name: #{number} · {generation_name}.` and includes `Reference author/style name: {reference}.`.
- Include resolver-required traits as `核心风格特征：...` / `Core style traits: ...`, without a separate traits section. Preserve their meaning; avoid generic quality claims, negative lists, unsolicited composition rules, or a fixed style anchor.
- When a theme color is selected, add its exact `prompt_zh` / `prompt_en` from `references/colors.json` after the style name. Color cards guide palette only and are not generation reference images.
- For a first pure-image response or a switch into it, note `当前处于纯图模式，可切换为图文模式。`; do not repeat on every turn or mislabel graphic-text mode. Prompt-only output may briefly explain how to use the prompts; actual generation should report actual reference use instead.

## Explicit image generation

Use the available native image tool; honor its current attachment schema and inspect each output for theme, style, required text, and reference-content leakage. If the tool is absent, do not try another service: save the fully expanded Chinese and English prompts in the user's workspace as `handdraw-prompt-01.md` (choose a new name instead of overwriting), return its absolute path, and state the limitation. The saved prompts must contain the resolved style number/name/traits, complete theme or display text, mode, ratio and other supplied constraints, visible content, and required reference-image absolute paths and roles, with no placeholders or dependence on chat history. Say that external tools require the user to upload those reference files; a path alone is not an attachment. Do not use independent image APIs or inspect credentials. Never claim generation, attachment, or visual acceptance without evidence.

Correct substantive defects only, with at most three retries after the first attempt per image, including tool failures and edits; stop earlier for persistent unavailability. Preserve usable output and disclose remaining defects at the limit. Label unviewed output 待人工检查. Save requested outputs in the workspace without overwriting existing files unless authorized. A calling comic workflow supplies its own stricter page/continuity checks and shares this retry budget.

## Utilities

- Prompt draft: `python -B -X utf8 scripts/prompt_style.py --style 18 --color C-01 --theme "秋天的第一杯奶茶" --model unknown`
- After catalog edits: `python -B -X utf8 scripts/build_library.py`
- After color catalog edits: `python -B -X utf8 scripts/build_color_gallery.py`
- Read-only library validation: `python -B -X utf8 scripts/validate_library.py`
- Style additions only: use the [importer](../../.agents/skills/style-library-importer/SKILL.md). Do not run rebuild/import utilities for ordinary prompts.

The CLI makes deterministic drafts that pass the theme as creative direction; conversational prompts should develop the actual visual concept and display copy before delivery. English creative direction can be naturally translated; preserve the intended language of display copy and any explicitly locked wording.
