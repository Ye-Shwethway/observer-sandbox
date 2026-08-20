# Creator Creation Contract Reuse Map v1

Status: **ACTIVE IMPLEMENTATION CONTRACT — I5.2 COMPLETE**  
Date: 2026-08-20

## Purpose

This document closes I5.2 by mapping the existing Observer Sandbox contracts and helpers that later Creator Item/Location slices must reuse, adapt, or deliberately replace.

The goal is to prevent a second Item, Location, grading, economy, relation, or Sandbox ontology from appearing during I5.3–I5.15.

Core rule:

`reuse authoritative semantics -> add typed adapters/contracts -> preserve world isolation -> remove prototype ambiguity only where the later slice owns it`

No runtime or canonical-world mutation is authorized by this document.

---

## 1. Creation proposal envelope

### Reuse

`src/observer_sandbox/creation_socket.py`

Keep the generic proposal envelope and proposal-level invariants:
- proposal version;
- creation type;
- schema version;
- Sandbox-only target scope;
- identity/properties/relationships/capabilities/provenance envelope;
- provenance mode validation;
- unknown top-level proposal keys rejected.

### Adapt

The generic socket is **not** the final type schema.

Current prototype Location registration requires only `identity.name`, while `properties`, `relationships` and `capabilities` remain structurally generic. Character has already evolved beyond this prototype through a stricter type-specific contract.

I5.6 and I5.10 must therefore use:

`generic creation envelope -> exact type-specific schema validator -> normalized typed proposal`

Do not weaken Character strictness to make Item/Location fit the old generic bag.

### Replace/prohibit

Do not add Item/Location AI generation that treats arbitrary `properties` keys as valid simply because the top-level proposal envelope validates.

---

## 2. Creation Sandbox persistence and lifecycle

### Reuse

`src/observer_sandbox/creation_sandbox.py`

Reuse:
- Sandbox namespace ownership;
- collision-safe `sbx_*` object ids;
- active/archive/delete/reset lifecycle;
- Sandbox event/audit stream;
- Sandbox-only object persistence;
- same-Sandbox relation validation;
- `canonical_state_fingerprint()` zero-mutation proof;
- isolated actor-runtime/readiness ownership for Sandbox Characters.

### Adapt

Current `creation_sandbox_objects` JSON columns are a generic persistence envelope. Later strict Item/Location contracts may materialize normalized Sandbox-owned supporting rows/tables where deterministic operations require them, but those rows remain under the Creation Sandbox ownership boundary.

The generic object JSON remains proposal/representation data; it must not become a reason to skip normalized operational state when Item stacks, container relations, quantities or spatial topology need deterministic querying.

### Legacy/prototype relation

Current Character-to-Location binding writes Sandbox relation type `located_in`.

Canonical Real World dynamic-location authority is `located_at` through `src/observer_sandbox/location_runtime.py`.

Decision:
- `located_in` is a Sandbox prototype compatibility relation, not the future universal relation name;
- I5.13 must reconcile Sandbox dynamic presence to the canonical semantic `located_at` through a Sandbox-owned adapter/migration;
- do not create a third dynamic-location relation.

---

## 3. Universal Item definition / instance / stack model

### Reuse

Authoritative contracts:
- `docs/INVENTORY_ITEM_ARCHITECTURE.md`;
- `docs/INVENTORY_OPERATIONS_V1.md`;
- `src/observer_sandbox/inventory.py`.

Canonical semantic chain:

`universal definition -> concrete instance/stack -> physical container/location -> ownership -> action/evidence -> quantity/state transition`

Existing Real World persistence establishes the important separation:
- reusable item semantics live in `entity_definitions`;
- concrete physical item/stack identity lives in `entities`;
- durable fungible quantity lives in `inventory_stacks`;
- current storage/ownership/carriage/equipment live in explicit relations.

### Definition-owned data

Reusable definition facts include, as applicable:
- semantic family/category;
- canonical capabilities;
- physical/specification semantics shared by the definition/variant;
- stackability and canonical quantity-unit semantics;
- nutrition/effects or later registered modules;
- economic unit/value policy when definition-level pricing is appropriate.

Definitions must not encode a particular owner or current Location.

### Concrete instance/stack-owned data

Instance/runtime facts include, as applicable:
- stable concrete object/stack id;
- quantity for stackable stock;
- current condition/service state when instance-specific;
- storage/current location;
- ownership;
- carried/equipped state;
- instance-specific provenance/history.

### Adapt

Creation Sandbox must reuse these semantics without writing new Sandbox Items into canonical `entity_definitions`, `entities`, `inventory_stacks`, or `relations` before transmigration.

