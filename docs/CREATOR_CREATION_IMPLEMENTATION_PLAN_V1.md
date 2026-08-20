# Creator Creation Systems — Minimum Implementation Plan v1

Status: **APPROVED IMPLEMENTATION PLAN — ACTIVE ITEM/LOCATION FOUNDATION**  
Date: 2026-08-20

## Objective

Build Creator Creation as a sequence of small vertical contracts that can create realistic Sandbox content without mutating the canonical Real World.

The current active dependency chain is:

`strict creation contracts -> quantity/measurement -> grading -> requirements/access -> Item -> Item batch/operations -> Location -> Location contents -> Character/Location binding -> runtime affordances -> vertical acceptance`

This plan deliberately reuses established world, inventory, valuation, grading and location foundations instead of inventing Sandbox-only duplicates.

---

## Completed foundation checkpoint

The following foundation families are already implemented/merged and should be treated as prerequisites rather than rebuilt:

- I0 — Creator authority hardening;
- I1 — universal creation proposal/socket core;
- I2 — isolated Creation Sandbox state/lifecycle;
- I2.5 — isolated Sandbox clock/speed/pause/readiness/AI binding;
- I3 — early Character + Location representation proof;
- I4 — Telegram Creator Studio proposal lifecycle;
- guided dual-pattern Creator Studio UX;
- I4.1 — Sandbox Character configuration UX;
- I5 — Sandbox Observer foundation;
- I5.1 — proactive Sandbox Observer delivery;
- exact AI Character schema generation/validation;
- exact Manual Character Creation parity;
- Sandbox Character profile browser/edit/grade parity;
- world-qualified Real/Sandbox runtime controls;
- scoped Telegram command-menu auto-sync.

Latest implementation checkpoint before this docs plan:
- PR #322 merge `366f07b4a9e1cfd0670d768132e9500f10c51b44`;
- PR #321 Creator live verification PASS for manual Character section persistence/prompt cleanup.

Character creation is sufficiently closed for the next dependency family. The old prototype Location socket is **not** considered a complete Location Creation system.

---

## Global creation rules for all following slices

### Exact schema rule

Every creation type must own a complete explicit versioned schema before AI generation is accepted.

Canonical pipeline:

`Creator intent -> exact schema -> AI fills permitted fields -> deterministic validation -> preview/draft -> explicit approval -> Sandbox apply`

AI output must fail closed on:
- missing required fields;
- unknown/extra keys;
- unknown conditional modules;
- wrong data types/units/enums;
- unresolved references;
- runtime-only or derived fields supplied as authoritative input;
- incompatible module combinations.

No heuristic “best effort” key acceptance.

### Strict core + strict conditional modules

Every major creation schema should use:
- one strict universal core for that type;
- zero or more explicitly selected strict conditional modules.

Conditional modules are versioned contracts, not arbitrary JSON extension bags.

### Manual/AI parity

Manual and AI creation may have different input UX but must converge on the same proposal validator and apply boundary.

### Isolation

Every slice must prove Sandbox operations do not mutate canonical Real World state unless that slice is explicitly a future transmigration apply slice. None of I5.2–I5.15 is such a slice.

### Reuse-first

Before adding a field/table/engine, inspect and reuse or adapt:
- `docs/INVENTORY_ITEM_ARCHITECTURE.md`;
- `docs/INVENTORY_OPERATIONS_V1.md`;
- `docs/UNIVERSE_OBJECT_VALUATION_RULES_V1.md`;
- `docs/MONEY_ECONOMY_FOUNDATION_V1.md`;
- `docs/UNIVERSAL_PROFILE_GRADING_FRAMEWORK_V1.md`;
- `src/observer_sandbox/grading.py`;
- `src/observer_sandbox/inventory.py`;
- `src/observer_sandbox/economic_value.py`;
- `docs/WORLD_LOCATION_NODE_MODEL.md`;
- `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`;
- `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`;
- `src/observer_sandbox/location_runtime.py`;
- existing Creation Sandbox proposal/lifecycle/runtime infrastructure.

---

# Active slices

## I5.2 — Creation Contract Audit & Reuse Map

### Objective

