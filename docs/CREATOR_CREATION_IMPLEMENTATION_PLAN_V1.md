# Creator Creation Systems — Minimum Implementation Plan v1

Status: **APPROVED IMPLEMENTATION PLAN — ACTIVE ITEM EDIT WIP**  
Date: 2026-08-20

## Objective

Build Creator Creation through bounded reusable contracts that create realistic Sandbox content without mutating canonical Real World state.

Core rules:
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.**
- `runtime_ready != running`.
- AI proposes structured facts; deterministic contracts validate and mutate.
- Real World and Creation Sandbox mutable state remain isolated.

---

## Current repository boundary

Merged `main`:
`2af1ee7d5e2e3e9c0d1da8384d858880e993fb4b` — PR #347.

Current unmerged Item Edit implementation started on `test` immediately before continuity sync:
- `src/observer_sandbox/telegram_sandbox_item_edit.py`;
- `src/observer_sandbox/telegram_world_layers_item_edit_extension.py`;
- `src/observer_sandbox/telegram_world_layers.py`.

At the start of this docs sync, `test` was `6e93c66bf627d90622f4ec4a599d7cb2c3bba886`, exactly 3 commits ahead of `main` and 0 behind.

This Item Edit code is **WIP only**: no focused test run, PR CI, merge, deploy or live acceptance has occurred yet.

---

## Completed Creator foundation

Do not rebuild:
- I0 Creator authority hardening;
- I1 universal creation proposal/socket core;
- I2 isolated Creation Sandbox persistence/lifecycle;
- I2.5 isolated Sandbox clock/speed/pause/readiness/AI binding;
- I3 initial Character + Location representation proof;
- I4 Creator Studio proposal lifecycle;
- I4.1 Sandbox Character configuration UX;
- I5/I5.1 Sandbox Observer foundations;
- exact Character Manual/AI parity;
- Sandbox Character profile/edit/grade-target parity;
- explicit Real/Sandbox runtime controls;
- scoped Telegram command menu publication.

Completed Item/Location backend:
- **I5.2** reuse map;
- **I5.3** universal quantity/measurement;
- **I5.4** cross-domain grading;
- **I5.5** requirements/access;
- **I5.6** Universal Item Schema v1;
- **I5.7** single Sandbox Item materialization;
- **I5.8** atomic heterogeneous Item Batch;
- **I5.9** Item/container operations, including `update_sandbox_item()`;
- **I5.10** Universal Location Schema v1.

---

## Merged Creator Item Telegram line

The Item Creator vertical now includes:
- PR #334 — Single Item AI/Exact JSON creation UX;
- #335 — atomic Item Batch AI/Exact JSON UX;
- #336 — batch retry context, error path, typing/prompt cleanup;
- #337 — locked full-schema Creator AI form-fill contract;
- #338 — safe detailed diagnostics;
- #339 — non-stackable unused stack-module normalization;
- #340 — exact bare local `stored_in` ref -> `$ref` normalization;
- #341 — exact legacy immaterial valuation-method placeholder normalization;
- #342 — detailed Item review + txt export;
- #343 — review-back navigation regression fix;
- #344 — shared ordinary-realism/plausibility gate;
- #345 — exactly one bounded AI self-correction regeneration after deterministic rejection;
- #346 — human review wording + descriptive export filenames;
- #347 — approved Item detail/economic presentation parity + improved default economic proposals for future Items.

These are merged repo capabilities, not proof of current production deployment/live Telegram behavior.

---

## Universal Creator AI contract

All deterministic creation types follow:

`Creator intent -> complete canonical type schema/form -> AI fills form -> narrow explicitly-authorized structural canonicalization -> deterministic validation -> preview -> explicit approval -> Sandbox-only materialization`.

AI is not schema designer and not mutation authority.

Provider-form rules:
- full stable schema is passed to structured generation;
- unused arrays = `[]`;
- unknown/unused nullable slots = `null`;
- canonicalization may only remove/normalize exact contract-defined placeholders or exact structural aliases;
- no fuzzy relation inference;
- no invented missing facts;
- no validator relaxation.

Default Item realism:
- ordinary real-world physics unless target-universe rules explicitly override;
- avoid false numeric precision when null is allowed;
- deterministic cross-field plausibility checks;
- one model regeneration after first deterministic rejection using the safe rejection reason;
- second failure surfaces to Creator.

---

## Locked ontology

### Item

`Item Definition -> concrete unique instance OR stack -> physical placement/storage -> ownership/carriage/equipment -> runtime state/history`.

### Relations

- `contains` = structural/static spatial containment;
- `located_at` = dynamic physical presence;
- `stored_in` = inventory/container storage;
- `owned_by` = ownership;
- `carried_by` = carriage;
- `equipped_by` = equipped state.

Ownership does not follow from physical presence/storage. Ordinary movable inventory does not use structural `contains` merely because it is physically inside a place.

### Sandbox isolation

Creator Item/Location mutable state remains Sandbox-owned. Use `canonical_state_fingerprint()` as a high-value zero-canonical-mutation proof.

---

# CURRENT IMPLEMENTATION SLICE

## Sandbox Item Edit Telegram parity — WIP

### Goal

Allow the Creator to edit an already-approved active Sandbox Item through Telegram without creating a second Item persistence or validation path.

### Existing authority to reuse

`src/observer_sandbox/sandbox_item_operations.py::update_sandbox_item()` is the deterministic update authority.

It already protects important semantics including:
- immutable Item definition key;
- immutable instance mode;
- shared-definition protection;
- exact Item schema validation;
- relation target validation;
- storage-cycle rejection;
- existing relation/persistence synchronization.

