# Creator Creation Systems — Minimum Implementation Plan v1

Status: **APPROVED IMPLEMENTATION PLAN — ACTIVE ITEM/LOCATION FOUNDATION**  
Date: 2026-08-20

## Objective

Build Creator Creation through bounded, reusable contracts that can create realistic Sandbox content without mutating the canonical Real World.

Current dependency chain:

`strict creation contracts -> quantity/measurement -> grading -> requirements/access -> Item schema -> Item creation/batch/operations -> Location schema -> Location creation/contents -> Character/Location binding -> runtime affordances -> vertical acceptance`

Reuse existing inventory, valuation, grading, world-location and Sandbox lifecycle semantics. Do not build parallel Sandbox-only ontologies where the same concept already exists.

Core operating rules:
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.**
- `runtime_ready != running`.
- AI proposes structured facts; deterministic contracts validate and mutate.
- Real World and Creation Sandbox mutable state remain isolated.

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

# Completed Creator Item / Location foundation

## I5.2 — Creation Contract Audit & Reuse Map — COMPLETE

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

## I5.3 — Universal Quantity & Measurement Contract — COMPLETE

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

Provides normalized SI physical truth for mass/length/area/volume with deterministic conversion. Creator-facing default remains Imperial; display conversion does not mutate truth.

## I5.4 — Universal Cross-Domain Grade Contract — COMPLETE

PR #325 merge:
`980a752160a48144ef91bf800c4f4ab8fc5bc98e`

Contract:
`docs/UNIVERSAL_CROSS_DOMAIN_GRADING_CONTRACT_V1.md`.

Acceptance:
- CI #1157 SUCCESS;
- 189 targeted tests passed;
- CLI init/status green;
- schema 21 healthy.

Shared grade order:
`E < D < C < B < A < S < SS < SSS < X < XX`.

Existing Character schemes remain compatible. Item resistance-load and Location completeness remain explicit separate domains/dimensions. Grade is derived interpretation, not source truth.

## I5.5 — Universal Requirement & Access Contract — COMPLETE

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

Provides typed requirements with nested `all` / `any`, including grade/value/skill/Item/equipment/ownership/residency/authorization/state predicates. Location access policy remains separate from current operating state.

Core lock:
`Item Grade != interaction Requirement Grade != Location Access != Location operating state`.

## I5.6 — Universal Item Schema v1 — COMPLETE

PR #328 merge:
`5820aad0f4abf5efb4b352071cbb67ee8056071b`

Acceptance:
- CI #1159 SUCCESS;
- 74 passed / 11 selected files.

Contract:
`docs/UNIVERSAL_ITEM_SCHEMA_V1.md`

Implementation:
`src/observer_sandbox/item_creation_schema.py`

Exact Item contract now distinguishes:
- stable definition facts;
- unique or stack concrete instance intent;
- strict conditional modules;
- normalized physical quantities;
- economic policy;
- explicit requirements;
- relation intent.

Bounded v1 modules:
- physical;
- stack;
- nutrition;
- container;
- resistance training.

Unknown fields/modules/capabilities fail closed.

## I5.7 — Sandbox Item Creation v1: Single — COMPLETE

PR #329 merge:
`74d83bc6d50a61a76becb41bc53d6cc65b354257`

Acceptance:
- CI #1160 SUCCESS;
- 89 passed / 17 selected files.

Added isolated Sandbox Item definition, concrete instance/stack and economic-policy persistence plus atomic materialization. Relations validate active same-Sandbox targets. Canonical fingerprint remains unchanged.

## I5.8 — Sandbox Item Batch Creation v1 — COMPLETE

PR #330 merge:
`716b56e64fa106f633c13c55de9211a7a67e5c8b`

Acceptance:
- CI #1161 SUCCESS;
- 88 passed / 15 selected files.

Single Item now uses the same batch-size-one service path. Batch creation supports write-free preview, forward `$ref` for batch-local `stored_in`, container validation, duplicate/unknown/self/cycle rejection, same-key semantic consistency and all-or-nothing apply.

## I5.9 — Sandbox Item / Container Operations — COMPLETE

PR #331 merge:
`d4b60e5fdd18706cbd60da8cdde556226c826efe`

Acceptance:
- CI #1162 SUCCESS;
- 99 passed / 18 selected files.

Supports browse/inspect, validated edit, move/store/own/carry/equip, stack quantity, archive/delete and dependency reporting.

Important locks:
- one physical placement mode at a time;
- ownership remains orthogonal to placement/storage;
- shared definitions cannot be rewritten through one instance;
- incoming dependencies require explicit detach before archive/delete;
- dependent Items survive detach;
- Sandbox reset clears Item definitions as well as object-owned Item state.

## I5.10 — Universal Location Schema v1 — COMPLETE

PR #332 merge:
`d670ac8e7a1ee3beaa6001011d8b04383c39533c`

Final PR head:
`aaf17efb4e142a5b3691bbd1eba1c9502c39143b`

Acceptance:
- CI #1164 SUCCESS;
- 126 passed / 22 selected files;
- CLI init/status green;
- fresh DB healthy;
- schema 21.

Contract:
`docs/UNIVERSAL_LOCATION_SCHEMA_V1.md`

Implementation:
`src/observer_sandbox/location_creation_schema.py`

Strict Location domains:
- identity/kind;
- structural parent + exposure;
- optional normalized extent;
- access policy + separate operating state;
- explicit spatial interfaces/topology;
- machine-readable facilities/resources/capabilities;
- minimal represented environment;
- optional economic policy;
- provenance.

Unknown spatial precision remains unknown/null. Structural parentage does not imply traversal. L0-L4 completeness and Location grade are derived interpretation only and do not grant authorization or runtime readiness.

