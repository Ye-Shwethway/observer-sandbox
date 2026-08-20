# Creator Studio Human Review UI v1

Status: LOCKED PRESENTATION CONTRACT

Creator-facing review screens must present domain facts in human language, not internal schema or graph syntax.

## Item review

- Resolve batch-local references such as `$camping-backpack` to the referenced Item display name, e.g. `Camping Backpack`.
- Hide internal definition keys and batch refs from normal Telegram review screens.
- Keep exact internal refs and payloads in exported technical draft files for audit/debugging.
- Translate internal enums when a natural display label exists, e.g. `unique` -> `Individual item`, `stack` -> `Grouped quantity`.
- Suppress null relationships and unused fields in normal review screens.
- Translate the standard `economically_immaterial + excluded` policy to `Value tracking: Not included — no monetary value was supplied`.
- Use human labels and units for module fields.

## Export filenames

Exports must be identifiable without opening the file.

- Single Item: `creator-studio-item-<item-name>-rN.txt`
- Item Batch: `creator-studio-item-batch-<first-item-name>-plus-<remaining-count>-rN.txt`
- Character: `creator-studio-character-<character-name>-rN.txt`

Names are lower-case filesystem-safe slugs. Revision remains part of the filename.

The exported text remains the technical/audit artifact and may preserve internal refs and exact structured payloads even when the Telegram review hides them.
