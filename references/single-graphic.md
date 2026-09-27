# Single text-and-image illustration — no storyboard

Use after selecting the single-graphic form: standalone opinions, reflections, aphorisms, or an explicit undivided text-and-image composition. “One image” specifies count and “no storyboard” excludes sequential narrative; neither overrides an explicit social-card/infographic type or SC/IG layout. Output one coherent sentence or short paragraph and one undivided image in which the text participates. Do not create panels, a hidden sequence of vignettes, sequential captions, a comic script, or a storyboard ID—even “one panel” is an unnecessary storyboard abstraction here.

## Create the copy and visual idea

Treat a supplied theme as the meaning the whole image should convey, not as display copy. First explore distinct visual interpretations through a situation, emotion, relationship, local detail, or metaphor; choose the strongest, then write complementary copy. Do not automatically use the theme as a headline, even when quoted. Exact transcription applies only to text the user explicitly requires on-image or asks to preserve verbatim. For example, a theme about visiting Changzhou at Mid-Autumn can be conveyed through local objects, moonlight, and hospitality without printing the invitation sentence. This is an example of the distinction, not a reusable composition or slogan.

Keep the broad meaning and explicit must-keeps; freely rephrase, sharpen, compress, or find an unexpected angle. Explore a few distinct verbal/visual interpretations internally, then select the most expressive and readable one. Keep the adapted text as a single thought; line breaks for typography are fine, splitting it into successive plot beats is not. Avoid inflating a sentence into a story, dialogue chain, or long essay merely to display creativity.

Find one visual situation or metaphor that adds humor, tension, warmth, or a second layer of meaning. Text need not describe the visible scene. A figure, an object, a relationship, or expressive empty space can carry the idea. Do not force a beginning–development–twist–ending structure. A quiet recognition or surprising image may be the entire payoff.

One idea does not require one isolated object, a tiny scene, a white background, or a visual pun. A literal moment, several interacting figures, and a layered environment can express one coherent thought. Choose density and negative space for that thought; do not mechanically shrink meaningful surroundings into decorative icons. Keep locality or other required specificity recognizable through concrete details, while allowing those details to serve the shared situation rather than a checklist of objects.

This route is expressive illustration, not a promotion brief. Do not add campaign objectives, sales claims, headline/subheadline systems, calls to action, or an event-information footer unless explicitly requested. An explicit poster request belongs to [poster.md](poster.md). Improve this form through the image–copy relationship, not by importing poster design requirements.

Design one focal composition with readable lettering, useful negative space, and a coherent relationship between the words and image. Respect chosen style, ratio, person references, and explicit content limits. Do not add an unrelated headline, explanatory moral, numbered steps, or extra captions. Keep exactly one output image unless the user requests additional images.

Default to **expressiveness over cross-image consistency**. When several independent single graphics are requested, let each idea choose its strongest subject, scene, camera, scale, palette emphasis, and visual metaphor; do not reuse one protagonist, outfit, background, or composition merely to make a set look uniform. Share only the selected style and any explicit brand or series anchors. Verbatim copy locks the displayed words, not the visual treatment. Apply character continuity only when the user supplies a person reference or explicitly asks for a recurring series character.

## Prompt contract

Use the resolved style and selected creative copy, omitting optional fields that do not apply:

```text
Asset type: a single hand-drawn text-and-image illustration, one undivided composition.
Canvas and audience: {ratio; intended readers/destination if supplied}.
Style: #{number} · {generation_name}; {resolver-required positive traits}.
Theme color: {optional matched prompt from colors.json, or omit}.
Core idea and tone (creative direction, not text to print): {retained broad meaning; selected attitude}.
Visual concept: {one evocative situation or metaphor and its relationship to the words}.
Display text (the only text to print): "{one newly composed or adapted sentence or short paragraph; do not automatically copy the theme}".
Text fidelity: {creative by default; identify only explicitly LOCKED spans}.
Typography: {placement and hierarchy that integrate the paragraph with the illustration; allow natural line breaks}.
Explicit must-keeps: {only user-required elements, or omit}.
Style reference instruction: {when a style image accompanies the prompt, write exactly “以该图作为艺术风格参考。”; otherwise omit}.
Person reference mapping: {only when a person image is supplied and identity mapping is needed; otherwise omit}.
Render the selected text legibly and retain its wit, attitude, and meaning. Only LOCKED spans require exact transcription.
Create one integrated image. No panel borders, gutters, split screens, numbered scenes, sequential vignettes, storyboard, or multi-step narrative. Do not add unplanned writing.
```

In prompt-only Markdown for ChatGPT web, a style image is represented only by the sentence `以该图作为艺术风格参考。`; omit local paths, filenames, attachment labels, input indices, role tables, and upload instructions. For direct generation calls, follow [rendering.md](rendering.md) and the image tool's actual attachment-role requirements. Person inputs supply only the assigned person's appearance. The written visual concept and display copy control the result.

This contract uses already-adapted copy; do not replace it with a raw-theme draft or let an additional suffix restart the writing pass. The resolver supplies style data without invoking that prompt-only workflow.

## Acceptance

Check the broad idea, distinctive expression, image/text relationship, mobile legibility, style, explicit requirements, and actual absence of panel structure. A split comic is a format defect even if the individual drawings are good. Apply [rendering.md](rendering.md) for reference checks, bounded corrections, saving, and unfinished-output labels; skip comic-only continuity and panel-sequence checks.

Check whether the image contributes meaning beyond illustrating the words, whether local details remain specific rather than interchangeable, and whether complexity supports the single thought. A simple literal scene is valid; forcing every theme into a cute metaphor is not required. Do not judge this route by advertising impact or conversion.
