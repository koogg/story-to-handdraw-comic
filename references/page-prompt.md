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

STYLE ANCHOR
Style number and generated name: #{STYLE} · {GENERATED_NAME}
Positive visible traits: {PROMPT_TRAITS}
The style label is catalog metadata; render the described visual traits and supplied reference rather than copying any existing character or artwork.

PAGE STRUCTURE
Primary storyboard mechanism: {ID and name}
Optional accent mechanism: {ID and name, or none}
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

When a numbered style reference image is attached, label its actual input index as STYLE in the attachment map and append this block. Apply it only to that input:

```text
Use only the image labeled STYLE as a style reference. Extract its linework, brushwork, medium, material texture, color tendencies, shape language, and overall visual language. Do not copy any subject, person, clothing, prop, action, pose, setting, background, composition, panel layout, text, or story from STYLE. Separately labeled PERSON inputs supply the designated characters' visible appearance. The written continuity bible and panel plan control character assignment, costume, action, setting, dialogue, and story.
```

## Multi-page continuity

Every page prompt repeats the full style anchor and continuity bible, plus the person-to-image mapping and likeness anchors when applicable. Read [person-reference.md](person-reference.md) for photo handling and input limits. Add a short page-state line describing only changes carried from the prior page, such as `red umbrella now open` or `left knee now muddy`. If attaching an earlier accepted page, label it as continuity-only and instruct the model not to copy its panel layout or story beats; it must not replace the original person's appearance with drift from earlier output.

## Text-light fallback

When text is long or exact typography is more important than illustration, edit it down before generation. If long wording is truly locked, generate a clean page with empty reserved balloons/caption boxes, then provide the intended typesetting copy. Do not repeatedly regenerate the illustration for minor punctuation or harmless editorial variants, and do not pretend garbled or meaning-changing text is correct.

Follow [rendering.md](rendering.md) for acceptance and retry limits. A page with empty balloons and separate copy is a **待排版 / awaiting typesetting** intermediate, not a finished publishable page.