Reconcile the existing Character, inventory/item, economy/value, grading, world-location and Sandbox creation foundations before schema expansion.

### Deliverables

- one concise implementation-facing reuse map documenting authoritative existing models/helpers;
- identify prototype/legacy fields that must be adapted rather than copied;
- define which data belongs to reusable definitions versus concrete Sandbox instances;
- confirm relation ownership: structural containment, mutable storage, dynamic location, ownership, carriage/equipment;
- identify economic-value boundary for newly created Item/Location objects;
- identify current grading APIs to generalize rather than replace;
- no production/runtime mutation.

### Acceptance

- no competing Item/Location ontology introduced;
- all later slices point to explicit existing contracts/helpers;
- canonical state unchanged;
- docs-only/focused validation only as appropriate.

---

## I5.3 — Universal Quantity & Measurement Contract

### Objective

Create one unit-safe quantity representation usable by Item and Location schemas while keeping **Imperial as default presentation**.

### Required semantics

Support typed physical quantities needed by the first vertical, including:
- mass/load;
- length/dimensions;
- area;
- volume/capacity where needed.

Architecture:

`normalized physical quantity -> display conversion -> Imperial(default) | Metric(future UI)`.

### Rules

- do not store formatted strings such as `"55 lbs"` as the simulation authority;
- unit conversion must preserve the same physical truth;
- grades/requirements/runtime calculations consume normalized quantities;
- initial Creator UX presents pounds for weight/load and appropriate Imperial units elsewhere;
- Metric switching can be added later without schema rewrite.

### Acceptance

- equivalent Imperial/Metric quantities normalize identically;
- round-trip presentation stays within explicit precision tolerance;
- switching display units cannot change derived grade or requirement result;
- no existing Character measurement semantics regress.

---

## I5.4 — Universal Cross-Domain Grade Contract

### Objective

Generalize the already proven profile-grading architecture so Items, Locations, Quests and later gradeable subjects can share one vocabulary while retaining domain-specific evaluators.

### Shared vocabulary

`E, D, C, B, A, S, SS, SSS, X, XX`.

A scheme may expose only a legitimate subset. Current RAPS/Skill 0..100 schemes continue to use E..S.

### Required model

`authoritative raw state + named grading scheme + scheme-specific context -> derived grade result`.

Support:
- grade vocabulary/order comparison;
- named scheme registry;
- domain/dimension identity;
- optional grade profiles containing multiple dimensions;
- optional overall grade derived only by an explicit composite scheme;
- universe/domain ceiling/compatibility metadata for future validation.

### Rules

- grade is normally derived, not independently persisted truth;
- AI supplies raw facts/specs and may not invent a derived grade as authority;
- same letter across domains does not imply same raw scale;
- do not force raw numeric fields into grading without explicit scheme registration;
- SS/SSS/X/XX are not compressed into current Character 0..100 RAPS bands.

### Acceptance

- existing Character/Profile grade behavior remains unchanged;
- one Item exemplar derives a deterministic domain grade from raw specs;
- one Location/other synthetic exemplar proves a separate scheme can use the same vocabulary;
- grade comparison ordering is deterministic;
- unit-display changes do not alter grade;
- no grade persistence competes with source state.

---

## I5.5 — Universal Requirement & Access Contract

### Objective

Create one composable condition language for Item interactions, Location access, Quest gates and later action prerequisites while keeping **grade separate from authorization**.

### Requirement predicates

Initial contract should support only what the first vertical needs, with extensible typed forms such as:
- minimum grade in a named Character/domain dimension;
- minimum raw value/capability where appropriate;
- required skill/item/equipment/reference present;
- ownership/residency/authorization predicate;
- quest/state prerequisite;
- operating-state/time condition where already represented;
- explicit `all` / `any` composition.

### Access policy

Location access policy is a separate layer capable of representing:
- public/access-to-all;
- private;
- owner/resident;
- authorized-only;
- grade-gated;
- quest/state-gated;
- composite.

Operating state remains separate from access policy.

### Critical rule

> **Item Grade describes the item. Requirement Grade describes the interaction.**

A 55 lb dumbbell may have an S load grade, but a curl, goblet squat and simple relocation can require different Character Strength levels.

