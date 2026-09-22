# Rendering and acceptance

Read when generating, repairing, or delivering prompts for comic pages, single text-and-image illustrations, social cards, or infographics. Each page or standalone image has its own attempt budget. Use the available native image-generation tool and its current attachment rules. Do not call independent image APIs or inspect credential/configuration files.

## Prompt-model delivery

If the user selects **提示词模型** (also accept 提示词模式 / 仅提示词) or explicitly asks for prompts, do not call an image-generation tool. Finish the same adaptation, style resolution, layout/storyboard design, and person/reference mapping that image generation would use, then save all final prompts in one Markdown file in the user's workspace. Use `graphic-prompts.md`, `social-card-prompts.md`, `infographic-prompts.md`, or `comic-page-prompts.md` as appropriate, choosing a new name rather than overwriting an existing file.

The file must be directly usable outside this conversation: no `{placeholders}`, omitted decisions, chat-history dependencies, or instructions to “use the plan above.” Start with a short usage note, then give one separately copyable fenced prompt per requested image/page. Every prompt must repeat the shared context it needs, including asset type, ratio and output count; resolved style number/name/positive traits; complete adapted display text with LOCKED spans, speaker, and placement; tone and core meaning; visual concept or full layout/page/panel plan and reading order; continuity/person mapping; explicit must-keeps and content boundaries; typography/layout constraints; and each required reference image's absolute path and role. State beside every reference that the user must upload it to the external image tool because a path alone is not an attachment. End with any exact typesetting copy or known limitations needed for correct use. Return the absolute Markdown path; a chat-only prompt is not completion of this mode.

## Before generation

- Social-card / infographic: generate one complete card or information graphic per call using [social-infographic.md](social-infographic.md). Multiple information zones are allowed; preserve the selected SC-/IG- structure. Inspect factual fidelity, labels, values, units, and visual relationships; creative freedom does not authorize factual changes. Use that guide's file names for images and prompt-only fallbacks.
- Check that required style/person images are readable and can actually be attached together within input limits. A path mentioned in prose is not an attachment. Never silently drop a required reference.
- Single-graphic: generate the one complete undivided composition in one call, with one sentence/paragraph integrated into the image. Do not create panels or additional cover/variation images by default.
- Comic: use one complete page per call to preserve borders, gutters, and rhythm. For a series, use a distinct prompt per page, not variants of one prompt. Repeat style and continuity anchors; retain required person/style inputs and optionally attach a checked prior page as continuity-only.
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
