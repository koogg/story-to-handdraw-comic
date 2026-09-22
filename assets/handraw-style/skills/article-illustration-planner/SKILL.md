---
name: article-illustration-planner
description: Plan illustration positions, visual concepts, and bilingual prompts for an article using the local numbered style library. Preserve the article by default; selectively simplify text only when requested.
---

# Article Illustration Planner

Decide what the article needs to communicate visually before choosing image contents. Style controls rendering, not the article's meaning. Default output is an illustration plan and prompts; generate images only when explicitly requested, including in the initial request.

## Inputs and scope

Use the supplied article and a valid local style number. Resolve the current index through [handdraw-style-prompter](../handdraw-style-prompter/SKILL.md); do not hard-code its range or invent indexed traits. Ask for missing article content or style choice when needed; choose a style when selection is explicitly delegated. Infer article type, image count, and visual strategy rather than asking the user to configure them. Honor specified audience, density/count, ratio, destination, cover, text requirements, and forbidden elements.

- **Preserve (default):** keep the article unchanged; illustrations supplement or explain it. Do not reproduce the full article unless requested.
- **Visual Rewrite:** only when authorized, shorten or replace selected passages where an image carries their meaning more effectively. Preserve voice, argument, precise definitions, numbers, dates, qualifications, attributions, and essential distinctions. Identify the exact passage, information the image must retain, and replacement/remaining prose. Leave unaffected text alone; provide a revised full article only when useful or requested, marking insertion points.

## Editorial pass

1. Read the whole article for its central idea, progression, difficult concepts, and emotional or argumentative turns. Keep internal analysis out of the deliverable.
2. Select positions where imagery improves comprehension, memory, or rhythm. Do not illustrate every paragraph, distribute pictures evenly, or add a cover automatically. A short plan—or no illustration for a section—is valid. Honor explicit counts or explain a material conflict.
3. Give each image one dominant visual proposition grounded in the surrounding text. For reflective writing, use a specific metaphor; for narrative, a meaningful moment/object; for explanation, a supported relationship, process, or comparison. Avoid generic motifs and decorative object lists. Do not fabricate factual relationships or replace source ambiguity with invented precision.
4. Choose exactly one image type from the table. Use it consistently in the plan and both prompts. It specifies the picture form, while purpose explains its editorial contribution.
5. Resolve the selected style using the style skill's capability policy. Keep a coherent visual identity across images without repeating the same composition. Labels, names, numbers, and factual claims must come from the supplied material unless external research is requested.

| Image type | Typical use |
|---|---|
| `editorial illustration` | Establish or reinforce an argument. |
| `conceptual diagram` | Explain a relationship, system, or abstraction. |
| `process diagram` | Show a sequence, causal chain, cycle, or transformation. |
| `comparison diagram` | Contrast states, groups, or outcomes. |
| `narrative scene` | Depict a concrete meaningful moment. |
| `metaphorical illustration` | Make an abstract or emotional idea visible. |

## Prompts and output

Start with a concise overall recommendation: article type, visual strategy, image count, and any authorized opportunity for visual replacement. Then list images in reading order, each with:

- **Insert after:** nearest heading or recognizable short source excerpt.
- **Purpose and visual approach:** what readers gain and the central visual idea.
- **图片类型:** one fixed value above.
- **Relationship to text:** supplements, explains, visually summarizes, or replaces part of text. Include exact edits for authorized replacements.
- **Style:** resolved number and generation name.
- **Chinese and English prompts:** style identity, image type, visual idea, essential subjects/relationships/facts, and explicit constraints.

Place `图片类型：{image_type}。` / `Image type: {image_type}.` before `主题：` / `Theme:` or the visual idea. Apply the style skill's prompt format and required reference handling. In its graphic-text mode, treat the planned visual brief as the illustration's theme; when the user supplies exact theme wording, preserve that wording instead. Keep the image-type field outside the theme and preserve the fixed suffix.

Translate article meaning into visible content rather than pasting the surrounding paragraph. Use short on-image labels only when they aid comprehension or are requested. Avoid long prose inside images, generic quality terms, unsolicited camera/lighting instructions, and unnecessary negative prompts; specify composition only when it carries meaning. For explicit generation, follow the style skill's rendering and inspection rules without asking for authorization again.
