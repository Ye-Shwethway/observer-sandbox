# Observer Sandbox Roadmap

Status: **ACTIVE**  
Roadmap synchronized: **2026-08-20**

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema, verified runtime/DB and current CI/deploy evidence outrank remembered chat context.
- AI proposes structured facts; deterministic contracts validate, derive and mutate.
- Telegram is observer/control, never simulation authority.
- Creator-approved state outranks ordinary seed/default refresh.
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.** Creation, runtime readiness and runtime execution are separate boundaries.
- Real World and Creation Sandbox mutable state remain isolated.
- Reuse established Real World semantics through adapters instead of creating Sandbox-only duplicate ontologies.
- Grades are derived interpretation, not persisted competing truth.
- Item grade, actor interaction requirement, Location access and Location operating state are distinct concepts.

---

## Current repository checkpoint

Latest merged implementation checkpoint:

### PR #326 — I5.5 Universal Requirement & Access Foundation

Merge:
`2372a3a32f3b400a029317174fcf7260fee7f1f3`

Evidence:
- CI #1158 — **SUCCESS**;
- targeted 2 test files;
- **22 passed**;
- CLI init/status — **SUCCESS**;
- fresh DB healthy, schema version 21;
- no DB migration;
- no canonical world mutation.

I5.5 added:
- strict typed requirement evaluation;
- explicit `all` / `any` composition;
- minimum-grade/raw-value/skill/item/equipment/ownership/residency/authorization/state predicates;
- separate Location access-policy evaluation;
- separate operating-state composition;
- structured fail-closed unmet-requirement evidence.

Access modes currently provided by the foundation contract:
- `public`;
- `owner_or_resident`;
- `authorized`;
- `restricted`;
- requirement-based.

Operating state remains separate:
- `open`;
- `closed`;
- `locked`;
- `blocked`.

---

## Newly completed Item/Location foundation chain

### I5.2 — Creation Contract Audit & Reuse Map — COMPLETE

Canonical contract:
`docs/CREATION_CONTRACT_REUSE_MAP_V1.md`.

Locked reuse boundaries:
- generic creation proposal envelope remains reusable;
- strict type-specific validators sit under that envelope;
- Creation Sandbox lifecycle/isolation remains reusable;
- universal Item definition / concrete instance or stack / storage / ownership remain distinct;
- existing inventory, valuation, grading and spatial semantics are reused rather than cloned;
- Sandbox `located_in` is prototype compatibility semantics and must later reconcile to canonical dynamic `located_at` through a Sandbox adapter.

### I5.3 — Universal Quantity & Measurement Contract — COMPLETE

PR #324 merge:
`a4abcbbcb932711bcf164d20bb977314afad5550`

Evidence:
- CI #1155 — **SUCCESS**;
- targeted **22 passed**;
- CLI init/status green;
- schema 21 healthy.

Canonical contract:
`docs/UNIVERSAL_QUANTITY_MEASUREMENT_CONTRACT_V1.md`.

Implementation:
`src/observer_sandbox/physical_quantity.py`.

Rules:
- normalized presentation-independent physical truth;
- mass -> kg, length -> m, area -> m², volume -> m³ internally;
- deterministic conversion;
- Imperial default Creator presentation (`lb`, `in`, `ft²`, US gal);
- Metric display supported without state mutation;
- existing Character body storage and inventory stack persistence remain unchanged.

### I5.4 — Universal Cross-Domain Grade Contract — COMPLETE

PR #325 merge:
`980a752160a48144ef91bf800c4f4ab8fc5bc98e`

Evidence:
- CI #1157 — **SUCCESS**;
- targeted **189 passed**;
- existing Character/Profile grading regressions green;
- CLI init/status green;
- schema 21 healthy.

Canonical contract:
`docs/UNIVERSAL_CROSS_DOMAIN_GRADING_CONTRACT_V1.md`.

Implementation extends:
`src/observer_sandbox/grading.py`.

Locked vocabulary:
`E < D < C < B < A < S < SS < SSS < X < XX`.