### Acceptance

- public high-grade Location can admit a low-grade Character;
- private Location can reject an otherwise high-grade unauthorized Character;
- grade-gated Location/Quest produces structured unmet requirements;
- Item grade is not automatically copied into Character requirement;
- requirement evaluation is deterministic and presentation-independent.

---

## I5.6 — Universal Item Schema v1

### Objective

Define the complete strict Item creation schema required for realistic physical/economic/runtime reasoning.

### Definition versus instance

Preserve existing architecture:

`universal Item definition -> concrete instance/stack -> location/container/owner state`.

Do not create owner/location-specific definitions.

### Strict core

The schema must support at minimum:
- technical/stable definition identity where applicable;
- display name;
- definition family and optional spec variant;
- category/subtype/classification;
- description/source/provenance;
- stackable versus unique;
- consumable versus non-consumable;
- movable/carriable versus fixed/installed;
- physical mass/weight;
- dimensions/size and occupied space/volume where meaningful;
- material/composition representation;
- condition/durability/serviceability semantics where applicable;
- storage/container compatibility;
- capabilities/affordances;
- economic-value policy + value/price inputs required by the valuation contract;
- modifier/effect references only through registered semantics;
- grade dimensions derived by registered schemes;
- compatibility/tags from registered vocabularies;
- module list/version identity.

### Strict conditional modules

Initial registry should cover enough families for broad reuse without trying to finish the whole future world:
- `container`;
- `consumable`;
- `food_nutrition`;
- `wearable_equipment`;
- `tool`;
- `powered_device`;
- `resistance_training_equipment`;
- `vehicle` when justified by existing world contracts;
- `medical` when justified by existing represented supplies/devices.

Only implement modules whose fields can be explicitly defined and validated. Unimplemented families remain unavailable rather than accepting arbitrary properties.

### Resistance-equipment exemplar

Use fixed dumbbells to prove family/spec semantics. Candidate module facts may include:
- resistance type;
- exact load quantity;
- fixed/adjustable;
- min/max/increment for adjustable equipment;
- supported use/capability metadata where deterministic consumers exist.

Do not encode unconditional `strength_gain`.

### Acceptance

- strict schema rejects unknown keys/modules;
- 2 lb and 55 lb dumbbells can share one family while preserving distinct exact specs;
- fixed versus movable and consumable versus non-consumable semantics validate;
- economic-value policy is explicit;
- no Character/location identity leaks into universal definition;
- schema is sufficient for later single/batch creation without free-form escape fields.

---

## I5.7 — Item Creation v1: Single

### Objective

Create one Item through Creator Studio in Manual or AI mode and activate it only into Creation Sandbox.

### Flow

`Create -> Item -> Build Manually | Generate with AI -> exact Item schema -> validate -> preview/edit -> approve -> Sandbox object/definition+instance materialization`.

### Requirements

- AI structured output constrained to exact schema;
- Manual mode exposes typed sections/modules from the same schema registry;
- derived grades shown read-only;
- economic/value coverage validated before activation;
- provenance/revision recorded;
- no canonical inventory/world/economy mutation;
- view/detail surface after activation.

### Acceptance

- single fixed dumbbell exemplar can be created end to end;
- invalid AI/manual values fail before apply;
- reroll/edit cannot inject unknown schema fields;
- Sandbox-only state changes; Real World fingerprint unchanged.

---

## I5.8 — Item Batch Creation v1

### Objective

Support creating multiple strict Items efficiently, including variant families such as dumbbell sets.

### Batch contract

- one strict batch envelope;
- each member is an individually strict Item payload;
- optional internal references/family relationship only through defined IDs;
- per-item validation results;
- deterministic batch preview;
- explicit apply semantics.

Prefer atomic activation when batch members have internal dependencies. If independent partial acceptance is useful later, make that a separate explicit mode rather than accidental partial writes.

### Acceptance

- generate/create a representative dumbbell set with multiple pound variants;
- every member validates against the same Item schema/module contract;
- one invalid dependent member prevents atomic activation;
- no unknown fields are tolerated because output came from a batch AI request;
- failure leaves no partial active Sandbox batch state under atomic mode.

