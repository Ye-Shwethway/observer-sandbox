# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**  
Last synchronized: **2026-08-20**

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
5. task-relevant canonical contracts/source
6. verified runtime/deploy evidence before live claims.

Authority:
`current Creator instruction > live repo contracts/config/schema > verified runtime/DB > CI/deploy evidence > continuity docs > remembered chat`.

Persistent branches: `main`, `test` only.

Workflow:
`test implementation -> focused verification -> PR/final CI -> merge main -> runtime deploy only when applicable -> verify evidence -> sync continuity -> main/test exact sync`.

Do not infer production deployment from merge alone.

---

## Current merged checkpoint

Latest implementation merge:

### PR #332 — I5.10 Universal Location Schema v1

Merge:
`d670ac8e7a1ee3beaa6001011d8b04383c39533c`

Final head:
`aaf17efb4e142a5b3691bbd1eba1c9502c39143b`

Evidence:
- CI #1164 — **SUCCESS**;
- 22 selected test files;
- **126 passed**;
- CLI init/status green;
- fresh DB healthy;
- schema version 21.

The first #332 run failed only because the new Location adapter referenced nonexistent `PhysicalQuantity` attributes. The adapter was corrected to use the existing `kind`, `base_value`, `base_unit` contract and preserve validated source value/unit without changing the shared quantity API.

`main` and `test` were synchronized to the merge before this continuity update.

---

## Completed Creator Item / Location foundation

### I5.2 — Creation Contract Reuse Map — COMPLETE

`docs/CREATION_CONTRACT_REUSE_MAP_V1.md`

Locks:
- generic proposal envelope stays reusable;
- exact type-specific schemas sit beneath it;
- Sandbox lifecycle/isolation stays shared;
- Item definition, concrete instance/stack, placement/storage and ownership remain distinct;
- Real World inventory/value/grading/location semantics are reused through Sandbox adapters;
- legacy Sandbox Character `located_in` remains prototype compatibility semantics to reconcile later toward canonical `located_at`.

### I5.3 — Quantity / Measurement — COMPLETE

PR #324 merge `a4abcbbcb932711bcf164d20bb977314afad5550`; CI #1155, 22 passed.

`physical_quantity.py` provides normalized SI physical truth for mass/length/area/volume with Imperial-default Creator presentation and zero truth mutation on display conversion.

### I5.4 — Cross-Domain Grading — COMPLETE

PR #325 merge `980a752160a48144ef91bf800c4f4ab8fc5bc98e`; CI #1157, **189 passed**.

Shared ordering:
`E < D < C < B < A < S < SS < SSS < X < XX`.

Existing Character schemes stay compatible. Item resistance load and Location completeness are separate domain/dimension schemes.

### I5.5 — Requirements / Access — COMPLETE

PR #326 merge `2372a3a32f3b400a029317174fcf7260fee7f1f3`; CI #1158, 22 passed.

Typed requirements support minimum grade, values, skill, Item/equipment, ownership, residency, authorization and state with nested `all`/`any`.

Location access policy and operating state remain separate.

### I5.6 — Universal Item Schema v1 — COMPLETE

PR #328 merge `5820aad0f4abf5efb4b352071cbb67ee8056071b`; CI #1159, **74 passed / 11 selected files**.

Contract:
`docs/UNIVERSAL_ITEM_SCHEMA_V1.md`

Implementation:
`src/observer_sandbox/item_creation_schema.py`

Exact Item semantics:
- stable definition facts;
- unique or stack concrete instance;
- strict conditional modules;
- physical quantities;
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

### I5.7 — Single Sandbox Item Creation — COMPLETE

PR #329 merge `74d83bc6d50a61a76becb41bc53d6cc65b354257`; CI #1160, **89 passed / 17 selected files**.

Added isolated Sandbox Item definition, instance/stack and economic-policy persistence plus atomic materialization.

Relations validate active same-Sandbox targets. Canonical fingerprint remains unchanged.

### I5.8 — Heterogeneous Item Batch — COMPLETE

PR #330 merge `716b56e64fa106f633c13c55de9211a7a67e5c8b`; CI #1161, **88 passed / 15 selected files**.

Single Item is now literally batch size 1.

Batch supports:
- write-free full preview;
- forward `$ref` for batch-local `stored_in`;
- container validation;
- duplicate/unknown/self/cycle rejection;
- same-key semantic consistency;
- all-or-nothing transaction.

### I5.9 — Item / Container Operations — COMPLETE

PR #331 merge `d4b60e5fdd18706cbd60da8cdde556226c826efe`; CI #1162, **99 passed / 18 selected files**.

