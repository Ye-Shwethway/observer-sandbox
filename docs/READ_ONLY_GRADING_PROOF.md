# Read-Only Grading — Exemplar + Attribute Batch 1

Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED; TELEGRAM PRESENTATION EXTENSION VALIDATION PENDING

## Purpose

Prove grading as a derived cross-domain layer without making grades authoritative state, then expand the proven same-scale pattern in one batch.

The underlying profile value remains authoritative. No grade column is added to profile tables.

## Exemplar

First proof:

`Darian raps_pa.strength raw value -> named evaluator -> derived grade -> Telegram Attributes display`

Darian's authoritative Strength value remains `90`; the evaluator derives `S · Expert` without mutating that stored value or its mode.

Scheme ID: `raps-100-proof-v1`.

Current proof bands remain:
- S: 90..100 — Expert
- A: 75..<90 — Advanced
- B: 60..<75 — Skilled
- C: 40..<60 — Capable
- D: 20..<40 — Novice
- E: 0..<20 — Beginner

The thresholds are unchanged from the accepted 0..100 proof. The human-readable labels are aligned with the shared grade vocabulary.

The complete shared vocabulary is:
- E — Beginner
- D — Novice
- C — Capable
- B — Skilled
- A — Advanced
- S — Expert
- SS — Elite
- SSS — Master
- X — Mythic
- XX — Transcendent

The current 0..100 RAPS proof scheme legitimately reaches only E through S. Higher tiers remain available to future named schemes whose underlying scale/semantics support them; they are not artificially compressed into 0..100.

Exemplar evidence:
- PR #12 merge `d0bdabc1faaede8adb6c3e8dd29a9b5ff9ba3cb3`;
- PR CI #381 / `31683547016` SUCCESS;
- pre-merge Read-Only Grading Proof Acceptance #1 / `31683547092` SUCCESS on a disposable production DB copy;
- release `ae9374a96ebcf243d8e091668cf586b7e2fb510f`;
- Deploy #138 / `31683632205` SUCCESS.

## Attribute Grading Batch 1

After the Strength exemplar proved the pattern, the same evaluator was expanded to **36 explicitly opted-in 0..100 fields** represented in the Attributes section across:
- physical / RAPS-PA;
- mental / RAPS-MA;
- 0..100 intellectual / RAPS-IA fields;
- social;
- verbal-charisma / RAPS-VC.

Membership is explicit in code. A future numeric field does not silently acquire this scheme merely because it shares a domain or happens to fit 0..100.

Important exclusions:
- `raps_ia.iq = 140` is not graded by this scheme because its scale semantics differ;
- Skills are not part of Attribute Batch 1;
- Body is not part of Attribute Batch 1.

Batch evidence:
- PR #13 merge `76bcf7fe7225a9504909f9d939bbcdd673bac7c6`;
- final PR CI #386 / `31683936756` SUCCESS;
- pre-merge Attribute Grading Batch 1 Acceptance #3 / `31683936844` SUCCESS on one disposable production DB copy, proving all 36 grades together, IQ excluded, Body excluded, Skills excluded, raw profile unchanged, Telegram rendering present;
- release `d14cae7ef88fc9e157caa5fa0b930f36aba3cf77`;
- Deploy #139 / `31684009154` SUCCESS.

## Telegram presentation extension

The schema-driven Telegram profile slice extends presentation without changing grading authority.

Individual graded fields render as:

`Strength   90 (S) · Expert`

The profile query also derives current aggregate grading for the Attributes display:
- each compatible domain/group uses the arithmetic mean of its current participating values and evaluates that mean through `raps-100-proof-v1`;
- the overall Attributes grade uses the same process across all current participating values;
- values from incompatible schemes/scales are excluded rather than coerced.

For the current Darian profile, the represented RAPS-PA values average approximately `86.54`, therefore the current Physical group evaluates to `A · Advanced`, while Strength itself remains `S · Expert` at 90. These are read-time results, not authored labels.

No aggregate grade is persisted. If an underlying authoritative value changes, individual/group/overall grades are recomputed on the next read.

## Architecture boundary

- grading logic lives outside Telegram presentation;
- profile query attaches derived grade metadata;
- Telegram consumes derived metadata;
- raw authoritative values remain untouched;
- aggregate grades are not persisted state;
- progression engines remain independent of display grading.

## Body grading boundary

Body measurements require a **separate evaluator family** and must not reuse `raps-100-proof-v1` by convenience.

Height, weight, body-fat percentage and circumferences can require materially different context and mathematics: units, sex/height normalization, body composition, proportional relationships, target ranges and actor-specific genetic ceilings. Therefore body grading follows the same development policy at a higher semantic boundary:

`one body-measurement exemplar -> prove formula/context -> one separate body-measurement batch`

Do not batch Body together with Attributes. Do not assume every body field should share one formula merely because all are displayed in one profile section.
