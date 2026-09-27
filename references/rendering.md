# Rendering and acceptance

Read when generating, repairing, or delivering prompts for comic pages, single text-and-image illustrations, posters, social cards, or infographics. Each page or standalone image has its own attempt budget. Use the available native image-generation tool and its current attachment rules. Do not call independent image APIs or inspect credential/configuration files.

## Prompt-model delivery

Use the main skill's delivery-intent rules. **提示词模式 / 仅提示词**, or a prompt request without a request for images, delivers a file without image generation. An explicit request for both images and prompts delivers both; the word “提示词” alone must not suppress requested generation. A later “按这个生成” switches an accepted prompt plan into rendering without restarting creative selection.

Finish adaptation, style resolution, layout/storyboard design, and person/reference mapping, then save all final prompts in one Markdown file in the user's workspace. Use `graphic-prompts.md`, `poster-prompts.md`, `social-card-prompts.md`, `infographic-prompts.md`, or `comic-page-prompts.md` as appropriate, choosing a new name rather than overwriting an existing file. For combined image-and-prompt delivery, update the new file with each page's final attempted prompt and its actual acceptance status.

The file must be directly usable in the ChatGPT web interface outside this conversation: no `{placeholders}`, omitted decisions, chat-history dependencies, or instructions to “use the plan above.” Start with a short usage note, then give one separately copyable fenced prompt per requested image/page. Every prompt must repeat the shared context it needs, including asset type, concrete ratio and **one image per call** (plus page N of TOTAL where applicable); resolved style name and only resolver-required positive traits; complete adapted display text with LOCKED spans, speaker, and placement as applicable; tone and core meaning; visual concept or full layout/page/panel plan and reading order; continuity/person mapping only when required by comics, person references, branding, or an explicit series request; explicit must-keeps and content boundaries; and typography/layout constraints. When a style reference image is used, include the exact sentence `以该图作为艺术风格参考。` once inside every copyable prompt. Do not include its local path, filename, `STYLE` label, input index, attachment-role map, or upload instructions. End with any exact typesetting copy or known limitations needed for correct use. Return the absolute Markdown path; a chat-only prompt is not completion of this mode.

For multiple non-comic outputs, repeat the selected style and explicit shared anchors, but default to a distinct strongest visual concept for each image. Do not invent a continuity bible, recurring protagonist, fixed outfit, fixed scene, identical composition, or one layout for the whole set unless the user asks for that consistency. Keep negative constraints short and limited to defects that would change meaning, facts, requested format, safety, or usability.

Prompt-only Markdown must stay free of machine-local attachment details even when the local reference exists. The user supplies the style image beside the prompt in ChatGPT, so the sentence `以该图作为艺术风格参考。` is sufficient. Keep actual attachment labels, paths, indices, and missing-input statuses only in the direct-generation workflow, where the agent is making the image call itself. Future continuity images have no path until generated; prompt-only files should repeat written continuity anchors instead of inventing attachment metadata.

Read back the saved file before delivery: verify page count/order, independent usability, resolved decisions, locked text, absence of template placeholders, and—when a style reference is intended—the exact sentence `以该图作为艺术风格参考。` in every prompt. Also verify that prompt-only Markdown contains no local filesystem paths, `STYLE` labels, input indices, attachment-role maps, or upload instructions. Omit inapplicable fields instead of inventing them. “提示词已完成” describes the file only; it is not image acceptance.

## Before generation

- Poster: apply [poster.md](poster.md), preserving the confirmed objective, audience, placement, information hierarchy and any real action destination. Generate one full poster per call; do not apply the single-graphic one-paragraph rule. Check purpose alignment as well as visual quality.

- For every type, generate exactly one full requested image/page per call. An explicit count of six social cards means six distinct full-card prompts/calls, not six zones on one card or a contact sheet. Keep required shared anchors; for non-comic sets, vary subject, scene, composition, visual metaphor, and layout as the content benefits unless the user requested uniformity. Total count is context, not the per-call image count.
- Social-card / infographic: use [social-infographic.md](social-infographic.md). Multiple information zones are allowed; preserve the selected SC-/IG- structure. Inspect factual fidelity, labels, values, units, and visual relationships; creative freedom does not authorize factual changes. Use that guide's file names for images and prompt-only fallbacks.
- Check that required style/person images are readable and can actually be attached together within input limits. A path mentioned in prose is not an attachment. Never silently drop a required reference.
- Single-graphic: generate the one complete undivided composition in one call, with one sentence/paragraph integrated into the image. Do not create panels or additional cover/variation images by default.
- Comic: use one complete page per call to preserve borders, gutters, and multi-panel rhythm. The prompt must render a finished multi-panel comic strip with physicalized speech bubbles and caption boxes embedded directly inside the prompt, never an isolated single-camera scene. For a series, use a distinct prompt per page, not variants of one prompt. Repeat style and continuity anchors; retain required person/style inputs and optionally attach a checked prior page as continuity-only.
- Keep copy readable; assign speakers only where speech is planned. Exact locked copy must remain exact. For long locked text, reserve clean text areas and supply typesetting copy instead of making it unreadable; mark that output **待排版**, not finished.

## Inspect and correct

Inspect every result against its adapted copy/concept for explicit must-keeps, locked text, mobile legibility, selected style, and creative effect. Single-graphic must contain one integrated image, without panels or a sequential scene layout. Comic additionally needs reading order, character/prop continuity, assigned dialogue, and the planned layout effect; a flattened equal grid is a defect when it destroys that effect. Do not treat authorized creative departures from the source as errors. Losing the intended joke, tension, or memorable image is substantive. If viewing is unavailable, label output **待人工检查**; a returned image is not visual acceptance.

Correct errors that damage meaning or usability: garbled/missing text, wrong speaker or sequence, broken continuity or likeness anchors, missing subject, or lost hierarchy. Harmless punctuation, equivalent editorial wording, and stylistic preferences alone do not justify regeneration. Target the defect while preserving accepted parts.

Allow at most **three retries per image/page after its initial call (four attempts total)**, counting tool failures and corrective edits. Changing prompts/tools/reference inputs never resets the counter. Stop earlier when a tool remains unavailable. At the limit, preserve usable output and the latest prompt, state unresolved issues, and request manual repair; do not accept the failed result.

## Tool-unavailable fallback

If the current agent has no suitable image-generation tool, do not attempt another service. Follow **Prompt-model delivery** and return the resulting absolute path. Also state that image generation was unavailable.

Show the prompt in the response when practical for immediate copying, but the saved file remains the required fallback artifact.

## Save and deliver

Save workspace outputs under stable names such as `graphic-01.png` or `comic-page-01.png`, choosing a new name when it already exists unless replacement was requested. Return accepted images in order with absolute paths. Report actual style/person reference use and remaining limitations honestly. Keep uninspected, failed, and awaiting-typesetting output clearly labeled.

For a serial-comic project, save source, final prompts, and page images under the current episode directory described by [serial-comic.md](serial-comic.md). Only approved character sheets and accepted continuity images belong in the project's `references/` directory. Update project progress and continuity after the episode is accepted or completed as agreed; drafts and failed images must not advance the persistent series state.

Use the user's output directory when supplied; otherwise use the workspace, never the reusable skill/assets folders. Use paths actually returned by the tool or verified after saving. A preview without a local saved file is not evidence of a saved path. For a mixed-success series, report each page separately (accepted / 待人工检查 / 待排版 / 待补参考 / failed), with its existing artifact or prompt path and remaining issue. Preserve accepted pages when repairing another page; do not restart the whole series or reset failed attempts through a mode switch.