New foundation includes:
- deterministic grade ordering/comparison;
- scheme domain/dimension metadata;
- optional read-time multi-dimension GradeProfile;
- explicit composite-only overall grade;
- Item `resistance_load` exemplar derived from normalized physical mass;
- Location completeness exemplar reusing existing L0-L4 spatial completeness contract.

Important distinction:
- a 55 lb dumbbell may derive S **Item resistance-load grade**;
- that does not imply S Character Strength to use it;
- Location completeness grade does not grant access.

### I5.5 — Universal Requirement & Access Contract — COMPLETE

Canonical contract:
`docs/UNIVERSAL_REQUIREMENT_ACCESS_CONTRACT_V1.md`.

Implementation:
`src/observer_sandbox/requirements.py`.

Core separation:

`represented state -> derived grade`  
`interaction -> explicit actor/item/state requirement`  
`Location -> explicit access policy`  
`Location current state -> operating/open-state check`.

No automatic conversion from Item grade to actor requirement and no automatic conversion from Location grade to authorization.

---

## Current active dependency chain

Completed:

`I5.2 reuse audit -> I5.3 quantity/measurement -> I5.4 cross-domain grading -> I5.5 requirements/access`

Next:

`I5.6 strict Item schema -> I5.7 single Item creation -> I5.8 batch Item creation -> I5.9 Sandbox Item/container operations -> I5.10 strict Location schema -> I5.11 Location + embedded contents -> I5.12 contents operations -> I5.13 Character/Location binding -> I5.14 runtime affordances -> I5.15 vertical acceptance`.

---

## I5.6 — Universal Item Schema v1 — NEXT

Goal: define the exact typed Item contract consumed identically by Manual and AI creation.

The schema must preserve the existing universal Item architecture:

`universal definition -> concrete unique instance OR stack -> physical placement/storage -> ownership -> capabilities/effects -> economic policy`.

Minimum design requirements:
- strict exact registered core fields;
- strict conditional modules selected by Item kind/capabilities;
- no arbitrary AI-created keys;
- unique/non-stackable versus stackable semantics explicit;
- normalized physical quantities from I5.3;
- gradeable dimensions reference registered I5.4 schemes only;
- action/use requirements use I5.5, never copied from Item grade;
- economic value policy reuses existing classification/treatment semantics;
- storage/current-location/ownership remain relation facts, not definition identity;
- Sandbox staging remains isolated from canonical `entity_definitions`, `entities`, `inventory_stacks`, `relations`, value tables and net-worth state.

Representative categories should be modeled as strict modules rather than separate incompatible systems, including:
- ordinary movable object;
- fixed fixture;
- training/equipment object;
- consumable/resource stock;
- container object;
- tool/electronic/medical or other capability-driven variants when represented.

Do not implement Item creation UI before the Item schema/validator is deterministic.

---

## Item creation direction

### I5.7 — Single Item Creation

One Item is a batch of one at the service boundary.

Manual and AI paths must converge on one exact Item validator and one Sandbox apply boundary.

### I5.8 — Batch Item Creation

Batch may be heterogeneous but every member remains an exact Item proposal.

Required behavior:
- validate all members;
- resolve batch-internal references;
- preview complete graph;
- approval boundary;
- atomic apply/rollback;
- no partial activation if any member fails.

### I5.9 — Sandbox Item / Container Operations

Provide generic inspect/edit/move/store/own/equip/quantity/archive/delete semantics in Sandbox-owned state.

Do not use structural `contains` for ordinary mutable inventory storage.

---

## Location creation direction

Canonical spatial definition remains:

> **Location = an identifiable spatial container with extent, contents, boundary/interface semantics, local state and explicit relationships to surrounding space.**

### I5.10 — Universal Location Schema v1

Replace the current name-centric arbitrary-properties Creator Location prototype with a strict spatial-container contract.

Must preserve:
- stable identity;
- kind/classification;
- one canonical structural parent where applicable;
- extent/exposure where known;
- boundaries/interfaces/topology;
- access and operating state;
- facilities/capabilities/resources;
- local environment where represented;
- economic/value policy;
- provenance;
- unknown precision remains unknown.

