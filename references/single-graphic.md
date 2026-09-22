# Single text-and-image illustration — no storyboard

Use for standalone opinions, reflections, aphorisms, or an explicit one-image/no-storyboard request. Output one coherent sentence or short paragraph and one undivided image in which the text participates. Do not create panels, a hidden sequence of vignettes, sequential captions, a comic script, or a storyboard ID—even “one panel” is an unnecessary storyboard abstraction here.

## Create the copy and visual idea

Keep the broad meaning and explicit must-keeps; freely rephrase, sharpen, compress, or find an unexpected angle. Explore a few distinct verbal/visual interpretations internally, then select the most expressive and readable one. Keep the adapted text as a single thought; line breaks for typography are fine, splitting it into successive plot beats is not. Avoid inflating a sentence into a story, dialogue chain, or long essay merely to display creativity.

Find one visual situation or metaphor that adds humor, tension, warmth, or a second layer of meaning. Text need not describe the visible scene. A figure, an object, a relationship, or expressive empty space can carry the idea. Do not force a beginning–development–twist–ending structure. A quiet recognition or surprising image may be the entire payoff.

Design one focal composition with readable lettering, useful negative space, and a coherent relationship between the words and image. Respect chosen style, ratio, person references, and explicit content limits. Do not add an unrelated headline, explanatory moral, numbered steps, or extra captions. Keep exactly one output image unless the user requests additional images.

## Prompt contract

Use the resolved style and selected creative copy, omitting optional fields that do not apply:

```text
Asset type: a single hand-drawn text-and-image illustration, one undivided composition.
Canvas and audience: {ratio; intended readers/destination if supplied}.
Style: #{number} · {generation_name}; {resolver-required positive traits}.
Core idea and tone: {retained broad meaning; selected attitude}.
Visual concept: {one evocative situation or metaphor and its relationship to the words}.
Display text: "{one adapted sentence or short paragraph}".
Text fidelity: {creative by default; identify only explicitly LOCKED spans}.
Typography: {placement and hierarchy that integrate the paragraph with the illustration; allow natural line breaks}.
Explicit must-keeps: {only user-required elements, or omit}.
Reference roles: {actual STYLE and/or PERSON inputs and their distinct purposes, or omit}.
Render the selected text legibly and retain its wit, attitude, and meaning. Only LOCKED spans require exact transcription.
Create one integrated image. No panel borders, gutters, split screens, numbered scenes, sequential vignettes, storyboard, or multi-step narrative. Do not add unplanned writing.
```

When STYLE is attached, instruct the model to extract only its visual language—linework, medium, texture, palette, and shape language—not its subjects, words, setting, layout, or story. Separately labeled PERSON inputs supply only the assigned person's appearance. The written visual concept and display copy control the result. Inspect required images before attaching them.

This contract uses already-adapted copy; do not replace it with the style prompter's raw-theme/verbatim wrapper or let an additional suffix restart the writing pass. The resolver supplies style data without invoking that prompt-only workflow.

## Acceptance

Check the broad idea, distinctive expression, image/text relationship, mobile legibility, style, explicit requirements, and actual absence of panel structure. A split comic is a format defect even if the individual drawings are good. Apply [rendering.md](rendering.md) for reference checks, bounded corrections, saving, and unfinished-output labels; skip comic-only continuity and panel-sequence checks.
