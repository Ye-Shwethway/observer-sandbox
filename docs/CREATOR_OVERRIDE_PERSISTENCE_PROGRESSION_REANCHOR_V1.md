# Creator Override Persistence & Progression Re-anchor Correctness v1

Status: IMPLEMENTATION CONTRACT
Date: 2026-08-19

## Purpose

Creator profile corrections and overrides are authoritative represented character state. Once explicitly applied, they must survive ordinary runtime initialization, service restart, status/read commands, deployment seeding, and future progression. Old evidence from before the correction must not be replayed against the new baseline.

This contract fixes two observed false-progression classes:

1. Creator-corrected canonical/static profile values being overwritten by ordinary canonical seed re-import.
2. Observer-only grading recalibration being reported as character progression when the represented raw value did not change.

It also defines the progression evidence boundary after a Creator correction so old training/practice evidence cannot become a second path back toward the pre-edit value.

## Authority

Canonical seed files are initialization baselines, not perpetual authority over an explicitly Creator-corrected persisted value.

For an existing represented value:

`explicit Creator correction/override > ordinary seed re-import`

A canonical seed may initialize an absent/unclaimed value. It may not silently overwrite a persisted row whose source records explicit Creator profile control.

Creator correction does not mean the character experienced a sudden in-world change. It changes represented canon/current baseline according to the existing mutation class contract.

## Persistence rule

`character_profile_values.source = creator-profile-control-v1` is a durable persisted override marker for ordinary seed import.

`profile_seed.import_seed(...)` must preserve such rows regardless of whether their mode is `canonical`, `static`, `derived`, or `simulated`, subject to the editor already refusing edits of deterministic derived-only state.

Existing `mode` and owning `authority` are not falsified merely to make the persistence rule work. Creator provenance is represented by the explicit source/audit event.

This rule is universal and actor-agnostic.

## Progression evidence boundary

An applied Creator edit establishes a new progression baseline at the current simulation time.

Pre-edit evidence must not be re-realized against the new baseline. Future evidence after the correction may progress normally.

Minimum v1 boundary:

- Skills already record `creator_reanchored_sim_time` in skill metadata. Skill progression must ignore otherwise eligible evidence at or before that represented boundary for the edited skill.
- Progression-owned profile fields use a generic per-character/per-field Creator re-anchor time in runtime state. Generic physical-attribute progression must ignore otherwise eligible evidence at or before that boundary.
- The boundary suppresses replay only; it does not fabricate a settlement or organic gain/loss event.
- The Creator edit audit event remains the provenance record.

The re-anchor boundary is field-scoped. Editing one field must not discard unrelated progression evidence.

## Hard-gain policy

Do not tune progression constants in response to a seed-restore or evidence-replay bug.

The existing fresh-evidence formulas already contain level/proficiency diminishing returns. First close replay/overwrite paths, then measure clean post-edit fresh-session gains.

Only if clean evidence demonstrates excessive gains should rate constants or diminishing curves be revised in a separate calibrated change.

Expected qualitative progression:

- E/D may improve faster than advanced grades, but not by multi-grade jumps from ordinary single sessions.
- B slows materially.
- A is hard-gain territory.
- S requires sustained high-quality relevant evidence and must not be trivially recovered by one ordinary session.

## Notification semantics

`CHARACTER PROGRESSION` represents a change in represented character state, not a change in observer interpretation rules.

A grade transition with effectively unchanged underlying raw value must not be emitted as organic progression.

Examples:

- `Waist / Hips 0.846 -> 0.846, S -> A` caused only by a new grading reference: suppress.
- raw value changes slightly and crosses a grade boundary: surface, even if the raw delta is below the ordinary numeric notification threshold.
- ordinary raw value change above threshold: surface normally.

Historical notification baselines are observer state and may be re-anchored after explicit Creator edits as already implemented.

## Non-goals

- no schema migration;
- no global wipe of progression history;
- no deletion of historical training/action events;
- no character-specific Darian rule;
- no automatic restoration of a previously overwritten production value without explicit Creator instruction;
- no Mind Engine behavior in this slice;
- no grading-system redesign.

## Acceptance

Disposable acceptance must prove:

1. Apply a Creator correction to a canonical/static profile value.
2. Run normal `initialize(...)`/seed import again.
3. Corrected value remains unchanged and Creator source provenance survives.
4. A pre-edit physical progression stimulus cannot affect the newly corrected field after re-anchor.
5. A post-edit eligible physical stimulus can progress the field normally.
6. Equivalent pre/post boundary behavior is proven for an editable Skill.
7. Grade-only recalibration with identical raw value creates no progression notification.
8. A real nonzero raw change that crosses a grade boundary still creates a notification.
9. No production character mutation is required for acceptance.
10. Schema remains v15.
