---
name: handdraw-style-library
description: Browse the bundled hand-drawn style library and route package-level requests to its prompt, article illustration, or import skill. Use a known specialized skill directly for creation.
---

# Hand-drawn style package

Install this complete package at path `.`; nested skills depend on its `images/` and catalog. This file is the package compatibility/router entrypoint, not a second prompt workflow. Its unique discovery name is `handdraw-style-library`; `$handdraw-style-prompter` identifies the specialized nested skill. Preserve the package paths when installing.

Read only the applicable entry:

- Numbered theme prompts or requested images: [handdraw-style-prompter](skills/handdraw-style-prompter/SKILL.md).
- Article illustration positions/concepts/prompts: [article-illustration-planner](skills/article-illustration-planner/SKILL.md), which uses the style resolver.
- Explicit reusable-style additions: [style-library-importer](.agents/skills/style-library-importer/SKILL.md).

Resolve resource paths relative to their owning skill files. Do not load every entry for one request.