---

## I5.9 — Sandbox Item / Container Operations

### Objective

Reuse existing inventory semantics for active Sandbox objects.

### Operations

Minimum:
- place/store an Item in a represented Sandbox container/Location;
- remove Item from container;
- move Item between valid containers/Locations;
- inspect contents;
- preserve ownership independently from storage/location;
- support stack quantity semantics where applicable;
- support unique Item instance state where applicable.

### Relation rules

Preserve:
- `contains` = authored structural/static containment;
- `stored_in` = mutable inventory containment;
- `located_at` = dynamic physical presence;
- `owned_by` = ownership;
- `carried_by` / `equipped_by` = separate state.

### Acceptance

- move an Item without redefining it;
- move a movable container and preserve logical contents;
- reject containment cycles;
- Real World inventory unchanged;
- Sandbox reset/delete cleans related Item state safely.

---

## I5.10 — Universal Location Schema v1

### Objective

Replace the prototype name-centric Location creation path with a strict spatial-container schema aligned to the authoritative world contract.

### Location core

Support:
- stable identity/display name;
- kind/spatial role and functional classification;
- parent structural container where applicable;
- known spatial extent/dimensions/area without fabricated precision;
- indoor/covered/outdoor exposure;
- terrain/surface/geographic metadata only when known/needed;
- boundaries/interfaces/topology references;
- ownership/control/residency references where represented;
- access policy;
- operating state separately;
- local environment/state hooks;
- facilities/affordances;
- child Location references;
- structural fixtures/objects;
- mutable Item/resource contents through proper instance relations;
- occupancy separately from structural containment;
- economic/asset valuation policy;
- domain grade profile;
- source/provenance/canon status;
- schema/module version identity.

### Rules

- Location = spatial container, not a screen label;
- containment != traversal;
- adjacency != traversability;
- connection != current permission;
- unknown geometry remains unknown;
- do not create arbitrary doorway micro-nodes;
- do not infer ownership from presence/containment.

### Acceptance

- strict schema rejects arbitrary AI keys;
- nested Location hierarchy is acyclic;
- public/private access semantics remain separate from grade;
- Item/fixture/occupant relationships are not conflated;
- Location can exist at a declared completeness level without inventing absent precision.

---

## I5.11 — Location Creation + Embedded Contents

### Objective

Create a Sandbox Location either empty or with explicit initial contents in one Creator workflow.

### Supported creation patterns

1. `Location only`;
2. `Location + references to already active Sandbox Items`;
3. `Location + new Item batch` using the strict Item batch contract.

Embedded contents are never unvalidated free-form prose.

### Transaction semantics

When new Location and new dependent Items are created together, activation should be atomic:
- validate Location;
- validate all Item payloads/modules;
- resolve internal references;
- validate valuation/access/containment constraints;
- apply all or none.

### Acceptance

- create a representative Sandbox gym Location with a validated dumbbell set;
- reject invalid contained Item without leaving half-created active state;
- Location contents resolve to real Sandbox Item IDs/instances;
- canonical world graph/inventory unchanged.

---

## I5.12 — Location Contents Editing / Operations

### Objective

Allow Creator to change an active Sandbox Location after creation without recreating the Location.

### Minimum operations

- add existing/new Item;
- remove Item;
- move Item to another valid Location/container;
- inspect structural children versus inventory contents;
- update allowed Location fields through strict schema editing;
- preserve stable Location identity and revision/audit history.

### Acceptance

- add/remove/move contents after Location creation;
- structural `contains` is not accidentally rewritten for ordinary inventory moves;
- access/grade/value recomputation occurs only through registered derived rules;
- Real World remains unchanged.

---

## I5.13 — Character ↔ Location Binding & Runtime Readiness

### Objective

Make an active Sandbox Character explicitly occupy a valid active Sandbox Location and integrate that with readiness.

### Requirements

- select active Sandbox Location;
- create/update isolated Character `located_in/located_at` representation according to current Sandbox contract;
- reject cross-namespace/inactive/wrong-type references;
- expose current Location in Creator surfaces;
- readiness requires a valid usable Location plus existing clock/options/cognition binding gates;
- removing/archiving the Location invalidates readiness cleanly.

