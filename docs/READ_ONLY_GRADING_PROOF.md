# Read-Only Grading Proof

Status: CANDIDATE

## Purpose

Prove the first grading architecture without making grades authoritative state.

Exemplar:

`Darian raps_pa.strength raw value -> named evaluator -> derived grade -> Telegram Attributes display`

The raw profile value remains authoritative and unchanged. No grade column is added to profile tables and schema v4 is unchanged.

## Proof scheme

Scheme ID: `raps-100-proof-v1`.

This is deliberately an exemplar scheme for current 0..100 RAPS-style attributes. It does **not** freeze the final universal cross-domain grading vocabulary.

Proof bands:
- S: 90..100
- A: 75..<90
- B: 60..<75
- C: 40..<60
- D: 20..<40
- E: 0..<20

Darian's current authoritative Strength value is 90, so the proof derives `Grade S` while leaving the stored raw value and mode unchanged.

## Architecture boundary

- grading logic lives outside Telegram presentation;
- profile query attaches derived grade metadata to the exemplar field;
- Telegram consumes the derived metadata;
- no raw-value mutation, progression, thresholds persisted as character state, or schema v5;
- only Strength is graded in this exemplar.

## Expansion policy

After this exemplar is accepted, same-scale RAPS/social/verbal-charisma attributes may be expanded as one batch using the proven evaluator pattern.

Body measurements are explicitly **not** part of that batch. Height, weight, body fat and circumferences may require different normalization, ratio, composition, sex/height context and genetic-ceiling semantics. Body grading therefore requires a separate exemplar and separate batch rather than reusing the 0..100 attribute evaluator by convenience.
