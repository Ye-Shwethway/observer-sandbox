# Creator Creation Systems — Minimum Implementation Plan v1

Status: **APPROVED IMPLEMENTATION PLAN — ITEM EDIT PR ACTIVE**  
Date: 2026-08-20

## Objective

Build Creator Creation through bounded reusable contracts that create realistic Sandbox content without mutating canonical Real World state.

Core rules:
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.** `runtime_ready != running`.
- AI proposes structured facts; deterministic contracts validate and mutate.
- Real World and Creation Sandbox mutable state remain isolated.

---

## Current repository boundary

Merged `main`:
`2af1ee7d5e2e3e9c0d1da8384d858880e993fb4b` — PR #347.

Current Item Edit implementation is on `test` under PR **#348 — Add Sandbox Item edit Telegram routing parity**.

Repo-side routing completion now includes:
- `telegram_sandbox_item_edit.py` — strict Item editor/session, Preview/Apply, stale guard, pause restoration;
- `telegram_world_layers_item_edit_extension.py` — Item-detail launcher plus `sw:iedit:*` callback routing;
- `telegram_sandbox_item_edit_adapter.py` — pending field free-text bridge for the legacy polling contract;
- `telegram_creator_studio.py` — installs that bridge before Creator bot captures legacy hooks;
- `tests/test_telegram_sandbox_item_edit_routing.py` — focused routing/keyboard/delegation tests.

Confirmed routing-line commits include `bee7240`, `8689b8e`, `cfcda16`, and `3cb186c`, followed by continuity synchronization commits.

**Evidence boundary:** implementation + PR creation are confirmed. CI, merge, deploy and live Telegram acceptance remain pending until verified separately.

---

## Completed Creator foundation — do not rebuild

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

Merged Item Creator Telegram line through #347 covers Single/Batch creation, full-schema AI fill, safe diagnostics, narrow structural canonicalization, detailed review/export, ordinary-realism validation, one bounded self-correction retry and approved Item detail/economic presentation.

---

## Universal Creator AI contract

`Creator intent -> complete canonical type schema/form -> AI fills form -> narrow explicitly-authorized structural canonicalization -> deterministic validation -> preview -> explicit approval -> Sandbox-only materialization`.

AI is not schema designer and not mutation authority. No fuzzy relation inference, invented missing facts, arbitrary contradiction repair or validator relaxation.

Default Item realism:
- ordinary real-world physics unless target-universe rules explicitly override;
- nullable unknown numbers stay null rather than fabricated precision;
- deterministic cross-field plausibility checks;
- one model regeneration after first deterministic rejection using the safe rejection reason;
- second failure surfaces to Creator.

---

## Locked Item ontology

