# Person references for personalized comics

Read when the user supplies a portrait, headshot, or other character reference to portray someone in the comic. This is optional: ordinary text-to-comic requests remain unchanged. Use visual observation and image conditioning, not a face-recognition service or biometric embedding database.

For single-graphic output, use the same inspection, likeness, and attachment-role rules for its one image; skip panel/page continuity and do not introduce a storyboard or character sheet.

## Inputs and inspection

- Accept a conversation attachment or a user-provided local image. Inspect each actual image before describing features; do not infer appearance from its filename. Follow the available image tool's attachment requirements.
- One clear front or three-quarter headshot is usually sufficient to start. Additional views are optional and useful for angles or partially hidden features. Do not require extra photos when the supplied image is usable.
- Assign each person a stable story label such as character A. Map each input image to a character and a role. Ask only when an ambiguous group photo or multiple subjects prevents reliable assignment; never guess who a real person is or their relationship.
- Extract a compact set of visible anchors: overall face silhouette and jaw/chin, eyebrow shape, relative eye spacing, nose and mouth shape, hairstyle/hairline, glasses, facial hair, and visible distinctive marks. Keep only features that remain legible in the selected style; do not invent occluded details or infer sensitive traits or personality.
- A headshot does not establish body shape, height, or clothing below the frame. Treat those as story design choices, label them as such, and honor any user-specified costume. Do not automatically carry over the photographed background, lighting, pose, clothes, or expression.
- If the face is too small, heavily obscured, or blurred, explain the specific limitation and request a clearer reference only if likeness depends on it. Do not claim unseen details were extracted.

## Likeness and style fit

These are routing heuristics based on the catalog, not measured identity-preservation scores. Inspect the selected style and actual portrait before deciding.

| Style family / examples | Expected transfer | Guidance |
|---|---|---|
| Light sketch, anime, ink storybook | More room for recognizable facial features | Retain face silhouette, hairstyle, eyebrows, glasses, and relative facial proportions while simplifying texture. |
| Naive crayon, paper craft, gouache, flat storybook | Selective likeness | Preserve several distinguishing anchors; translate eyes, skin shading, and proportions into the style's graphic language. |
| Stick figure, bean figure, coarse pixel art | Symbolic likeness | Use hairstyle, glasses, facial hair, and permitted silhouette cues. State that detailed facial resemblance is limited. |
| Strong caricature anatomy | Intentional distortion | Preserve recognizable anchors without promising the original face geometry; exaggerated anatomy can conflict with likeness. |

Default `balanced`: preserve the most recognizable visible anchors within the chosen style. Accept `likeness-first` / 更像本人 or `style-first` / 画风优先 when requested. These are prompt priorities, not image-tool parameters.

For a strict style that erases facial geometry, briefly explain the tradeoff in the plan. Do not silently switch the selected style. If the user simultaneously requires detailed likeness and an incompatible exact style, ask which should take priority; otherwise proceed with balanced adaptation and state its limits. Do not promise exact or quantified similarity.

## Separate image roles

Maintain an attachment map matching the tool's actual input order:

- `PERSON_A`: photo(s) for character A's visible appearance only.
- `STYLE`: numbered style image for linework, medium, palette, and shape language only.
- `CONTINUITY`: a previously accepted comic page for established stylized appearance, costume, and story state only.

The style resolver's `use_reference_image` flag controls **STYLE only**. A false value never means discard a supplied person photo. Do not let style-image characters replace the user, blend multiple people's features, or use a previous page's drift to override the original person reference.

Attach the person reference and any required style reference through the image tool; mentioning a path in the prompt is not an attachment. For multiple people, keep separate labels and use those labels in each panel. For tools that support local paths, resolve them at runtime; for conversation images, use the supported attachment mechanism. Do not mix mutually exclusive tool input methods or claim that an unavailable input was passed.

If the tool cannot take both a person photo and a required style image, explain the limitation. A text-only style anchor is acceptable when the resolver does not require a style image. Otherwise pause that image generation and provide the prepared prompt and missing-input requirement; never silently omit either required reference. If the tool cannot accept any images, deliver a plan marked as awaiting reference-capable rendering, not a personalized result.

## Workflow and quality

1. Add the image-to-character map, likeness priority, visible anchors, and story-designed costume to the continuity bible. Present a short human-readable summary with the normal pre-generation plan; no extra approval gate for usable supplied photos.
2. Generate the first requested comic page directly with the photo and style inputs. Use this page as the stylized continuity anchor after checking it. Create a separate character sheet only when the user requests it; do not add an unrequested preparatory image by default.
3. For later pages, retain the same person reference, written anchors, and style; also pass the checked page when supported. If input capacity is limited, omit the optional continuity page before dropping a required person/style reference.
4. Inspect each result against the supplied photo and written anchors: face/hairstyle/glasses where visible, no character swaps or blended faces, consistent proportions across panels, and preservation of the selected style. Do not mistake a generic same-hairstyle avatar for detailed facial likeness. Consider whether panel size allows the requested facial detail before retrying.
5. Correct substantive loss of distinguishing features with targeted edits that preserve layout, dialogue, and other characters. Reference/likeness corrections share the page budget in [rendering.md](rendering.md); changing prompts or continuity anchors does not reset it. Disclose remaining differences at the limit.

Use supplied photos only for the current task. Do not add personal photos or their feature descriptions to the shared style catalog, gallery, source import records, or reusable skill examples unless the user explicitly asks. Save project-specific character notes only when needed for the requested continuing project, alongside its outputs.

## Prompt block

Fill the attachment indices from the actual call; remove unused roles. If this block is used, the style-isolation block must target only the STYLE input.

```text
REFERENCE ROLES
Image {index}: PERSON_A — appearance reference for character A only.
Image {index}: STYLE — visual medium and rendering reference only.
Image {index}: CONTINUITY — established stylized design and story state only.

PERSONALIZED CHARACTER
Character A visible anchors: {observed face silhouette, hair, brows, glasses, and other relevant visible features}.
Likeness priority: {balanced / likeness-first / style-first}; acceptable simplification: {style-specific translation}.
Story-designed costume/body details: {details not established by the headshot}.
Keep A recognizable through these anchors while rendering all features in the selected comic style. Expressions, actions, camera angles, costume, and setting follow the panel plan. Do not inherit the photo's background or pose, paste a photorealistic face onto the drawing, substitute the style sample's person, or blend A with another character. The person reference supplies appearance; the panel plan supplies the story.
```