Supports browse/inspect, validated edit, move/store/own/carry/equip, stack quantity, archive/delete and dependency reporting.

Important locks:
- physical placement modes are mutually exclusive;
- ownership is orthogonal;
- shared definitions cannot be rewritten through one instance;
- container archive/delete refuses incoming dependencies unless explicit detach is requested;
- dependent Items survive detach;
- Sandbox reset now clears Item definitions as well as object-owned Item state.

### I5.10 — Universal Location Schema v1 — COMPLETE

PR #332 merge `d670ac8e7a1ee3beaa6001011d8b04383c39533c`; CI #1164, **126 passed / 22 selected files**.

Contract:
`docs/UNIVERSAL_LOCATION_SCHEMA_V1.md`

Implementation:
`src/observer_sandbox/location_creation_schema.py`

Exact Location domains:
- identity/kind;
- structural parent + exposure;
- optional normalized extent;
- access policy + separate operating state;
- explicit spatial interfaces/topology;
- machine-readable facilities/resources/capabilities;
- minimal represented environment;
- optional economic policy;
- provenance.

Unknown spatial precision remains null. Completeness L0-L4 and Location grade are derived, not authored truth or access authority.

---

## Core semantic locks

### Item ontology

`Item Definition -> concrete unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`

Do not flatten these into one properties bag.

### Relation ontology

- `contains` = structural/static spatial containment;
- `located_at` = current dynamic physical presence;
- `stored_in` = inventory/container storage;
- `owned_by` = ownership;
- `carried_by` = carriage;
- `equipped_by` = equipped state.

Ownership never follows automatically from location/storage.

### Grade / requirement / access

`Item Grade != Character requirement != Location access != Location operating state`.

### Creation / runtime

**Created is not alive.**

`runtime_ready != running` remains locked.

### Isolation

Creation Sandbox must not mutate canonical Real World entity/item/inventory/economic/runtime state. Continue using `canonical_state_fingerprint()` as a high-value acceptance check.

---

## Exact next slice

### I5.11 — Sandbox Location Creation + Embedded Contents

Next implementation must materialize the strict I5.10 Location contract into Sandbox-owned state.

Support both:
1. empty Location;
2. furnished/populated Location with typed embedded Item contents.

Required direction:
- exact I5.10 validation first;
- active same-Sandbox structural parent validation when supplied;
- parent graph remains acyclic;
- explicit interface destination validation where supplied;
- Sandbox-owned economic/access/topology/location state only;
- embedded new Items invoke I5.6/I5.8 Item contracts rather than a parallel contents schema;
- validate complete Location + contents graph before write;
- atomic apply/rollback;
- no automatic runtime readiness;
- no canonical writes.

Do not add broad Telegram Location authoring UX before the materialization/composition contract is deterministic.

---

## Subsequent route

### I5.12 — Location Contents Operations
- add existing Item;
- create Item;
- create Item batch;
- remove/move Item;
- create child Location;
- preserve relation distinctions and explicit dependency handling.

### I5.13 — Character ↔ Location Binding & Runtime Readiness
Reconcile Sandbox prototype `located_in` toward canonical `located_at` through Sandbox-owned persistence/adapters. A name-only place must not make a Character runnable; target a usable represented Location (conceptually at least L3 unless the implemented readiness contract says otherwise).

### I5.14 — Item / Location Runtime Affordance Bridge
Derive legal options from represented Items/fixtures/resources/environment/capabilities/access/requirements, never from Location labels or LLM invention.

### I5.15 — Sandbox Vertical Acceptance
Prove strict Character + strict usable Location + typed contents + correct relations/economics + binding/readiness/options with canonical fingerprint unchanged.

Full Sandbox autonomous ticking remains separately unauthorized.

---

## Character and transmigration locks

Character exact Manual/AI parity and Sandbox profile/edit/grade-target behavior remain established and must not be loosened.

Nothing transmigrates automatically.

I6 remains planning/validation only unless the Creator explicitly changes scope.

Adrian Vale remains Sandbox-only. The second real Character gate remains closed.

---

## Exact resume point

**Latest merged implementation is PR #332 at `d670ac8e7a1ee3beaa6001011d8b04383c39533c`. CI #1164 passed 126 tests across 22 selected files with CLI init/status green and schema 21 healthy. I5.2 through I5.10 are complete. Next: I5.11 Sandbox Location Creation + Embedded Contents. Materialize the strict I5.10 Location schema in isolated Sandbox state; reuse the I5.6/I5.8 Item contracts for embedded contents; validate the whole graph before one atomic apply; preserve `contains` vs `located_at` vs `stored_in` vs ownership semantics; do not grant runtime readiness automatically and do not mutate canonical Real World state.**
