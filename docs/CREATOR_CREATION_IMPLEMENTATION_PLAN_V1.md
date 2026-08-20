# Creator Creation Systems — Minimum Implementation Plan v1

Status: **APPROVED IMPLEMENTATION PLAN — ACTIVE ITEM/LOCATION FOUNDATION**  
Date: 2026-08-20

## Objective

Build Creator Creation through small runnable contracts that can create realistic Sandbox content without mutating the canonical Real World.

Current dependency chain:

`strict creation contracts -> quantity/measurement -> grading -> requirements/access -> Item schema -> Item creation/batch/operations -> Location schema -> Location contents -> Character/Location binding -> runtime affordances -> vertical acceptance`

Reuse existing inventory, valuation, grading, world-location and Sandbox lifecycle semantics. Do not build parallel Sandbox-only ontologies where the same concept already exists.

---

## Completed prerequisites

Already merged and not to be rebuilt:
- I0 Creator authority hardening;
- I1 universal creation proposal/socket core;
- I2 isolated Creation Sandbox persistence/lifecycle;
- I2.5 isolated Sandbox clock/speed/pause/readiness/AI binding;
- I3 initial Character + Location representation proof;
- I4 Creator Studio proposal lifecycle;
- I4.1 Sandbox Character configuration UX;
- I5/I5.1 Sandbox Observer foundations;
- exact Character AI schema generation and deterministic validation;
- exact Manual Character creation parity;
- Sandbox Character profile/edit/grade-target parity;
- explicit Real/Sandbox runtime controls;
- scoped Telegram command menu publication.

Character remains the strictness exemplar: Manual and AI converge on one deterministic contract; runtime/derived state is not Creator seed ownership.

---

## Completed current foundation slices

### I5.2 — Creation Contract Audit & Reuse Map — COMPLETE

Contract:
`docs/CREATION_CONTRACT_REUSE_MAP_V1.md`.

Locked decisions:
- keep generic Creation proposal envelope;
- add exact type-specific schemas beneath it;
- reuse Creation Sandbox lifecycle/isolation;
- keep Item definition / concrete instance-or-stack / storage / ownership separate;
- reuse world relation meanings;
- reuse valuation/grading/access foundations through adapters;
- later reconcile Sandbox prototype `located_in` to canonical dynamic `located_at` semantics.

### I5.3 — Universal Quantity & Measurement Contract — COMPLETE

PR #324 merge:
`a4abcbbcb932711bcf164d20bb977314afad5550`

Contract:
`docs/UNIVERSAL_QUANTITY_MEASUREMENT_CONTRACT_V1.md`.

Implementation:
`src/observer_sandbox/physical_quantity.py`.

Acceptance:
- CI #1155 SUCCESS;
- 22 targeted tests passed;
- CLI init/status green;
- schema 21 healthy.

Provides normalized mass/length/area/volume truth with deterministic conversion and Imperial-default presentation. Existing Character body fields and inventory-stack persistence remain unchanged.

### I5.4 — Universal Cross-Domain Grade Contract — COMPLETE

PR #325 merge:
`980a752160a48144ef91bf800c4f4ab8fc5bc98e`

Contract:
`docs/UNIVERSAL_CROSS_DOMAIN_GRADING_CONTRACT_V1.md`.

Acceptance:
- CI #1157 SUCCESS;
- 189 targeted grading/profile/runtime regression tests passed;
- CLI init/status green;
- schema 21 healthy.

Adds:
- deterministic E→XX ordering;
- scheme domain/dimension metadata;
- optional read-time GradeProfile;
- Item resistance-load exemplar;
- Location completeness exemplar using existing L0-L4 contract.

Grade remains derived interpretation.

### I5.5 — Universal Requirement & Access Contract — COMPLETE

PR #326 merge:
`2372a3a32f3b400a029317174fcf7260fee7f1f3`

Contract:
`docs/UNIVERSAL_REQUIREMENT_ACCESS_CONTRACT_V1.md`.

Implementation:
`src/observer_sandbox/requirements.py`.

Acceptance:
- CI #1158 SUCCESS;
- 22 targeted tests passed;
- CLI init/status green;
- schema 21 healthy.

Provides:
- typed minimum-grade/raw-value/skill/item/equipment/ownership/residency/authorization/state predicates;
- nested `all` / `any` composition;
- structured unmet-requirement output;
- public/owner-or-resident/authorized/restricted/requirement-based access policies;
- separate current operating-state evaluation.

