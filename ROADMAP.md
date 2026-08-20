# Observer Sandbox Roadmap

Status: **ACTIVE**  
Roadmap synchronized: **2026-08-20**

## Operating principles

- Current Creator instruction, live repo/schema, verified runtime/DB and current CI/deploy evidence outrank remembered chat context.
- AI proposes structured facts; deterministic contracts validate and mutate.
- Telegram is observer/control, never simulation authority.
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.** `runtime_ready != running`.
- Real World and Creation Sandbox mutable state remain isolated.
- Reuse established semantics instead of cloning ontologies.
- `canonical_state_fingerprint()` remains a high-value zero-canonical-mutation invariant.

---

## Current repository checkpoint

### Item Edit live hardening — PR #350

Merged: `b0083c6155006ba7103878056bceecc95413e4a3`.
CI #1189 ✅.

Live Creator evidence after the diagnostic improvement identified the failing approved Item as legacy-schema data:
`modules.physical.mass has unknown field(s): ['kind']`.

Current Item Edit entry behavior:
- validates persisted Item payload before pausing Sandbox;
- no edit session or pause-state mutation if preflight fails;
- rollback if editor home rendering fails after pause;
- owner-facing bounded `Error` + `Reason` details;
- no Item/canonical mutation on entry failure.

### Sandbox Character + Item Batch Delete — PR #351

Merged: `f9131857fcc861a5dc3b747595fc22352cd737ff`.
CI #1190 ✅ targeted tests + CLI smoke.

Accepted cleanup behavior:
- `Sandbox World -> 🗑 Batch Delete`;
- select Characters and Items together;
- per-object toggle, Select All, Clear;
- review screen + explicit final confirmation;
- Locations excluded;
- active/same-Sandbox/type validation before mutation;
- atomic deletion;
- existing FK cascades remove dependent Sandbox runtime/item rows;
- touched Item definitions are removed only when orphaned;
- delete audit events retained;
- canonical fingerprint checked in-transaction; mismatch => rollback.

---

## Completed Creator foundation

Retained complete:
- I5.2 Creation Contract Reuse Map;
- I5.3 Universal Quantity / Measurement;
- I5.4 Cross-Domain Grading;
- I5.5 Requirements / Access;
- I5.6 Universal Item Schema v1;
- I5.7 Single Sandbox Item materialization;
- I5.8 Atomic heterogeneous Item Batch;
- I5.9 Item / Container Operations;
- I5.10 Universal Location Schema v1.

Item Creator Studio/Telegram line now includes current-schema Single/Batch creation, full-schema AI fill, validation diagnostics, review/export, realism/self-correction policy, approved Item details/economics, Item Edit parity, live Item Edit diagnostics, and Sandbox batch cleanup.

---

## Locked Item ontology

`Definition -> unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Relations:
- `contains` structural/static containment;
- `located_at` dynamic physical presence;
- `stored_in` storage/container;
- `owned_by` ownership;
- `carried_by` carriage;
- `equipped_by` equipped state.

Ownership never follows automatically from location/storage.

---

## CURRENT ACCEPTANCE — clean legacy Sandbox data and retest fresh Item Edit

Reason: live Item Edit failed on an older approved Item batch carrying obsolete `modules.physical.mass.kind`. Do not weaken the current schema validator to accommodate obsolete test data.

Acceptance sequence:
1. verify PR #351 deploy/live Telegram availability;
2. Creator selects/deletes obsolete Sandbox Character seeds and legacy Items via `🗑 Batch Delete`;
3. create fresh current-schema Item(s)/Item Batch;
4. open fresh approved Item -> `✏️ Edit Item`;
5. edit a representative scalar field and a structured/module field where practical;
6. Preview -> Apply -> Done Editing;
7. verify pre-edit Sandbox pause state restores;
8. verify Real World/canonical state unchanged.

If current-schema live Item Edit still fails, fix the concrete current-data/runtime issue; do not silently canonicalize persisted legacy data unless explicitly designed as a migration slice.

---

## NEXT AFTER fresh Item Edit acceptance

### I5.11 — Sandbox Location Creation + Embedded Contents

Required semantics:
- strict I5.10 Location materialization;
- active same-Sandbox parent validation;
- acyclic structural parent graph;
- structural parent uses `contains`;
- interface destinations validate active same-Sandbox Locations;
- embedded Items reuse I5.6/I5.8 contracts;
- ordinary movable Items use `located_at`, or exact `stored_in` typed containers;
- validate whole Location + contents graph before writes;
- one atomic apply/rollback;
- no automatic runtime readiness;
- no autonomous execution;
- no canonical writes.

Then I5.12 Location Contents Operations -> I5.13 Character/Location Binding & Runtime Readiness -> I5.14 Runtime Affordance Bridge -> I5.15 Sandbox Vertical Acceptance.

Full Sandbox autonomous ticking remains separately unauthorized.

---

## Transmigration / Character locks

Nothing transmigrates automatically. I6 stays planning/validation only unless Creator expands scope. Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed. Existing Character Manual/AI parity and Sandbox profile/edit/grade-target behavior stay locked.

---

## Exact resume point

**PR #351 is merged at `f9131857fcc861a5dc3b747595fc22352cd737ff` after CI #1190 passed. Mixed Character+Item Sandbox batch delete is repository-accepted. Live Item Edit root cause on the old batch is confirmed as obsolete `modules.physical.mass.kind`. Next verify deployment, clean the selected legacy Sandbox data, create fresh current-schema Items, and complete live Item Edit acceptance. I5.11 starts only after that gate closes.**
