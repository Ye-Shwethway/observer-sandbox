# Creator Creation Systems — Minimum Implementation Plan v1

Status: **APPROVED IMPLEMENTATION PLAN — ITEM EDIT REPOSITORY ACCEPTED**  
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

PR **#348 — Add Sandbox Item edit Telegram routing parity** is merged to `main`.

Merge commit: `cee6337e9dc479988f2d3a4c78e52b70ef1b7b84`.

Final PR head: `b980c52447d84bb072764e5f29cf99d8abd933d9`.

Acceptance evidence:
- CI #1188 / run `32369393983`: **success**;
- CI selected 68 affected test files;
- targeted PR tests: **success**;
- CLI smoke init/status: **success**;
- Public Readiness Security Audit #197 / run `32369394081`: **success**.

Repo-side Item Edit routing now includes:
- `telegram_sandbox_item_edit.py` — strict Item editor/session, Preview/Apply, stale guard, pause restoration;
- `telegram_world_layers_item_edit_extension.py` — wraps actual Item `sandbox_object_view`, adds `✏️ Edit Item`, and routes canonical `sw:iedit:enter:<object_id>` / `sw:iedit:*` callbacks;
- `telegram_sandbox_item_edit_adapter.py` — pending field free-text bridge for the legacy polling contract;
- `telegram_creator_studio.py` — installs that bridge before Creator bot captures legacy hooks;
- `tests/test_telegram_sandbox_item_edit_routing.py` — focused routing/keyboard/delegation coverage.

Repository acceptance is complete. Production deployment/live Telegram acceptance remains separately evidence-gated until the applicable merge-triggered deploy/runtime result is verified.

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

Merged Item Creator Telegram line through #348 covers Single/Batch creation, full-schema AI fill, safe diagnostics, narrow structural canonicalization, detailed review/export, ordinary-realism validation, one bounded self-correction retry, approved Item detail/economic presentation, and existing Item field edit/save parity.

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

# COMPLETED SLICE

## Sandbox Item Edit Telegram parity — PR #348

### Goal

Allow the Creator to edit an already-approved active Sandbox Item through Telegram without creating a second Item persistence or validation path.

### Authority

`src/observer_sandbox/sandbox_item_operations.py::update_sandbox_item()` remains the deterministic update authority and protects:
- immutable Item definition key;
- immutable instance mode;
- shared-definition protection;
- exact Item schema validation;
- relation target validation;
- storage-cycle rejection;
- relation/persistence synchronization.

The Telegram editor reuses this service rather than duplicating persistence semantics.

### Accepted UX / routing

`Sandbox World -> approved Item detail -> ✏️ Edit Item`.

On entry:
- target is an active Sandbox Item;
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

Routing contract:
- Item detail is the established `sandbox_object_view`;
- launcher callback is `sw:iedit:enter:<object_id>`;
- remaining `sw:iedit:*` callbacks route using configured Creator identity;
- pending field free text is intercepted before ordinary command fallback;
- slash commands deliberately remain on the normal command path;
- returned Item-editor keyboards are preserved across the existing polling loop's separate text/keyboard contract.

Apply requirements:
- compare current payload with preview baseline and reject stale proposal;
- call existing `update_sandbox_item()`;
- keep Sandbox paused while editor remains open;
- Done Editing restores pre-edit Sandbox pause state.

### Acceptance evidence

PR #348 repository gates are closed green:
1. callback routing contract ✅
2. free-text routing and keyboard preservation ✅
3. command delegation compatibility ✅
4. affected 68-file targeted regression scope ✅
5. CLI init/status smoke ✅
6. public-readiness security audit ✅
7. mergeability and merge ✅

Deployment remains separate:
- `deploy.yml` applies to `main` pushes touching `src/**` when VPS deployment is enabled;
- deployment/runtime/live Telegram evidence must be checked separately before calling the slice live.

---

# NEXT AFTER DEPLOY/RUNTIME VERIFICATION

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
- do not infer production deployment/live behavior from merge alone;
- continuity docs are updated at material checkpoints and exact-synced across persistent branches after acceptance.

---

## Exact resume point

**PR #348 is merged at `cee6337e9dc479988f2d3a4c78e52b70ef1b7b84` after CI #1188 and Security Audit #197 passed. Sandbox Item Edit Telegram parity is repository-accepted. Verify the applicable merge-triggered deploy/runtime evidence next; then finish continuity PR/main-test exact sync. Once production evidence is green, start I5.11 Location Creation + Embedded Contents.**