I5.6–I5.9 should provide Sandbox-owned definition/instance/stack adapters or normalized state that mirrors the same semantic split.

### Prohibit

Do not collapse all of the following into one free-form Sandbox Item object:
- reusable Item definition;
- unique physical instance;
- fungible stack quantity;
- storage relation;
- ownership relation.

---

## 4. Relation ownership map

The following semantics are authoritative and must remain distinct.

| Relation | Authority / meaning | Reuse decision |
| --- | --- | --- |
| `contains` | authored structural/static containment and Location hierarchy | reuse unchanged |
| `connected_to` | legal traversable topology | reuse unchanged |
| `located_at` | current dynamic physical presence of a movable entity | canonical semantic; Sandbox adapter required |
| `stored_in` | mutable inventory/container storage | reuse unchanged semantically |
| `owned_by` | legal/economic ownership | reuse unchanged semantically |
| `carried_by` | current carriage/possession | reuse unchanged semantically |
| `equipped_by` | current equipped state | reuse unchanged semantically |

Rules:
- containment does not imply traversal;
- location/storage does not imply ownership;
- ownership does not imply current location;
- carriage/equipment are not structural containment;
- ordinary inventory moves must not rewrite Location hierarchy.

Sandbox implementations use Sandbox-owned relation persistence but keep these meanings.

---

## 5. Location world model

### Reuse

Authoritative contracts:
- `docs/WORLD_LOCATION_NODE_MODEL.md`;
- `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`;
- `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`;
- `src/observer_sandbox/location_runtime.py`.

Canonical definition:

> Location = an identifiable spatial container with extent, contents, boundary/interface semantics, local state and explicit relationships to surrounding space.

Reuse unchanged:
- stable technical identity independent of display name/path;
- recursive structural containment;
- acyclic hierarchy;
- `connected_to` topology separate from containment;
- dynamic presence through `located_at`;
- access/permission separate from topology;
- unknown geometry remains unknown;
- fixtures/resources/occupants are not all one relation class;
- Location label alone does not grant an action.

### Adapt / replace prototype

The existing Creator Location socket is only an early representation proof. It is not a complete Location Creation schema.

I5.10 replaces the name-centric arbitrary-properties prototype with a strict type-specific spatial-container schema while preserving generic Creation Sandbox lifecycle/identity.

Do not mutate or refactor the canonical Thorne Estate merely to implement Sandbox Location creation.

---

## 6. Economic value boundary

### Reuse

Authoritative contracts/helpers:
- `docs/MONEY_ECONOMY_FOUNDATION_V1.md`;
- `docs/UNIVERSE_OBJECT_VALUATION_RULES_V1.md`;
- `src/observer_sandbox/economic_value.py`.

Existing classifications:
- `standalone_asset`;
- `component`;
- `consumable_stock`;
- `resource_proxy`;
- `economically_immaterial`.

Existing net-worth treatments:
- `independent`;
- `included_in_parent`;
- `derived_stock`;
- `excluded`.

Core invariant:

`has economic value != contributes independent net worth`

### Reuse in later creation slices

Reuse the **classification, validation and valuation semantics**. New Item/Location schemas must require an explicit applicable economic-value policy rather than an accidental default.

For stock, definition-level unit value may derive current stack value from quantity.

For fixtures/components, replacement value may exist while net-worth treatment remains `included_in_parent`.

### Isolation boundary

Do **not** write Sandbox creation values directly into canonical:
- `economic_value_profiles`;
- `economic_assets`;
- canonical accounts/ledger/net-worth state.

I5.6/I5.10 stage equivalent validated Sandbox-owned value policy data. Future transmigration adapts that policy into the target universe only after compatibility/authority checks.

The current `require_entity_value_policy()` helper validates canonical entity persistence; its policy semantics should be generalized/adapted, not called against nonexistent Sandbox canonical rows.

---

## 7. Grading reuse boundary

### Reuse

`src/observer_sandbox/grading.py` and `docs/UNIVERSAL_PROFILE_GRADING_FRAMEWORK_V1.md` already establish:
- shared vocabulary `E, D, C, B, A, S, SS, SSS, X, XX`;
- explicit named scheme registry;
- `GradeResult` / `GradeScheme` concepts;
- monotonic, target-range and composite scheme families;
- derived read-time grades rather than competing persisted truth;
- explicit opt-in rather than automatically grading every number.

### Generalize, do not replace

I5.4 should extend this architecture with:
- deterministic grade ordering/comparison;
- explicit domain/dimension identity;
- Item and Location schemes;
- optional multi-dimension grade profiles;
- explicit composite schemes where justified;
- future universe/domain ceiling metadata.

Current RAPS/Skill/body behavior must remain unchanged.

