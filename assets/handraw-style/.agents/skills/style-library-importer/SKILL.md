---
name: style-library-importer
description: Add a named or locally referenced visual style to the numbered hand-drawn style library, deriving visible traits from supplied images or generating a representative image when needed.
---

# Text-Defined Style Library Importer

Use this Skill when the user explicitly wants to add a reusable visual style using a name, visual traits, or a local reference image. Compare existing names, traits and examples first; skip duplicates and report the existing number. Source URLs may be recorded as provenance, but this workflow does not fetch posts or download their images.

## Interpret the input

- **Name only:** keep the supplied name as the style label, do not invent or store visual traits, and register `name_activation=strong`, `traits_activation=none` for `gpt-image-2`.
- **Name plus traits:** preserve the name, retain only positive concrete visual traits, remove negative clauses such as `避免`、`不要`、`不准`、`禁止` or `无写实纹理`, and register `name_activation=weak`, `traits_activation=strong`.
- **Traits only:** invent a readable Chinese style label and a concise English generation name, retain only positive concrete visual traits, and register `name_activation=weak`, `traits_activation=strong`.
- **Image only:** inspect the supplied image, derive positive visible traits, and create a descriptive Chinese label and English generation name. Do not invent an artist attribution. If the image cannot be inspected, ask for the missing description before registration.

For every text-defined style, `gpt-image-2` must use its configured text activation and must not receive a reference image. Unknown models retain the library's existing image fallback behavior.

## Representative image

If the user provides an image alongside textual input, use it directly as the representative source image; do not generate another one.

If no image is provided, generate one original 1:1 representative image using the client's available native image tool. Inspect required inputs and use at most three retries after the first call, counting failures and edits; stop earlier for persistent tool unavailability. Inspect the result before import; if generation is unavailable, request a supplied local representative image before registration. Select a simple neutral subject and setting that make the declared style legible. Use the supplied name and, when present, the filtered positive traits; do not reuse subjects, actions, scenes, compositions, or stories from existing library entries. Generate one image, not a contact sheet. The generated image's model does not establish measured activation performance for other models.

## Import

After a square representative image is available, run the deterministic importer from the bundled library root (three parent directories above this SKILL.md). Relative image paths resolve from that working directory. Fit a non-square input proportionally with padding rather than stretching it.

```powershell
python scripts/import_manual_style.py --source-name "中文风格名" --generation-name "English Generation Style Name" --traits "正向可见特征" --image "./representative.png" --dry-run
```

- Omit `--traits` for name-only input.
- For traits-only input, pass the names you created with `--source-name` and `--generation-name`.
- Run `--dry-run` first, then remove it to register after preflight passes. Read the actual returned number; preflight does not reserve one.
- The importer assigns the next number, creates a 512px numbered tile, and continues the active H contact sheet. A single supplied or generated representative image does not create a reference grid; the numbered single image is used if a reference is required. This CLI accepts one `--image`; it does not accept multiple source images. The lower-level library can build grids, but do not pass unsupported repeated image arguments here. The importer then updates the source table and capability metadata, rebuilds the gallery, and runs full validation.

Manual styles use a number-only gallery badge. Do not add a fictitious author handle. Report the number, activation path, whether an image was generated or supplied, the active H sheet, and the validation result.

Imports use a lock and rollback backup. On failure, inspect the reported recovery state before retrying; do not bypass a retained lock. Run read-only validation from the library root with `python -B -X utf8 skills/handdraw-style-prompter/scripts/validate_library.py`. Pillow is required. Keep provenance/license records when available; model activation entries are configured policy, not measured benchmark results.
