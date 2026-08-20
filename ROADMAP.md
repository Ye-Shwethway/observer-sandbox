# Observer Sandbox Roadmap

Status: **ACTIVE**  
Roadmap synchronized: **2026-08-20**

## Operating principles

- Current Creator instruction, live repo contracts/config/schema, verified runtime/DB and current CI/deploy evidence outrank remembered chat context.
- AI proposes structured facts; deterministic contracts validate, derive and mutate.
- Telegram is observer/control, never simulation authority.
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.**
- Real World and Creation Sandbox mutable state remain isolated.
- Reuse established semantics through adapters instead of cloning ontologies.
- Grades are derived interpretation, not persisted competing truth.
- Item grade, actor requirement, Location access and Location operating state remain distinct.
- `runtime_ready != running`.

---

## Current repository checkpoint

### Merged `main`

`2af1ee7d5e2e3e9c0d1da8384d858880e993fb4b` — PR **#347, Align Sandbox Item details and future economic values**.

Merged Creator Item Telegram/economic refinement line after the original I5 backend foundation:

`#334 Single Item UX -> #335 Batch UX -> #336 retry/typing -> #337 full-schema AI fill -> #338 safe diagnostics -> #339 stack fill normalization -> #340 exact local stored_in ref normalization -> #341 legacy immaterial valuation-method normalization -> #342 detail review/export -> #343 review-back regression -> #344 shared ordinary-realism gate -> #345 bounded one-retry self-correction -> #346 human review/export naming -> #347 approved Item detail/economic parity`.

No merged slice in that line authorizes canonical mutation, automatic transmigration or autonomous Item execution.

### Unmerged `test` WIP

`test` = `6e93c66bf627d90622f4ec4a599d7cb2c3bba886` at the start of continuity sync, **3 commits ahead of main, 0 behind**.

WIP files:
- `src/observer_sandbox/telegram_sandbox_item_edit.py`;
- `src/observer_sandbox/telegram_world_layers_item_edit_extension.py`;
- `src/observer_sandbox/telegram_world_layers.py`.

Purpose: expose approved active Sandbox Item editing through Telegram while reusing existing `update_sandbox_item()` authority.

Status: **implementation started only**. No focused tests, PR CI, merge, deploy or live acceptance yet. Next work must finish/verify this slice before I5.11 unless the Creator explicitly redirects.

---

## Backend Creator Creation foundation

Completed and retained:

- **I5.2** Creation Contract Reuse Map.
- **I5.3** Universal Quantity / Measurement.
- **I5.4** Cross-Domain Grading.
- **I5.5** Requirements / Access.
- **I5.6** Universal Item Schema v1.
- **I5.7** Single Sandbox Item materialization.
- **I5.8** Atomic heterogeneous Item Batch.
- **I5.9** Item / Container Operations, including validated `update_sandbox_item()`.
- **I5.10** Universal Location Schema v1.

The Item Telegram vertical is now materially more complete than the old PR #332 continuity state; do not treat I5.11 as the immediate resume while an Item Edit WIP is present on `test`.

---

## Creator AI architecture lock

All current/future deterministic creation domains follow:

`Creator intent -> full canonical type form/schema -> structured AI fill -> narrow explicitly-defined canonicalization -> deterministic validation -> preview -> explicit approval -> Sandbox-only materialization`.

AI does not design schemas, repair arbitrary contradictions or directly mutate state.

Allowed narrow Item boundary canonicalizations include only explicitly locked structural cases such as:
- null/unused provider-form module slots;
- non-stackable unused `modules.stack` fill slot;
- exact bare batch-local `stored_in` token matching a declared batch ref -> explicit `$ref`;
- the exact legacy empty valuation-method placeholder for economically-immaterial/excluded/no-money fill.

No fuzzy target inference or validator weakening.

Default Item generation realism:
- ordinary real-world physics unless target-universe contract says otherwise;
- unknown nullable numbers remain null instead of false precision;
- deterministic cross-field plausibility validation;
- exactly one AI regeneration after first deterministic rejection, using the safe rejection reason;
- second rejection is surfaced.

---

## Locked ontology

### Item

`Definition -> unique instance OR stack -> physical placement/storage -> ownership/carriage/equipment -> runtime state/history`.

### Relations

- `contains` — structural/static spatial containment;
- `located_at` — dynamic physical presence;
- `stored_in` — inventory/container storage;
- `owned_by` — ownership;
- `carried_by` — carriage;
- `equipped_by` — equipped state.