### I5.11 — Location Creation + Embedded Contents

A Location may be created empty or with a typed contents manifest.

Embedded new Items must invoke the same I5.6/I5.8 Item contracts; Location generation must not invent a parallel contents schema.

### I5.12 — Location Contents Operations

Support:
- add existing Item;
- create Item;
- create Item batch;
- remove/move Item;
- add child Location.

Relation semantics remain distinct:
- `contains` structural/static containment;
- `located_at` dynamic physical presence;
- `stored_in` inventory storage;
- `owned_by` ownership;
- `carried_by` carriage;
- `equipped_by` equipped state.

---

## Runtime closure direction

### I5.13 — Character ↔ Location Binding & Runtime Readiness

Reconcile Sandbox prototype `located_in` toward the canonical `located_at` semantic through Sandbox-owned persistence/adapters.

A Character must not be considered meaningfully runnable merely because a Location name exists.

Target minimum:
`active Character + usable active Location + runtime options + cognition AI binding + configured Sandbox clock -> runtime_ready`.

### I5.14 — Item / Location Runtime Affordance Bridge

Location labels alone do not grant executable actions.

Deterministic options should derive from represented:
- fixtures/equipment;
- Item capabilities;
- resources;
- environment/terrain;
- Location capabilities;
- explicit requirements/access.

### I5.15 — Sandbox Vertical Acceptance

Prove one complete isolated vertical:
- strict Character;
- strict usable Location;
- typed Items/contents;
- correct relations;
- explicit economic policies;
- Character binding;
- deterministic legal options/readiness;
- zero canonical mutation.

Full autonomous Sandbox ticking remains separate unless explicitly authorized.

---

## Existing Creator Character checkpoint

Character creation remains the strictness exemplar.

Current established behavior includes:
- exact AI creation-owned profile schema;
- sparse canonical skills;
- registered data types authoritative;
- exact Manual/AI field-set parity;
- manual section editing remains in context;
- accepted input prompt cleanup;
- Sandbox Character profile browsing/editing/grade-target parity;
- Real/Sandbox runtime controls isolated;
- scoped Telegram command menus auto-published from final role-aware help contract.

Do not loosen Character exactness while adding Item/Location schemas.

---

## Staging & transmigration locks

Lifecycle direction remains:

`Draft -> Sandbox Approved -> Sandbox Active -> Tested/Revised -> Ready for Transmigration -> Canonical Approved -> Canonical Active`.

Nothing transmigrates automatically.

Supernatural/impossible systems may be Sandbox-valid but incompatible with the current realistic Real World and valid in a future universe profile.

I6 remains planning/validation only when resumed unless the Creator explicitly changes scope.

Adrian Vale remains Sandbox-only and must not be transmigrated as a side effect of Item/Location work.

---

## Second-character gate

No second real production Character may be activated/transmigrated before the established gates remain satisfied, including MIND-F2..F7, relationship adaptation, foundation review and explicit Creator approval.

Sandbox Characters do not violate this gate.

---

## Runtime / production evidence boundary

Repository and PR-CI evidence is verified through PR #326.

Source changes in I5.3-I5.5 are foundation code, but this roadmap does **not** infer production deployment from merge alone. Verify push/deploy/boot evidence separately before making live-runtime claims.

Full Sandbox autonomous ticking remains **not implemented**. `runtime_ready != running` remains locked.

---

## Exact resume point

**PR #326 is merged at `2372a3a32f3b400a029317174fcf7260fee7f1f3`; CI #1158 succeeded with 22 targeted tests, CLI init/status green and schema 21 healthy. I5.2 reuse mapping, I5.3 quantity/measurement, I5.4 cross-domain grading and I5.5 requirements/access are complete. Next implementation slice: I5.6 Universal Item Schema v1. Build an exact typed Item contract that reuses inventory definition/instance/stack semantics, I5.3 physical quantities, I5.4 registered grading, I5.5 requirements and existing economic-value policy semantics. Do not add Item Telegram creation UI before the schema/validator is deterministic; do not mutate canonical Real World Item/inventory/economic state; do not transmigrate Adrian or another Character.**
