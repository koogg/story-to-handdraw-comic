# Comic page prompt contract

Use only for the comic branch. Standalone opinions/reflections use [single-graphic.md](single-graphic.md); do not apply this panel template to them.

Use this structure for each page. Omit fields that do not apply, but never omit storyboard mechanism, reading order, continuity, or panel descriptions. Use the creatively adapted script, not the raw user paragraph. Rendering consistency applies to the new script; it must not pull the adaptation back toward a literal retelling.

```text
Use case: illustration-story
Asset type: finished hand-drawn comic page, page {N} of {TOTAL}
Primary request: Render one complete comic page from the panel plan below.
Publishing target and canvas: {Xiaohongshu 3:4 / WeChat body 3:4 / WeChat cover 2.35:1 / other}
Audience and use: {reader group; platform or purpose separately}
Output structure: {single page / continuous series; requested total pages}
Text mode: {creative (default; editorial alias) / faithful / verbatim; scope of explicitly locked copy}
Core meaning and creative treatment: {the broad idea retained; the new hook, situation, or metaphor}
Explicit user must-keeps: {only user-protected characters, objects, events, or outcomes and where shown; otherwise none}
Required exact display copy: {mark each required quote LOCKED with speaker/placement, or none}
Content boundaries: {forbidden changes/elements; permitted additions}

ART DIRECTION
Catalog style number and generated name: #{STYLE} · {GENERATED_NAME}
Positive visible traits: {PROMPT_TRAITS}
Theme color: {optional matched prompt from colors.json, or omit}
以该图作为艺术风格参考。

PAGE STRUCTURE
Primary storyboard mechanism: {ID and name}
Optional accent mechanism: {ID and name, or none}
Series layout role: {this page's story state and why this mechanism differs from or intentionally repeats adjacent pages}
Expressiveness level: {clear / varied / experimental}
Visual thesis: {the story contrast, movement, object, space, or payoff embodied by the page geometry}
Reading order: {explicit path}
Panel geometry: {count, relative sizes, borders/gutters, and position of the dominant panel}
Layout contribution: {what would be lost if these beats were placed in equal boxes}
Mobile hierarchy: the first focal point, dialogue, and final beat remain immediately legible on a phone screen.

NARRATIVE EXPRESSION
Tone: {selected humor / irony / warmth / reflection, independent of the visual style}.
Pacing and information density: {requested or inferred rhythm, pauses, and dialogue density}.
Payoff and timing: {the specific contrast, reaction, callback, or insight; which panel reveals it}.
Preserve the scripted speaker assignments, gestures, pauses, and reveal order. Do not replace character dialogue with plot-summary captions or add an unscripted moral. These instructions guide rendering and are not text to print on the page.

CONTINUITY BIBLE
{stable characters, clothing, scale, props, palette, setting facts}

PERSON REFERENCES (when supplied)
{Actual attachment-to-character map, visible anchors, likeness priority, and the personalized-character block from person-reference.md.}

PANEL PLAN
Panel 1 — {shot size}; {visible action and setting}; {character state}; Display text: "{TEXT}".
Panel 2 — ...

TEXT RULES
Render only quoted display text from the adapted script. Text marked LOCKED must be verbatim; other quoted text is the selected creative copy and may vary when meaning, speaker, and comic timing remain intact. Keep balloons/captions inside their intended reading areas with clear tails and ample padding. No watermark, signature, labels, or extra writing unless specified. Include titles or sound effects when they strengthen the planned hook, action, or payoff.

CONSTRAINTS
Maintain the same character design, clothing, colors, and recurring props across all panels. No duplicate limbs or characters. Do not merge neighboring scenes. Preserve the stated page, navigation logic, and intentional hierarchy. Keep critical content inside the stated platform safe area. Do not regularize intentionally unequal panels or replace the stated visual thesis with a generic equal grid. Decorative effects cannot substitute for the specified timing, scale contrast, recurring object/background, route, or payoff hierarchy.
```