### Prohibit

Do not allow AI-authored grade letters to become source truth for physical Item/Location facts when a registered evaluator exists.

Do not assume same letter = same raw scale across domains.

---

## 8. Requirement/condition reuse boundary

### Existing reusable primitive

`src/observer_sandbox/action_conditions.py` already provides a small deterministic fail-closed comparison engine for explicit field conditions.

It proves useful behavior to retain:
- typed bounded operators;
- malformed contracts fail closed;
- missing authoritative values fail closed;
- structured evaluated/failure output.

### Do not overextend it

Current v1 action conditions support exactly one `all` list of generic field comparisons. They do not represent:
- grade-aware requirements;
- `any` composition;
- possession/equipment predicates;
- authorization/residency/ownership;
- quest/state references;
- Location access policy.

I5.5 should therefore build a typed universal requirement/access contract that reuses comparison/evaluation principles, not mutate arbitrary access semantics into the old field-only shape.

---

## 9. Quantity and measurement boundary for I5.3

Current inventory definitions/stacks already use canonical quantity/unit pairing, and body/profile systems have domain-specific physical measurements. There is not yet one reusable cross-domain physical quantity object for Item/Location creation.

I5.3 therefore owns the new minimal abstraction:

`normalized physical quantity + quantity kind -> deterministic conversion/presentation`

It must:
- preserve existing Character/profile fields unchanged;
- provide Item/Location-safe typed quantities;
- keep formatting out of authoritative state;
- make Imperial the default Creator-facing presentation;
- allow later Metric display without changing physical truth.

Do not rewrite existing inventory stock quantities or Character body storage merely to adopt the new helper.

---

## 10. Character contract boundary

Character creation is already the strictness exemplar.

Reuse its architectural pattern:
- exact creation-owned schema;
- shared deterministic validator for Manual and AI paths;
- runtime/derived fields excluded from Creator seed authority;
- structured collections validated separately where repetition is legitimate;
- Sandbox-only approval/materialization;
- revision/audit evidence.

Do not force Item/Location into Character profile field storage. Reuse the **contract pattern**, not Character-specific persistence.

---

## 11. Later-slice wiring map

| Slice | Must start from |
| --- | --- |
| I5.3 Quantity/Measurement | existing unit-bearing inventory/profile facts + this map; add minimal standalone quantity helper |
| I5.4 Cross-Domain Grade | `grading.py` registry/results/vocabulary; extend without changing current schemes |
| I5.5 Requirement/Access | fail-closed `action_conditions.py` principles + world access/topology semantics |
| I5.6 Item Schema | inventory definition/instance/stack split + value policy + quantity + grade + requirement contracts |
| I5.7 Single Item | generic creation envelope + exact Item validator + Sandbox lifecycle + Sandbox Item adapters |
| I5.8 Item Batch | same exact Item validator per member; batch is orchestration, not relaxed schema |
| I5.9 Item Operations | `stored_in`/ownership/carriage/equipment semantics + Sandbox-owned operational state |
| I5.10 Location Schema | world spatial-container contract + quantity/access/value/grade contracts |
| I5.11 Embedded Contents | strict Location + exact Item batch + atomic Sandbox apply |
| I5.12 Contents Operations | structural `contains` kept separate from inventory movement |
| I5.13 Binding/Readiness | canonical `located_at` semantic through Sandbox adapter; remove reliance on prototype `located_in` |
| I5.14 Runtime Affordances | represented Item/fixture/Location capabilities + deterministic action authority |
| I5.15 Vertical Acceptance | strict Character + strict Location + strict Items + isolated binding/readiness/options |

---

## 12. Explicit no-duplicate decisions

The following are rejected designs:
- separate Sandbox-only Item ontology with different definition/instance semantics;
- separate Sandbox-only grade vocabulary;
- Location `contents` as arbitrary prose/JSON without typed references;
- one `contains` relation used for structure, inventory, occupants and ownership;
- Item grade copied directly into Character interaction requirement;
- Location grade treated as access authorization;
- Sandbox value policy written into Real World economy before transmigration;
- another dynamic-location relation beyond migration from prototype `located_in` to semantic `located_at`;
- broad canonical world/schema refactor as a side effect of Item/Location Sandbox creation.

---

## I5.2 acceptance result

I5.2 is complete when this document is merged.

Result:
- authoritative reuse points are explicit;
- prototype/legacy boundaries are identified;
- definition versus instance/stack ownership is locked;
- relation ownership is locked;
- economic-value isolation boundary is explicit;
- grading and requirement extension points are explicit;
- no code/runtime/schema/production mutation is part of this slice.

Next slice:

**I5.3 — Universal Quantity & Measurement Contract.**