Ownership never follows automatically from presence/storage. Ordinary movable inventory does not use structural `contains` merely because it is inside a place.

### Grade / access

`Item Grade != actor Requirement != Location Access != Location operating state`.

### Sandbox isolation

All Creator Item/Location mutable state remains Sandbox-owned. Continue zero-canonical-mutation acceptance with `canonical_state_fingerprint()`.

---

## Active dependency chain

Backend completed:

`I5.2 reuse -> I5.3 quantity -> I5.4 grading -> I5.5 requirements/access -> I5.6 Item schema -> I5.7 single Item -> I5.8 batch -> I5.9 Item operations -> I5.10 Location schema`.

Creator-facing Item usability refinements through PR #347 are merged.

### CURRENT — Sandbox Item Edit Telegram parity

Finish the WIP already on `test`.

Target behavior:
- approved active Sandbox Item detail exposes `✏️ Edit Item`;
- enter Item Edit Mode and pause only Sandbox runtime;
- remember and restore the previous Sandbox pause state;
- Real World stays untouched;
- reconstruct the exact current Item payload and validate it before editing;
- `definition.key` and `instance.mode` remain immutable;
- expose detailed definition, stack instance, economic policy, modules, requirements and relationships where applicable;
- complex values use exact JSON rather than a second ad-hoc schema;
- candidate change must pass `validate_item_payload()` before Preview;
- Apply must reject stale previews and reuse `update_sandbox_item()`;
- backend shared-definition protection remains authoritative;
- relation target/type/container/cycle checks remain authoritative;
- physical placement exclusivity remains authoritative;
- editor stays paused until Done Editing.

Required verification before merge:
- Item detail -> editor entry;
- callback routing;
- free-text routing;
- valid scalar edit;
- complex JSON edit;
- invalid contract rejection with no mutation;
- immutable-field behavior;
- shared-definition rejection;
- relation edit validation;
- economic edit;
- stale-preview rejection;
- Apply -> updated detail;
- pre-paused and running Sandbox pause restoration;
- canonical fingerprint unchanged.

No completion/live claim until PR/CI and, where relevant, Telegram runtime evidence.

---

## NEXT AFTER Item Edit acceptance

### I5.11 — Sandbox Location Creation + Embedded Contents

#### Objective

Materialize one strict I5.10 Location into isolated Sandbox state, optionally with typed Item contents, without creating a parallel Item model.

#### Empty path

`Location payload -> I5.10 validation -> relation/topology/economic validation -> preview -> atomic Sandbox materialization`.

#### Furnished path

`Location payload + contents manifest -> I5.10 + I5.6/I5.8 validation -> whole graph preview -> atomic apply`.

Required semantics:
- active same-Sandbox parent when resolved;
- structural parent graph acyclic;
- parent uses `contains`, not `located_at`;
- interface destinations validate active same-Sandbox Locations;
- Location access/economic/topology/environment state Sandbox-only;
- embedded Item definitions/instances/economics reuse existing Item services/storage;
- movable Items normally use `located_at`, unless exact graph says `stored_in` another typed container;
- validate whole graph before writes;
- success as one graph or zero partial state;
- no automatic runtime readiness;
- no autonomous execution;
- no canonical writes.

Then:
- **I5.12** Location Contents Operations;
- **I5.13** Character ↔ Location Binding & Runtime Readiness;
- **I5.14** Item / Location Runtime Affordance Bridge;
- **I5.15** Sandbox Vertical Acceptance.

Full Sandbox autonomous ticking remains separately unauthorized.

---

## Transmigration / Character locks

Nothing transmigrates automatically. I6 remains planning/validation only unless Creator expands scope.

Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed.

Character Manual/AI exact parity and established Sandbox profile/edit/grade-target behavior must not be weakened by Item/Location work.

---

## Runtime / deploy evidence boundary

Repository merge/CI proves repository acceptance only. Do not claim production deployment or live Telegram acceptance without separate evidence.

---

## Exact resume point

**`main` is `2af1ee7d5e2e3e9c0d1da8384d858880e993fb4b` (PR #347 merged). The current `test` line contains a 3-commit unmerged Sandbox Item Edit WIP ending at `6e93c66bf627d90622f4ec4a599d7cb2c3bba886` before continuity commits. Finish that editor first: verify callback/text routing, strict payload/update reuse, immutable fields, shared-definition/relation safeguards, preview/stale protection, pause restoration and zero canonical mutation; add focused tests; PR/CI; merge and sync only on green evidence. After Item Edit acceptance, resume I5.11 Location Creation + Embedded Contents.**
