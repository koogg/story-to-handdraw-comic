---
name: handdraw-style-prompter
description: Create bilingual prompts from a local numbered hand-drawn style and theme, or plan article illustrations with the bundled style library.
---

# Hand-drawn style package

Install this complete package at path `.`; nested skills depend on its `images/` and catalog. This file is a compatibility entrypoint for the same style skill, not a second workflow.

Read only the applicable entry:

- Numbered theme prompts or requested images: [handdraw-style-prompter](skills/handdraw-style-prompter/SKILL.md).
- Article illustration positions/concepts/prompts: [article-illustration-planner](skills/article-illustration-planner/SKILL.md), which uses the style resolver.
- Explicit reusable-style additions: [style-library-importer](.agents/skills/style-library-importer/SKILL.md).

Resolve resource paths relative to their owning skill files. Do not load every entry for one request.
