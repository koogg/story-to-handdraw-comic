# Local style library maintenance

The bundled library is `assets/handraw-style`, relative to the parent SKILL.md. Normal style use is local and read-only. Add, correct, or remove reusable styles only within the user's requested scope.

## Add a style


- Run commands from the library directory; resolve supplied relative image paths from that working directory.
- The CLI accepts one square representative image. For multiple examples, prepare one coherent square board before import. Preserve proportions and available source/license records.
- `--dry-run` validates without reserving a number. The completed import reports the actual number, updates catalog/policy/assets/gallery/manifest, and runs validation.
- Imports use a lock and backup. Handled failures restore managed files; failed rollback retains the lock and reports its backup path. After abrupt termination, inspect both before recovery. Do not blindly delete a lock or retry a possibly completed import.
- Verify the returned number from the comic skill directory: `python -B -X utf8 scripts/resolve_style.py --model unknown --style <new-number>`.

## Update or remove a style

Correct the authoritative `styles_200_reorganized.md` and any affected numbered asset/capability metadata. From the library root, rebuild with `python -B -X utf8 skills/handdraw-style-prompter/scripts/build_library.py`, then validate with `python -B -X utf8 skills/handdraw-style-prompter/scripts/validate_library.py`. Validation is read-only; rebuilding is explicit.

Removing or renumbering entries can break saved numbers: perform it only when explicitly requested and migrate dependent references together. Importers maintain README/manifest counts and contact-sheet records; those files have script callers and must not be removed as redundant documentation.

Maintenance and full validation require Pillow. Check the active environment before installing missing dependencies.
