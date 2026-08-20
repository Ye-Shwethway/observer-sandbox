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

Accepted recent Item-side fixes:
- **PR #350** — Item Edit preflight/rollback and bounded failure diagnostics;
- **PR #351** — atomic Sandbox Character+Item batch delete;
- **PR #353/#354** — scoped cleanup controls + real `sw:list:item` callback-composition fix;
- **PR #356** — human-friendly Item draft economic presentation;
- **PR #358** — current physical-quantity normalization made re-validatable for fresh Item Edit.

Latest runtime-affecting merge: PR #358 at `9c93739655fc6981a8c5bfd31a7c83a4cce16f62`.
CI **#1194** ✅ targeted tests + CLI smoke.

### Corrected `mass.kind` finding

A fresh current-schema batch proved that `modules.physical.mass.kind` is not merely obsolete legacy data.

Current Item validation accepts authoring quantity input `{value, unit}` but normalizes it through `PhysicalQuantity.as_dict()` into `{kind, value, unit}`. Current materialization persists that normalized output. Item Edit then reconstructs the persisted payload and re-runs the same validator. Before PR #358, `_quantity()` accepted only `{value, unit}`, causing the validator to reject its own normalized persisted form.

PR #358 closes that idempotence gap without broad schema relaxation:
- authoring `{value, unit}` remains accepted;
- normalized `{kind, value, unit}` is accepted only when `kind` equals the expected physical dimension;
- unknown extras remain rejected;
- wrong dimension kinds remain rejected;
- regression covers fresh materialization followed by real Item Edit entry.

The already-approved fresh batch should therefore remain usable after deployment; it does not need recreation merely because current normalization persisted `kind`.

### Human-facing review contract retained

PR #356 remains accepted: Telegram review formats canonical money as human currency while `.txt` export keeps raw `*_minor` fields.

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

Item Creator Studio/Telegram line includes current-schema Single/Batch creation, full-schema AI fill, deterministic validation, realism/self-correction, human review + raw export, approved Item details/economics, Item Edit parity/diagnostics, and Character/Item cleanup.

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

## CURRENT ACCEPTANCE — deployed fresh Item Edit/Save

Required live sequence:
1. verify production/runtime checkpoint includes PR #358 or later;
2. reopen an already-approved fresh current-schema Item;
3. enter `✏️ Edit Item` and confirm the prior `modules.physical.mass.kind` error is gone;
4. edit representative fields -> Preview -> Apply -> Done Editing;
5. verify pre-edit Sandbox pause state restores;
6. verify Real World/canonical state remains unchanged.

Do not delete/recreate the current fresh batch solely because normalized quantity `kind` exists. If another fresh Item failure appears, repair the concrete current-contract/runtime issue rather than weakening unrelated validation.

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

## Test / release policy

- smallest relevant tests while iterating;
- regression tests must reproduce the actual persistence/re-entry boundary when bugs occur there;
- Creator-facing previews use human-readable presentation while technical exports may preserve canonical/raw representation;
- PR CI is repository acceptance gate;
- deploy/live behavior is verified separately from merge;
- continuity docs update after material work and persistent branches exact-sync after acceptance.

---

## Exact resume point

**PR #358 is merged at `9c93739655fc6981a8c5bfd31a7c83a4cce16f62`; CI #1194 is green. The fresh Item Edit failure was a validator-idempotence bug: current validation persisted normalized physical quantities as `{kind,value,unit}` but previously re-accepted only `{value,unit}`. The bounded fix accepts its own normalized representation only with the correct dimension and keeps other unknown fields invalid. Verify deployment, reopen the existing fresh batch, finish Edit/Preview/Apply/Done acceptance, then start I5.11.**