### Acceptance

- place current Sandbox Character into the new Location;
- move/rebind within Sandbox safely;
- readiness false when Location dependency is absent/invalid;
- Real World actor location unchanged;
- `runtime_ready` still does not imply autonomous running.

---

## I5.14 — Item / Location Runtime Affordance Bridge

### Objective

Derive meaningful deterministic action options from represented Location facilities/resources and Item capabilities instead of names or narrative guesses.

### Core chain

`Character capability/state + Location + available Item/facility specs + access/environment + action contract -> valid options/requirements -> cognition choice -> deterministic validation`.

### Training exemplar

Use resistance training to prove contextual effects:

`dumbbell load/spec + exercise + actor strength/capacity + reps/sets/tempo/ROM/rest + fatigue/history -> valid workload / training stimulus`.

A 2 lb dumbbell should not automatically provide meaningful strength progression to an elite Character merely because it is tagged `dumbbell`; it may still support warm-up/rehab/endurance contexts.

### Rules

- Item names do not grant actions;
- Location labels do not grant actions;
- no unconditional generic stat bonuses where context is required;
- cognition cannot invent missing equipment, doors, facilities or resources;
- the same requirement evaluator used to shape options validates committed action.

### Acceptance

- options differ when relevant Item specs differ;
- unavailable/insufficient resources suppress or fail the relevant action deterministically;
- a represented valid training setup exposes appropriate action capability;
- no model owns physical arithmetic/state mutation;
- Sandbox-only execution evidence.

---

## I5.15 — Sandbox Vertical Acceptance

### Objective

Prove the complete pre-autonomy vertical:

`strict Character + strict Location + strict Items -> active Sandbox objects -> contents/binding -> runtime readiness -> deterministic represented options`.

### Required acceptance

- create or reuse one exact-schema Sandbox Character;
- create Item(s), including a batch exemplar;
- create a usable Location and attach contents;
- edit contents after creation;
- bind Character to Location;
- derive/read grades without changing raw truth;
- evaluate access/requirements separately;
- produce deterministic represented runtime options;
- inspect through Telegram Creator/Observer surfaces;
- reset/delete safely;
- prove canonical Real World character/world/inventory/economy state unchanged.

### Explicit stop point

Passing I5.15 does **not** authorize full Sandbox autonomous ticking. After acceptance, stop for Creator review and define the smallest autonomous execution slice separately.

---

# I6 — Transmigration planning/validation boundary

I6 remains deferred and planning-only unless Creator explicitly changes scope.

Minimum future boundary:
- freeze source Sandbox revision/snapshot;
- choose target-universe profile;
- compute dependency closure;
- validate grade/capability/system compatibility;
- return structured compatible/incompatible/dependency/error results;
- generate deterministic proposed canonical mutations;
- incompatible/failure path produces zero target-universe writes.

Supernatural/impossible Items, Locations or systems may be valid Sandbox content while rejected by the current realistic Real World and accepted by another future universe profile.

No automatic canonical apply.

---

## Explicit non-goals for I5.2–I5.15

Do not include as side effects:
- full multi-universe runtime;
- full autonomous Sandbox ticking;
- automatic canonical promotion;
- arbitrary AI-generated executable code;
- exhaustive crafting/market/logistics systems;
- exhaustive Item conditional modules merely for completeness;
- GIS/polygon geometry for every Location;
- every doorway as an entity;
- migration/refactor of the canonical Thorne Estate merely to support Sandbox creation;
- second real production Character activation.

---

## Test policy

Use smallest relevant tests during implementation. Final CI is the PR checkpoint.

High-value regression themes across the slices:
- exact schema/unknown-key rejection;
- Manual/AI apply-boundary parity;
- unit normalization/display invariance;
- derived grade authority and existing Character grading regression;
- grade versus requirement separation;
- grade versus access separation;
- definition versus instance semantics;
- batch atomicity/reference resolution;
- containment-cycle rejection;
- valuation coverage;
- Sandbox/Real zero-mutation isolation;
- readiness dependency gating;
- property/capability-driven affordances;
- reset/delete cleanup.

Docs-only planning changes do not require the full Python suite.
