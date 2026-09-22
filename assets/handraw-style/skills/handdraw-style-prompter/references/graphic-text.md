# Graphic-text mode

Read only for 图文模式 / `graphic-text`. Preserve the supplied theme verbatim after `主题：` / `Theme:` in both languages; do not translate or expand it into scenes, characters, metaphors, or commentary. Put explicit constraints and any article image-type field outside the theme.

For a standalone opinion, reflection, or aphorism, default to one integrated image with a sentence/paragraph and no storyboard. Do not invent panel sequences. When assembling its prompt, put the no-panels composition requirement outside the preserved theme and before the fixed suffix. An explicit comic request may override this form. This wrapper preserves the input theme for the image model; a calling workflow with already-adapted copy may use its own single-image prompt contract directly.

Append this exact suffix to both copyable prompts, retaining all spaces and punctuation:

```text
【如果主题直白包含画面元素那就按主题出图，文案由你来升华，但是不要直接描述画面。 如果主题比较概念化，那么文案和主题尽量保持一致，如果文案较长由你提炼，由你先设计画面隐喻（人类和非人类都行）再出图   。    文字参与构图，图文一体】
```

If a style reference is required, display the resolved image outside both copyable prompts; when image display is unavailable, provide a separate reference link/path for upload. Neither copyable prompt contains a local path, upload instruction, or reference-isolation block.

For actual generation, attach the required image and prepend the STYLE-only isolation instruction from SKILL.md to the chosen copyable prompt. The copyable prompt (including theme and final suffix) remains an unchanged block; the complete tool prompt therefore has additional reference instructions before it. Do not append anything after the suffix. Keep other inputs labeled separately.