Core lock:

`Item Grade != interaction Requirement Grade != Location Access != Location operating state`.

---

# Active implementation slices

## I5.6 — Universal Item Schema v1 — NEXT

### Objective

Define one strict exact Item contract used by Manual creation, AI generation, single creation, batch creation and later Location embedded contents.

### Dependency inputs

Reuse:
- `docs/INVENTORY_ITEM_ARCHITECTURE.md`;
- `src/observer_sandbox/inventory.py` semantics;
- I5.3 normalized physical quantities;
- I5.4 registered grading;
- I5.5 requirement contracts;
- `src/observer_sandbox/economic_value.py` classifications/treatments;
- generic Creation proposal envelope;
- isolated Creation Sandbox lifecycle.

### Semantic model

Do not flatten the Item into one ambiguous object.

Canonical conceptual chain:

`Item Definition -> concrete unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Definition-owned facts and concrete-instance facts must be distinguishable even if a Creator Studio draft presents them together.

### Exact-schema rule

Use:

`strict core + strict conditional modules`.

The validator determines the allowed exact field set from registered modules. Unknown AI-generated fields fail validation.

Manual and AI output must normalize to the same schema.

### Core fields

The exact final field list is owned by I5.6 implementation, but must cover at minimum:
- stable/display identity;
- Item kind / semantic family;
- stackability / unique semantics;
- description/provenance as appropriate;
- capability/module declarations;
- physical properties through I5.3 quantities where applicable;
- economic-value policy;
- grade inputs/scheme references where applicable;
- use/action requirement declarations where applicable;
- optional storage/container capability;
- lifecycle-safe metadata required for Sandbox materialization.

### Conditional modules

Prefer capability-driven modules over unrelated global fields.

Candidate modules include:
- physical dimensions/mass;
- stackable stock/unit semantics;
- container capacity;
- training/resistance load;
- nutrition/consumable effects;
- equipment/wearable semantics;
- tool/electronic/medical capabilities;
- fixture/fixed-mobility semantics;
- durability/condition only when needed by represented behavior.

Do not include future depth merely because it may someday exist.

### Economic policy

Every represented Item must make an explicit applicable value-policy choice using existing semantics:
- standalone asset;
- component;
- consumable stock;
- resource proxy;
- economically immaterial;
with compatible net-worth treatment.

Sandbox creation stores Sandbox-owned staged policy; it must not write canonical economic value/net-worth tables.

### Grade policy

When an Item dimension is gradeable:
- raw physical/specification state is authoritative;
- grade derives from a registered scheme;
- AI does not author the grade as source truth.

### Requirement policy

Any actor/item/state prerequisite uses the I5.5 typed requirement contract.

Do not copy Item grade into an interaction requirement.

### Acceptance

Prove at minimum:
- exact schema rejects unknown fields;
- required core fields cannot be omitted;
- conditional module fields are required/forbidden correctly;
- unique and stackable semantics cannot conflict;
- normalized quantities are unit-system independent;
- economic policy is mandatory and internally coherent;
- derived grade is deterministic where configured;
- requirement contract remains separate;
- Manual-shaped and AI-shaped payloads validate identically;
- no canonical DB writes.

Do not add Telegram Item creation UI in I5.6.

---

## I5.7 — Sandbox Item Creation v1: Single

### Objective

Create one validated Item into isolated Sandbox state.

### Flow

`Manual or AI intent -> exact Item schema -> preview -> validate -> Creator approve -> Sandbox materialization`.

### Rules

- single Item uses the same service boundary as a batch of one;
- AI output never writes DB directly;
- Sandbox definition/instance/stack state mirrors canonical semantics without canonical table mutation;
- economic policy materializes in Sandbox-owned state;
- explicit placement/ownership relations only when supplied/valid;
- revision/provenance/audit evidence required.

### Acceptance

Create at least:
- one unique movable Item;
- one fixture-like Item;
- one stackable stock exemplar;
without canonical fingerprint change.

---

## I5.8 — Sandbox Item Batch Creation v1

### Objective

Create heterogeneous Item sets atomically.

### Rules

- every member is an exact I5.6 Item proposal;
- batch orchestration never relaxes member validation;
- support batch-internal stable references;
- validate dependencies/relations/value policies before write;
- preview complete batch;
- all-or-nothing apply;
- failure leaves zero partial activation.

Single creation remains batch size 1 conceptually.

---

## I5.9 — Sandbox Item / Container Operations

Provide generic:
- browse/inspect;
- edit through validated schema;
- move/location assignment;
- `stored_in`;
- ownership;
- carry/equip semantics where supported;
- stack quantity changes;
- archive/delete with explicit dependency handling.

Do not silently cascade-delete movable/owned contents merely because a container disappears.

---

## I5.10 — Universal Location Schema v1

### Objective

Replace the current Creator Location prototype with a strict spatial-container schema.

Reuse:
- `WORLD_LOCATION_NODE_MODEL.md`;
- `WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`;
- `WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`;
- I5.3 quantities;
- I5.4 grading;
- I5.5 access/requirements;
- economic policy semantics.

Minimum strict domains:
- identity/kind;
- structural parent;
- extent/exposure where known;
- boundary/interfaces/topology where represented;
- access policy;
- operating state;
- facilities/capabilities/resources;
- environment where represented;
- economic policy;
- provenance.

Unknown precision stays unknown.

Target for a runtime-ready Character should be a **usable** represented place, conceptually at least L3, unless a later explicit readiness rule chooses otherwise.

---

## I5.11 — Location Creation + Embedded Contents

Support:

### Empty Location

Create the spatial container, approve/activate, then add contents later.

### Furnished/populated Location

Location proposal carries a typed contents manifest whose new Items are exact I5.6/I5.8 proposals.

Validate the whole graph before write and apply atomically.

Location creation must call Item creation contracts, not duplicate them.

---

## I5.12 — Location Contents Operations

Support:
- Add Existing Item;
- Create Item;
- Create Item Batch;
- Remove/Move Item;
- Create Child Location.

Relations remain semantically distinct:
- structural `contains`;
- dynamic `located_at`;
- inventory `stored_in`;
- `owned_by`;
- `carried_by`;
- `equipped_by`.

---

## I5.13 — Character ↔ Location Binding & Runtime Readiness

Reconcile Sandbox prototype `located_in` to canonical semantic `located_at` through Sandbox-owned adapters/persistence.

Readiness target:

`active Sandbox Character + active usable Sandbox Location + represented runtime/action options + explicit cognition AI binding + configured Sandbox clock -> runtime_ready`.

Missing dependencies fail closed with exact reasons.

---

## I5.14 — Item / Location Runtime Affordance Bridge

Derive executable options from represented machine-readable facts:
- Item/fixture capabilities;
- resources;
- environment/terrain;
- Location capabilities;
- explicit requirements/access.

Cognition may choose legal options but may not invent missing equipment/resources/doors/actions.

---

## I5.15 — Sandbox Vertical Acceptance

Prove one complete isolated vertical:
- exact Character;
- exact usable Location;
- typed Item contents;
- correct relations;
- economic policies;
- binding/readiness;
- deterministic legal options;
- canonical fingerprint unchanged.

Full autonomous Sandbox ticking is still a separate authorization boundary.

---

## I6 — Transmigration planning boundary

Not the active next slice.

When resumed, keep planning/validation only unless Creator explicitly expands scope:
- freeze Sandbox revision;
- select target-universe profile;
- dependency closure;
- compatibility checks;
- proposed canonical mutations;
- zero canonical writes on incompatibility.

No automatic Character promotion.

---

## Test policy

During each slice:
- run smallest relevant tests;
- PR CI is final checkpoint;
- targeted CI is preferred when selector can prove scope;
- full fallback only for cross-cutting/unmapped risk;
- production-copy acceptance only for stateful/migration/runtime risk that actually needs it.

High-value continuing invariants:
- strict schema validation;
- canonical/Sandbox isolation;
- value/grade/requirement separation;
- relation semantics;
- atomic batch behavior;
- readiness gates;
- zero canonical mutation on failed creation/compatibility paths.

---

## Exact resume point

**I5.2 through I5.5 are merged and green. Latest implementation merge is PR #326 at `2372a3a32f3b400a029317174fcf7260fee7f1f3`; CI #1158 passed 22 targeted tests with CLI init/status green and schema 21 healthy. Next slice is I5.6 Universal Item Schema v1. Implement the exact type-specific Item schema/validator first; do not add Telegram Item creation UI yet and do not mutate canonical Item/inventory/economic state.**