---

# Locked ontology

## Item ontology

`Item Definition -> concrete unique instance OR stack -> physical placement/storage -> ownership/carriage/equipment -> runtime state/history`

Do not flatten these layers into one arbitrary properties bag.

## Relation ontology

- `contains` = structural/static spatial containment;
- `located_at` = current dynamic physical presence;
- `stored_in` = inventory/container storage;
- `owned_by` = ownership;
- `carried_by` = carriage;
- `equipped_by` = equipped state.

Ownership never follows automatically from location/storage. Ordinary movable inventory must not use structural `contains` merely because it is inside a place/container.

## Sandbox isolation

Creator Item/Location mutable state remains Sandbox-owned. Do not write Sandbox creation into canonical Real World entity/item/inventory/economic/runtime state.

Continue using `canonical_state_fingerprint()` as a high-value zero-mutation acceptance proof.

---

# Active implementation slices

## I5.11 — Sandbox Location Creation + Embedded Contents — NEXT

### Objective

Materialize the strict I5.10 Location contract into isolated Sandbox state, optionally with typed Item contents, while reusing the existing Item contracts rather than inventing a parallel Location-contents model.

### Empty Location path

`Location payload -> I5.10 validation -> parent/topology/economic validation -> preview -> atomic Sandbox materialization`

### Furnished / populated Location path

`Location payload + typed contents manifest -> I5.10 validation + I5.6/I5.8 Item validation -> whole-graph preview -> one atomic apply`

### Required semantics

- resolved `parent_ref` must identify an active Location in the same Sandbox;
- structural parent graph must remain acyclic;
- structural parent relation uses `contains`, not `located_at`;
- explicit interface destinations must validate active same-Sandbox Locations when resolved;
- Location access/economic/topology/environment state persists only in Sandbox-owned storage;
- embedded new Items must invoke I5.6/I5.8 Item contracts;
- Location generation must not invent an arbitrary unvalidated `contents` properties bag;
- ordinary movable/unique Items physically present in the Location use `located_at` unless their exact manifest instead establishes `stored_in` another typed container;
- structural fixtures may use structural containment only when the composition contract explicitly classifies them that way;
- Item definitions/instances/economics continue through the existing Sandbox Item services/storage;
- validate the complete Location + contents graph before writes;
- apply the complete graph transactionally: success as one graph or zero partial state;
- creation does not automatically grant `runtime_ready`;
- no autonomous Sandbox ticking is introduced;
- no canonical Real World writes.

### Minimum acceptance target

Prove:
- one empty strict Location;
- one furnished Location with a unique Item plus stack/container relationship;
- valid structural parent materialization;
- parent-cycle rejection;
- interface-target validation;
- invalid embedded Item leaves zero new Location/Item graph;
- economic/access/topology state remains Sandbox-only;
- canonical fingerprint unchanged.

Do not add broad Telegram Location authoring UX before this materialization/composition contract is deterministic.

---

## I5.12 — Location Contents Operations

Support:
- add existing Item;
- create Item;
- create Item batch;
- remove/move Item;
- create child Location.

Preserve relation distinctions and explicit dependency handling.

---

## I5.13 — Character ↔ Location Binding & Runtime Readiness

Reconcile legacy Sandbox Character `located_in` toward canonical semantic `located_at` through Sandbox-owned adapters/persistence.

A Location name alone is insufficient. Target readiness should require an active usable represented Location, conceptually at least L3 unless the implemented contract establishes a narrower justified rule, plus explicit runtime dependencies such as cognition AI binding and configured Sandbox clock.

Missing dependencies fail closed with exact reasons.

---

## I5.14 — Item / Location Runtime Affordance Bridge

Derive executable legal options from represented machine-readable facts:
- Item/fixture capabilities;
- resources;
- environment/terrain;
- Location capabilities;
- explicit access and requirements.

Cognition may choose among legal options but may not invent missing equipment, resources, doors or actions from Location names or narrative plausibility.

---

## I5.15 — Sandbox Vertical Acceptance

Prove one complete isolated vertical:
- exact Character;
- exact usable Location;
- typed Item contents;
- correct relation semantics;
- economic policies;
- Character/Location binding;
- runtime readiness gate;
- deterministic legal options;
- canonical fingerprint unchanged.

Full autonomous Sandbox ticking remains a separate authorization boundary.

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

Nothing transmigrates automatically. Adrian Vale remains Sandbox-only. The second real Character gate remains closed.

---

## Test / release policy

During each slice:
- run the smallest task-relevant tests while iterating;
- use PR CI as the final repository checkpoint;
- targeted CI is preferred when selectors prove scope;
- use full fallback only for cross-cutting/unmapped risk;
- use production-copy acceptance only when stateful/migration/runtime risk actually requires it;
- do not infer production deployment from merge alone.

High-value continuing invariants:
- strict schema validation;
- canonical/Sandbox isolation;
- value/grade/requirement/access separation;
- exact relation semantics;
- atomic graph behavior;
- runtime readiness gates;
- zero canonical mutation on failed creation/compatibility paths.

---

## Exact resume point

**Latest merged implementation is PR #332 at `d670ac8e7a1ee3beaa6001011d8b04383c39533c`. CI #1164 passed 126 tests across 22 selected files with CLI init/status green and schema 21 healthy. I5.2 through I5.10 are complete. Next: I5.11 Sandbox Location Creation + Embedded Contents. Materialize the strict I5.10 Location schema in isolated Sandbox state; reuse I5.6/I5.8 Item contracts for embedded contents; validate the full parent/topology/content graph before one atomic apply; preserve `contains` vs `located_at` vs `stored_in` vs ownership semantics; do not infer runtime readiness and do not mutate canonical Real World state.**