The Telegram editor must call this service rather than duplicate its persistence logic.

### Intended WIP UX

`Sandbox World -> Items -> approved Item detail -> ✏️ Edit Item`.

On entry:
- target must be an active Sandbox Item;
- pause only that Sandbox runtime if it was running;
- remember pre-edit pause state;
- Real World is not paused or mutated.

Editor sections:
- Definition;
- Instance;
- Economic Value;
- Modules;
- Requirements;
- Relationships.

Locked fields:
- `definition.key`;
- `instance.mode`.

Complex objects/arrays may use exact JSON rather than a new ad-hoc mini-schema.

Per-field flow:
`select -> send new value -> reconstruct complete Item payload -> deterministic Item validation -> Preview -> Apply`.

Apply requirements:
- compare current payload with preview baseline and reject stale proposal;
- call existing `update_sandbox_item()`;
- keep Sandbox paused while editor remains open;
- Done Editing restores pre-edit Sandbox pause state.

### Mandatory implementation verification

Before PR:
1. Inspect the three current WIP files for correctness.
2. Verify Item detail button actually routes to the Item editor.
3. Verify Telegram free-text input is routed to `handle_sandbox_item_edit_text()` while a field is pending.
4. Verify callback ownership does not conflict with Character profile editors or Creator Studio input routing.
5. Verify reconstruction from `get_sandbox_item()` produces an exact payload acceptable to `validate_item_payload()`.
6. Verify valid scalar field editing.
7. Verify stack quantity/unit editing for stack Items.
8. Verify economic field editing, including integer minor-unit values and nullable fields.
9. Verify module object/leaf editing.
10. Verify requirements editing.
11. Verify `located_at` / `stored_in` / `owned_by` / `carried_by` / `equipped_by` edits.
12. Verify invalid relation/container/cycle edits fail without mutation.
13. Verify immutable key/mode behavior.
14. Verify shared definition edit protection.
15. Verify stale Preview rejection.
16. Verify Apply updates approved Item detail correctly.
17. Verify editor handles both initially-running and already-paused Sandbox states.
18. Verify Real World/canonical fingerprint unchanged.
19. Add focused regression tests around all high-risk boundaries.
20. Run focused verification; open PR; use final CI as repository checkpoint; merge only if green; exact-sync `test` to final `main` afterward.

No live acceptance claim before real Telegram evidence.

---

# NEXT AFTER Item Edit acceptance

## I5.11 — Sandbox Location Creation + Embedded Contents

### Objective

Materialize strict I5.10 Location into isolated Sandbox state, optionally with typed Item contents, while reusing the existing Item contracts instead of inventing a Location-only contents model.

### Empty Location path

`Location payload -> I5.10 validation -> parent/topology/economic validation -> preview -> atomic Sandbox materialization`.

### Furnished/populated path

`Location payload + typed contents manifest -> I5.10 + I5.6/I5.8 validation -> whole graph preview -> one atomic apply`.

### Required semantics

- resolved parent must be an active same-Sandbox Location;
- structural parent graph acyclic;
- structural parent uses `contains`, not `located_at`;
- explicit interface destination validates active same-Sandbox Location;
- Location access/economic/topology/environment state Sandbox-owned only;
- embedded Items invoke I5.6/I5.8 contracts;
- no arbitrary unvalidated `contents` bag;
- ordinary movable Items use `located_at` unless exact graph establishes `stored_in` another typed container;
- structural fixtures use structural containment only when explicitly composition-marked;
- validate complete Location + contents graph before writes;
- whole apply succeeds atomically or leaves zero partial graph;
- no automatic runtime readiness;
- no autonomous ticking;
- no canonical writes.

Minimum acceptance:
- empty strict Location;
- furnished Location with unique Item + stack/container relation;
- parent/interface validation;
- cycle rejection;
- invalid embedded Item -> zero graph;
- Sandbox-only economic/access/topology state;
- canonical fingerprint unchanged.

Then:
- I5.12 Location Contents Operations;
- I5.13 Character ↔ Location Binding & Runtime Readiness;
- I5.14 Item / Location Runtime Affordance Bridge;
- I5.15 Sandbox Vertical Acceptance.

---

## I6 — Transmigration boundary

Not active.

Nothing transmigrates automatically. Keep I6 planning/validation only unless explicitly expanded:
- freeze Sandbox revision;
- target-universe profile;
- dependency closure;
- compatibility checks;
- proposed canonical mutations;
- zero canonical writes on incompatibility.

Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed.

---

## Test / release policy

- smallest task-relevant tests while iterating;
- PR CI as final repository checkpoint;
- full fallback only for cross-cutting/unmapped risk;
- production-copy/runtime acceptance only when actually relevant;
- do not infer production deployment/live behavior from merge alone.

High-value invariants:
- strict schema validation;
- Sandbox/canonical isolation;
- exact relation meanings;
- shared-definition protection;
- atomic graph behavior;
- runtime readiness boundary;
- zero canonical mutation on rejected/failed paths.

---

## Exact resume point

**Finish the current Sandbox Item Edit WIP on `test` before I5.11. Merged `main` is PR #347 at `2af1ee7d5e2e3e9c0d1da8384d858880e993fb4b`. The WIP began as exactly 3 commits ahead ending at `6e93c66bf627d90622f4ec4a599d7cb2c3bba886` before continuity commits. Inspect and complete callback/text routing, deterministic `update_sandbox_item()` reuse, immutable/shared-definition/relation safeguards, Preview/stale Apply flow, Sandbox pause restoration and zero canonical mutation; add focused tests; PR/CI; merge only on green evidence. After Item Edit acceptance, resume I5.11 Location Creation + Embedded Contents.**