`Item Definition -> concrete unique instance OR stack -> physical placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Relations:
- `contains` = structural/static containment;
- `located_at` = dynamic physical presence;
- `stored_in` = inventory/container storage;
- `owned_by` = ownership;
- `carried_by` = carriage;
- `equipped_by` = equipped state.

Ownership does not follow from physical presence/storage. Ordinary movable inventory does not use structural `contains` merely because it is physically inside a place.

Creator Item/Location mutable state remains Sandbox-owned. Use `canonical_state_fingerprint()` as a high-value zero-canonical-mutation proof.

---

# CURRENT IMPLEMENTATION SLICE

## Sandbox Item Edit Telegram parity — PR #348

### Goal

Allow the Creator to edit an already-approved active Sandbox Item through Telegram without creating a second Item persistence or validation path.

### Existing authority

`src/observer_sandbox/sandbox_item_operations.py::update_sandbox_item()` remains the deterministic update authority and continues to protect:
- immutable Item definition key;
- immutable instance mode;
- shared-definition protection;
- exact Item schema validation;
- relation target validation;
- storage-cycle rejection;
- relation/persistence synchronization.

The Telegram editor reuses this service rather than duplicating persistence semantics.

### Implemented UX

`Sandbox World -> approved Item detail -> ✏️ Edit Item`.

On entry:
- target must be an active Sandbox Item;
- only the Sandbox runtime is paused if it was running;
- pre-edit pause state is remembered;
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

Complex objects/arrays use exact JSON rather than a second ad-hoc mini-schema.

Per-field flow:
`select -> next free-text value -> reconstruct complete Item payload -> deterministic validation -> Preview -> Apply`.

Routing now implemented:
- `sw:iedit:*` callbacks are routed by the world-layer extension using configured Creator identity;
- pending field free text is intercepted before the ordinary command fallback;
- slash commands deliberately remain on the normal command path;
- returned Item-editor keyboards are preserved across the existing polling loop's separate text/keyboard contract.

Apply requirements:
- compare current payload with preview baseline and reject stale proposal;
- call existing `update_sandbox_item()`;
- keep Sandbox paused while editor remains open;
- Done Editing restores pre-edit Sandbox pause state.

### Verification gates still open

PR #348 must not merge until current CI evidence confirms the relevant checks. High-value coverage remains:
1. Item detail -> editor entry and callback routing.
2. Pending field -> free-text routing and keyboard preservation.
3. Ordinary/slash command delegation remains unchanged.
4. Valid scalar and complex JSON editing.
5. Stack quantity/unit editing.
6. Economic field editing, including minor-unit integers/nullables.
7. Module/requirements/relation editing.
8. Invalid relation/container/cycle edits fail with no mutation.
9. Immutable key/mode behavior.
10. Shared-definition protection.
11. Stale Preview rejection.
12. Apply updates approved Item detail correctly.
13. Running and already-paused Sandbox states restore correctly.
14. Real World / canonical fingerprint remains unchanged.

Release sequence:
`focused tests -> PR #348 CI -> concrete-failure fixes only -> merge on green -> deployment verification if applicable -> continuity final sync -> exact main/test sync`.

No live acceptance claim before real Telegram/runtime evidence.

---

# NEXT AFTER Item Edit acceptance

## I5.11 — Sandbox Location Creation + Embedded Contents

Objective: materialize strict I5.10 Location into isolated Sandbox state, optionally with typed Item contents, while reusing existing Item contracts rather than inventing a Location-only contents model.

Empty path:
`Location payload -> I5.10 validation -> parent/topology/economic validation -> preview -> atomic Sandbox materialization`.

Furnished path:
`Location payload + typed contents manifest -> I5.10 + I5.6/I5.8 validation -> whole graph preview -> one atomic apply`.

Required semantics:
- resolved parent is active same-Sandbox Location;
- structural parent graph acyclic;
- structural parent uses `contains`, not `located_at`;
- explicit interface destinations validate active same-Sandbox Locations;
- Location access/economic/topology/environment state is Sandbox-owned only;
- embedded Items invoke I5.6/I5.8 contracts;
- no arbitrary unvalidated `contents` bag;
- ordinary movable Items use `located_at` unless exact graph establishes `stored_in` another typed container;
- validate complete Location + contents graph before writes;
- atomic whole-graph success or zero partial graph;
- no automatic runtime readiness;
- no autonomous ticking;
- no canonical writes.

Then I5.12 Location Contents Operations -> I5.13 Character ↔ Location Binding & Runtime Readiness -> I5.14 Item/Location Runtime Affordance Bridge -> I5.15 Sandbox Vertical Acceptance.

---

## I6 — Transmigration boundary

Not active. Nothing transmigrates automatically. Keep I6 planning/validation only unless explicitly expanded. Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed.

---

## Test / release policy

- smallest task-relevant tests while iterating;
- PR CI as final repository checkpoint;
- full fallback only for cross-cutting/unmapped risk;
- production-copy/runtime acceptance only when actually relevant;
- do not infer production deployment/live behavior from merge alone.

---

## Exact resume point

**Finish PR #348 before I5.11. `main` remains PR #347 at `2af1ee7d5e2e3e9c0d1da8384d858880e993fb4b`. The missing Item Edit callback and free-text wires are now implemented repo-side and focused routing tests exist. Inspect current PR #348 CI, repair only concrete failures, verify the wider affected Item/Telegram invariants, merge only on green evidence, verify deploy/live state separately if applicable, update all continuity docs with final evidence, then exact-sync `test` to `main`. After Item Edit acceptance, resume I5.11 Location Creation + Embedded Contents.**
