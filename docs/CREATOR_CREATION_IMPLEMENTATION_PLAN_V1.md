# Creator Creation Systems — Minimum Implementation Plan v1

Status: **APPROVED IMPLEMENTATION PLAN — SANDBOX CLEANUP / FRESH ITEM RETEST ACTIVE**  
Date: 2026-08-20

## Objective

Build Creator Creation through bounded reusable contracts that create realistic Sandbox content without mutating canonical Real World state.

Core rules:
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.** `runtime_ready != running`.
- AI fills structured canonical forms; deterministic services validate and mutate.
- Real World and Creation Sandbox mutable state remain isolated.

---

## Current repository boundary

### PR #350 — Item Edit live-entry hardening

Merged commit: `b0083c6155006ba7103878056bceecc95413e4a3`.
CI #1189 passed.

Item Edit now preflights the persisted Item before Sandbox pause/session creation, rolls back pause/session state on entry-render failure, and surfaces bounded owner-facing error type/reason details.

Live evidence then identified the obsolete approved batch payload field:
`modules.physical.mass.kind`.

Policy: do not weaken current `item-v1` validation just to admit obsolete test data. Clean old Sandbox test objects and retest with fresh current-schema creation first.

### PR #351 — Sandbox Character + Item Batch Delete

Merged commit: `f9131857fcc861a5dc3b747595fc22352cd737ff`.
CI #1190 passed targeted regression and CLI smoke.

Implemented contract:
- entry from Sandbox World via `🗑 Batch Delete`;
- mixed Character + Item selection;
- Select All / Clear / per-object toggles;
- review screen and explicit destructive confirmation;
- Locations deliberately outside this slice;
- all targets must be active, same-Sandbox, Character/Item objects;
- one atomic delete operation;
- FK-dependent Sandbox rows cascade;
- Item definitions touched by deletion are removed only when no surviving instance references them;
- Sandbox delete audit events retained;
- canonical fingerprint checked before transaction release; mismatch rolls deletion back.

---

## Completed Creator foundation — do not rebuild

- I0 Creator authority hardening;
- I1 universal creation proposal/socket core;
- I2 isolated Creation Sandbox persistence/lifecycle;
- I2.5 Sandbox clock/speed/pause/readiness/AI binding;
- I3 Character + Location representation proof;
- I4 Creator Studio proposal lifecycle;
- I4.1 Sandbox Character configuration UX;
- I5/I5.1 Sandbox Observer foundations;
- Character Manual/AI parity;
- Sandbox Character profile/edit/grade-target parity;
- explicit Real/Sandbox runtime controls;
- I5.2 reuse map;
- I5.3 universal quantity/measurement;
- I5.4 cross-domain grading;
- I5.5 requirements/access;
- I5.6 Universal Item Schema v1;
- I5.7 single Sandbox Item materialization;
- I5.8 atomic heterogeneous Item Batch;
- I5.9 Item/container operations and `update_sandbox_item()`;
- I5.10 Universal Location Schema v1;
- Item Creator Studio Single/Batch UX and current full-schema AI fill;
- Item review/export, ordinary-realism validation, bounded one-retry self-correction;
- approved Item detail/economic presentation;
- Sandbox Item field edit/save parity;
- safe Item Edit entry diagnostics/rollback;
- mixed Character+Item Sandbox batch cleanup.

---

## Universal Creator AI contract

`Creator intent -> complete canonical type schema/form -> AI fills form -> narrow explicitly-authorized canonicalization -> deterministic validation -> preview -> explicit approval -> Sandbox-only materialization`.

AI is not schema designer, validator bypass or direct mutation authority. Unknown nullable numeric facts remain null instead of fabricated precision.

---

## Locked Item ontology

`Item Definition -> concrete unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Relations:
- `contains` = structural/static containment;
- `located_at` = dynamic physical presence;
- `stored_in` = storage/container;
- `owned_by` = ownership;
- `carried_by` = carriage;
- `equipped_by` = equipped state.

Ownership does not follow from physical presence/storage. Sandbox-only mutable state must not mutate Real World state.

---

# CURRENT ACCEPTANCE SLICE

## Legacy cleanup -> fresh current-schema Item -> live Edit/Save proof

### Why this gate exists

The observed Item Edit failure is not evidence that the current editor contract should accept `modules.physical.mass.kind`; it is evidence that an older test Item batch was persisted under an obsolete shape. The fastest clean acceptance path is to remove obsolete Sandbox test data and exercise the full current creation/edit pipeline from a fresh object.

### Required live sequence

1. Confirm the PR #351 deployment is present in Telegram.
2. Open Sandbox World -> `🗑 Batch Delete`.
3. Select the obsolete Character seeds and legacy Items requested by Creator.
4. Review the list; confirm deletion.
5. Verify selected objects disappear while Locations remain untouched.
6. Create a fresh current-schema Item or Item Batch through Creator Studio.
7. Open a fresh approved Item -> `✏️ Edit Item`.
8. Exercise edit entry, field input, Preview, Apply, and Done Editing.
9. Verify Sandbox pre-edit pause state restores correctly.
10. Verify Real World/canonical state remains unchanged.

### Failure policy

If the fresh current-schema Item still fails:
- surface exact error/reason;
- repair the concrete current-schema/runtime defect;
- do not add broad legacy canonicalization or validator relaxation as an incidental fix.

A dedicated legacy migration path may be designed later only if old Sandbox content is worth preserving. The present Creator direction is cleanup and fresh recreation.

---

# NEXT AFTER FRESH ITEM EDIT ACCEPTANCE

## I5.11 — Sandbox Location Creation + Embedded Contents

Objective: materialize strict I5.10 Locations in isolated Sandbox state, optionally with typed Item contents, while reusing Item contracts rather than inventing a Location-only contents model.

Required semantics:
- active same-Sandbox parent validation;
- acyclic structural parent graph;
- structural parent uses `contains`;
- interface destinations validate active same-Sandbox Locations;
- embedded Items reuse I5.6/I5.8 contracts/services/storage;
- movable Items normally use `located_at`, unless exact graph establishes `stored_in` a typed container;
- validate complete Location + contents graph before writes;
- atomic whole-graph success or zero partial graph;
- no automatic runtime readiness;
- no autonomous ticking;
- no canonical writes.

Then I5.12 Location Contents Operations -> I5.13 Character ↔ Location Binding & Runtime Readiness -> I5.14 Item/Location Runtime Affordance Bridge -> I5.15 Sandbox Vertical Acceptance.

---

## I6 / Character locks

Transmigration remains inactive/planning-only. Nothing transmigrates automatically. Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed. Existing Character parity contracts stay locked.

---

## Test / release policy

- smallest relevant tests while iterating;
- PR CI as repository acceptance gate;
- full fallback only for cross-cutting/unmapped risk;
- deploy/live behavior verified separately from merge;
- continuity docs updated after material work and persistent branches exact-synced after acceptance.

---

## Exact resume point

**PR #351 merged at `f9131857fcc861a5dc3b747595fc22352cd737ff` after CI #1190 passed. Sandbox mixed Character+Item batch delete is repository-accepted. The old Item Edit failure is confirmed as obsolete `modules.physical.mass.kind` data. Next verify the deployed delete UI, clean selected legacy seeds/items, create fresh current-schema Item(s), and complete live Item Edit/Save acceptance. I5.11 Location Creation + Embedded Contents follows only after that proof is green.**