The copyable prompt above is the prompt-mode form for ChatGPT web. Do not add a local reference path, filename, `STYLE` label, input index, attachment-role map, or upload instruction to its Markdown. The user sends the chosen style image together with the prompt, and the sentence `以该图作为艺术风格参考。` is the only attachment-facing instruction needed.

The following block is for **direct image-generation tool calls only**, never for prompt-only Markdown. When a numbered style reference image is attached by the agent, label its actual input index as STYLE in the tool call's attachment map and append this block only to the tool-call prompt:

```text
Use only the image labeled STYLE as a style reference. Extract its linework, brushwork, medium, material texture, color tendencies, shape language, and overall visual language. Do not copy any subject, person, clothing, prop, action, pose, setting, background, composition, panel layout, text, or story from STYLE. Separately labeled PERSON inputs supply the designated characters' visible appearance. The written continuity bible and panel plan control character assignment, costume, action, setting, dialogue, and story.
```

## Multi-page continuity

Every page prompt repeats the full style anchor and the complete continuity subset needed by that page, plus the person-to-image mapping and likeness anchors when applicable. For a serial project, load only the active characters' stable anchors and current state from the project files, not the entire cast archive. Read [person-reference.md](person-reference.md) for photo handling and input limits. Add a short page-state line describing only changes carried from the prior page, such as `red umbrella now open` or `left knee now muddy`. If attaching an approved character sheet or earlier accepted page, label it as continuity-only and instruct the model not to copy its layout or story beats; a prior page must not replace the original person reference or approved character baseline with accumulated drift.

## Text-light fallback

When text is long or exact typography is more important than illustration, edit it down before generation. If long wording is truly locked, generate a clean page with empty reserved balloons/caption boxes, then provide the intended typesetting copy. Do not repeatedly regenerate the illustration for minor punctuation or harmless editorial variants, and do not pretend garbled or meaning-changing text is correct.

Follow [rendering.md](rendering.md) for acceptance and retry limits. A page with empty balloons and separate copy is a **待排版 / awaiting typesetting** intermediate, not a finished publishable page.

## Direct Multi-Panel Prompt Pattern (直接多格漫画生图提示词规范)

When delivering copyable text-to-image prompts for a comic page (for modern multi-modal diffusion tools such as Flux, SD3, Midjourney v6, or Ideogram), the prompt MUST generate a complete multi-panel comic page on a single canvas, not an isolated single-camera illustration.

1. **Explicit Multi-Panel Canvas Statement:**
   Always start with an explicit layout declaration:
   `A complete vertical comic strip page on a single canvas, [style traits], clean black panel borders with white gutters between panels. Aspect ratio [ratio].`
2. **Explicit Panel Geometry & Navigation:**
   Translate the chosen SB mechanism into clear spatial divisions:
   - For SB-004: `One large horizontal panel at the top (60% height), two equal square reaction panels at the bottom side-by-side (40% height).`
   - For SB-005: `Two upper compact panels (40% height), one wide payoff hero panel at the bottom (60% height).`
   - For SB-025: `Four alternating shot/reverse-shot grid panels with dynamic gutters.`
   - For SB-030: `Two tense top panels, an ultra-narrow horizontal strip in the middle, and a large payoff panel at the bottom.`
   - For SB-046: `One central dominant square hero panel surrounded by detail reaction panels.`
3. **Physicalized In-Image Text Elements (图文一体):**
   NEVER separate dialogue or narration into external formatting notes outside the prompt. Physically embed every text element directly into the per-panel prompt description:
   - **Narration/Captions:** `A rectangular caption box with Chinese text: "[TEXT]"` placed at the top or corner of the respective panel.
   - **Dialogue:** `A clean white speech bubble pointing to [character] with pointer tail, containing Chinese text: "[TEXT]"`.
   - **Sound Effects/Exclamations:** `Bold explosive sound effect text: "【[SFX]】"`.
4. **Negative Constraints for Comic Strip:**
   Ensure negative prompts explicitly forbid: `isolated single shot, single camera illustration, missing panel borders, text outside balloons, blurry speech bubbles`.
