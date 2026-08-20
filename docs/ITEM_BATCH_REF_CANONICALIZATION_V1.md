# Item Batch Ref Canonicalization v1

Status: **IMPLEMENTED ON TEST — LIVE BUG FIX**  
Date: 2026-08-20

## Problem

Creator live acceptance of PR #362 produced a valid semantic Item batch request, but the AI returned human-readable batch refs such as `LED Camping Flashlight`. The batch contract requires stable lowercase tokens using letters, digits, `_` or `-`, so the draft was rejected even after bounded self-correction.

The issue was at the AI batch canonicalization boundary, not in grading metrics.

## Contract

Before batch validation/materialization:

1. AI-produced `ref` values are normalized to stable lowercase tokens.
2. Whitespace and other separators become `_`.
3. Repeated separators collapse.
4. Leading/trailing `_`/`-` are trimmed.
5. Batch-local relationship targets are rewritten through the same alias map.
6. Existing explicit `$ref` relationship syntax is preserved after canonicalization.
7. Unknown external relationship targets are not guessed.
8. Duplicate canonical refs remain invalid under the existing batch contract; no silent renaming/counter suffix is introduced.

Example:

`LED Camping Flashlight` -> `led_camping_flashlight`

`30 L Hiking Backpack` -> `30_l_hiking_backpack`

`stored_in = "30 L Hiking Backpack"` -> `stored_in = "$30_l_hiking_backpack"`

## Safety

This is a normalization fix only. It does not change Item grading, metrics, economics, persistence authority, batch atomicity, Sandbox isolation, or canonical Real World state.
