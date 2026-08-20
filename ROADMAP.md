# Observer Sandbox Roadmap

Status: ACTIVE  
Roadmap synchronized: **2026-08-20**

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema, verified live runtime/DB and current CI/deploy evidence outrank remembered chat context.
- AI proposes structured facts; deterministic contracts validate, derive and mutate.
- Telegram is observer/control, never simulation authority.
- Creator-approved state outranks ordinary seed/default refresh.
- Creator-created objects stage in Creation Sandbox first; Sandbox approval and canonical transmigration are separate authority transitions.
- **Created is not alive.** Creation, runtime readiness and runtime execution are separate boundaries.
- Real World and Creation Sandbox mutable state remain isolated.
- Reuse established Real World systems and ontologies for Sandbox equivalents whenever semantics match; prefer adapters over parallel systems.
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**

---

## Current repository checkpoint

Latest merged implementation checkpoint:

### PR #322 — Auto-sync scoped Telegram command menus

Merge commit:
`366f07b4a9e1cfd0670d768132e9500f10c51b44`

Evidence:
- CI #1154 — targeted mode, **96 passed**;
- `main == test` at the merge checkpoint;
- role-scoped Telegram command menus are generated from the final `/help` contract on bot startup;
- stale chat scopes are removed;
- legacy ambiguous `/pause`, `/resume`, `/speed`, `/time` remain non-mutating redirects and are not advertised.

Production deployment/live command-menu behavior for PR #322 has **not been independently verified** from repository evidence. Do not infer live deployment from merge alone.

### PR #321 — Manual Character field editing UX closure

Merge commit:
`6c568711e67b63f0412daf84189187834e9e71dd`

Evidence:
- CI #1153 — targeted mode, **135 passed**;
- accepted manual field input stays inside the same section/page;
- consumed prompt cards are deleted; rejected input edits the existing prompt into retry state;
- Creator live Telegram verification — **PASS**.

### PR #319 — Manual Character Creation Exact Parity

Merge commit:
`6838c9503fee9d9bd2bd8b4786e10cc907ba5c2`

Manual and AI Character creation now share the same exact creation-owned profile field contract. Manual creation supports typed structured fields, collections, exact readiness validation, revisioned drafts and Sandbox-only approval/materialization.

Character creation is therefore sufficiently closed for the next vertical dependency work. Character creation alone is **not** sufficient for a runnable Sandbox actor: a usable Location and relevant world contents are required.

---

## Active Creator Creation direction — Item + Location Foundation

The next architecture family is the **Universal Item and Location Creation Foundation**.

The ordering is intentional:

`strict creation contracts -> quantity/measurement -> universal grading -> universal requirements/access -> item schema -> item creation -> item batch/operations -> location schema -> location contents -> Character/Location binding -> runtime affordances`

Full autonomous Sandbox ticking remains later. `runtime_ready != running` stays locked.

### Why Item precedes full Location creation

A Location is an identifiable **spatial container**, not a label or dimensionless node. It may contain child locations, fixtures, movable items, resources and occupants.

Creator must be able to:
- create a Location with contents already represented;
- create a Location first and add Items later;
- remove/move Items later;
- move Items between Locations/containers without redefining Item identity.

Therefore robust Location creation depends on a reusable Item creation/instance model rather than a free-form `contents` bag.

Existing world architecture remains authoritative:
`universal definition -> concrete instance/stack -> physical container/location -> ownership -> action/evidence -> state transition`.

Do not create a second Sandbox-only inventory ontology. Reuse the universal definitions, instance/stack semantics, relations and operations through Sandbox-owned storage/adapters.

---

## Strict creation-schema contract

Every Creator Creation type must have a **complete, explicit, versioned schema** before AI generation is allowed for that type.

Canonical rule:

`Creator intent -> exact registered JSON-like schema -> AI fills permitted fields only -> deterministic validation -> draft`

AI must not:
- invent unknown keys;
- omit required core fields;
- invent conditional-module shapes;
- guess runtime-only/derived state;
- bypass registered units, enums, references or value policies;
- write directly to canonical or Sandbox runtime state.

Preferred schema architecture:

`strict core + strict conditional modules`.

The core describes properties universal to the creation type. Conditional modules are selected by explicit classification/capabilities and are themselves strict/versioned. This allows future expansion without weakening validation into arbitrary JSON.

Manual and AI creation must converge on the same validation/apply boundary.

---

## Universal quantity and measurement direction

Imperial is the primary Creator-facing measurement system.

Default presentation examples:
- weight/load: `lb`;
- length/body dimensions: inches/feet as appropriate;
- area/volume use domain-appropriate Imperial presentation.

Future UI may switch to Metric without changing physical truth.

Architecture invariant:

`canonical physical quantity -> presentation conversion -> Imperial(default) | Metric`

A unit-display change must not alter grade, capability, requirement or runtime outcome. Grading and simulation consume normalized physical quantities, not formatted strings such as `"55 lbs"`.

---

## Universal cross-domain grading

Observer Sandbox already has the shared vocabulary:

`E < D < C < B < A < S < SS < SSS < X < XX`

Existing profile grading proves the correct architecture:

`authoritative raw state + named domain grading scheme -> derived grade metadata`.

The vocabulary is universal; the evaluator is **domain-specific**. The same grade letter must not imply the same raw scale for Character Strength, Item Durability, Location Prestige or Quest Difficulty.

Future grade profiles may expose multiple dimensions plus an optional overall grade.

Examples:

Character:
- overall;
- strength;
- agility;
- intelligence/skill dimensions as registered.

Item:
- overall;
- load/resistance;
- durability;
- quality/performance;
- complexity/handling where meaningful.

Location:
- overall;
- prestige/facility quality;
- hazard;
- complexity;
- other explicitly registered dimensions.

Quest/challenge:
- overall difficulty;
- combat/technical/social/other demand dimensions.

Grades should normally be deterministic derived values. AI supplies authoritative raw facts/specifications; registered grading schemes derive grades. If Creator override is later allowed for a grade, it must carry explicit provenance and must not silently replace raw physical truth.

Realistic universe profiles may cap legitimate grade/capability ranges by domain. Sandbox or future supernatural universes may represent SSS/X/XX or impossible capabilities. Future transmigration validation must reject unsupported grades/capabilities with zero target-universe writes.

---

## Grade versus requirement

Core invariant:

> **Item Grade describes the item. Requirement Grade describes the interaction.**

Example: a 55 lb fixed dumbbell may derive an `S` load/resistance grade under an Item scheme. That does **not** universally mean every interaction requires Character Strength `S`.

Requirement depends on the action context, for example:

`item specs + actor capability + action/exercise + workload/prescription + current state -> required capability / outcome`.

A 55 lb single-arm curl, two-hand goblet squat and simply moving the dumbbell to a rack may have different Character Strength requirements.

Do not hard-code Item grade as Character requirement unless a specific registered interaction contract explicitly defines that mapping.

---

## Universal requirement contract

Items, Locations, Quests, Actions and Equipment rules should consume one typed/composable requirement language instead of independent ad-hoc gates.

Requirement predicates may include:
- minimum grade in a named Character/domain dimension;
- minimum raw capability/value when appropriate;
- skill/equipment/item presence;
- authorization/ownership/residency;
- quest/state prerequisites;
- time/operating-state conditions;
- logical composition (`all`, `any`, explicit negation where justified).

Evaluation must produce deterministic pass/fail plus structured unmet requirements.

---

## Grade versus access policy

Grade is **not** authorization.

A Location may have a high grade yet be public and accessible to all. A private high-grade Location may reject a same-grade or higher-grade stranger. A lower-grade Character may enter a high-grade public facility if policy allows it.

Location access is a separate contract. Candidate policy families:
- public / access-to-all;
- private;
- owner/resident;
- authorized-only;
- grade-gated;
- quest/state-gated;
- composite.

Operating state is also separate from access policy: a public place can be closed; a private gate can be physically open but still restricted.

---

## Universal Item Schema v1 direction

Item schema must be detailed enough to support real-life-like scenario reasoning without hard-coded item-name behavior.

### Strict core dimensions

At minimum the ontology must support:
- stable identity and display name;
- definition family / variant identity;
- classification/category/subtype;
- description/source/provenance;
- stackable versus unique instance semantics;
- consumable versus non-consumable;
- movable/carriable versus fixed/installed;
- physical mass/weight;
- dimensions/size and occupied volume/space where meaningful;
- material/composition;
- condition, durability and serviceability where meaningful;
- ownership/location/container compatibility;
- capabilities/affordances;
- economic-value policy and price/value data;
- modifier/effect declarations only through registered deterministic semantics;
- grade profile derived through named schemes;
- compatibility/tags only through registered vocabularies.

### Strict conditional modules

Candidate modules include:
- container/storage;
- consumable;
- food/nutrition;
- wearable/equipment;
- tool;
- powered device/electronics;
- resistance/training equipment;
- vehicle;
- medical supply/device;
- other future modules only through explicit schema versions.

A module is not a free-form escape hatch. If selected, its required/optional fields and data types are exact.

### Item family and specification variants

Same semantic family can have many exact specification variants.

Example:
`Fixed Dumbbell` definition family -> 2 lb, 5 lb, 25 lb, 55 lb, etc.

Do not duplicate behavioral logic for every weight. The physical specification is authoritative and domain runtime derives interaction consequences.

### Effects are contextual

Items should generally expose intrinsic facts/capabilities rather than unconditional Character bonuses.

Bad default:
`55 lb dumbbell -> strength_gain +4`.

Preferred:
`mass/load + resistance capability + actor + exercise + reps/sets/tempo/ROM/rest/fatigue/history -> training stimulus`.

The same 2 lb dumbbell can be trivial for elite strength work yet useful for rehabilitation, warm-up or endurance contexts.

---

## Item creation and batch creation

Creator Studio must eventually support:
- one Item at a time;
- multiple Items in one batch;
- manual and AI modes through the same exact Item schema;
- definition-family/spec-variant creation where appropriate;
- per-item deterministic validation;
- explicit references/dependencies;
- safe preview/approval before Sandbox activation.

Batch format must remain a strict envelope containing individually strict Item payloads. Batch generation must not relax per-item validation.

Inventory/container operations after activation must support add/remove/move without redefining semantic identity.

---

## Economic value and asset integration

Creation work must reuse the existing valuation/economy contracts.

Core distinction remains:

`has economic value != contributes independent net worth`.

Every represented Item/Location/object that requires a value profile must explicitly classify its economic role and net-worth treatment instead of receiving accidental defaults.

Relevant classifications include standalone assets, components, consumable stock, resource proxies and economically immaterial objects. Replacement value, market value, purchase price and independent net-worth contribution remain separate concepts.

Sandbox creation may stage valuation metadata without affecting canonical net worth/economy until an explicit future compatible apply boundary.

---

## Universal Location Schema v1 direction

Location remains defined by the world contract as:

> **an identifiable spatial container with extent, contents, boundary/interface semantics, local state and explicit relationships to surrounding space.**

Location creation must support, without fabricating precision:
- identity/name/kind/classification;
- optional parent/structural containment;
- indoor/outdoor/exposure and known physical extent;
- boundary/interface/topology semantics;
- access policy and operating state separately;
- ownership/control/residency references where represented;
- local environment/state hooks;
- facilities/affordances;
- child locations;
- fixtures/structural objects;
- movable Item contents/resources;
- occupancy separately from structural containment;
- economic/asset value profile;
- domain-specific grade profile;
- provenance/canon/source status.

Do not overload relations:
- `contains` = structural/authored containment;
- `located_at` = dynamic physical presence;
- `stored_in` = mutable inventory containment;
- `owned_by` = legal/economic ownership;
- `carried_by` / `equipped_by` remain distinct.

Location creation may include existing/new Item contents in one Creator workflow, but those contents must resolve through Item schemas/instances rather than unvalidated embedded prose.

---

## Character × Item × Location runtime direction

A Sandbox Character becomes meaningfully runnable only when the represented environment supplies valid options.

Target chain:

`Character profile/capabilities`
`+ active Location/container`
`+ contained/available Items/facilities/resources`
`+ access/topology/environment state`
`+ cognition binding + Sandbox clock`
`-> deterministic affordances/options`
`-> cognition chooses among represented options`
`-> deterministic runtime validates and commits`

Location labels or Item names alone must not magically grant actions. Runtime options should derive from represented capabilities, facilities, resources and conditions.

---

## Active implementation slices

Detailed acceptance is maintained in `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`.

Current sequence:

1. **I5.2 — Creation Contract Audit & Reuse Map**
2. **I5.3 — Universal Quantity & Measurement Contract**
3. **I5.4 — Universal Cross-Domain Grade Contract**
4. **I5.5 — Universal Requirement & Access Contract**
5. **I5.6 — Universal Item Schema v1**
6. **I5.7 — Item Creation v1: Single**
7. **I5.8 — Item Batch Creation v1**
8. **I5.9 — Sandbox Item/Container Operations**
9. **I5.10 — Universal Location Schema v1**
10. **I5.11 — Location Creation + Embedded Contents**
11. **I5.12 — Location Contents Editing/Operations**
12. **I5.13 — Character ↔ Location Binding & Runtime Readiness**
13. **I5.14 — Item/Location Runtime Affordance Bridge**
14. **I5.15 — Sandbox Vertical Acceptance**

Do not collapse these into one broad rewrite merely for speed. Each slice should leave a runnable/testable contract while reusing existing world foundations.

---

## Creator Staging & Transmigration

Lifecycle/authority direction:

`Draft -> Sandbox Approved -> Sandbox Active -> Tested/Revised -> Ready for Transmigration -> Canonical Approved -> Canonical Active`.

Nothing transmigrates automatically.

Future transmigration must:
- freeze a source revision;
- compute dependency closure;
- choose a target-universe profile;
- validate grade/capability/system compatibility;
- generate deterministic proposed mutations;
- apply atomically only after Creator approval;
- produce zero target-universe writes on incompatibility/failure.

I6 remains planning/validation-only until the Creator explicitly changes that scope.

---

## Existing runtime locks

- W0-W5 plus Perception Foundation v1 remain the completed Real World external-input foundation.
- PR #278 protects Creator progression/profile overrides from seed/evidence snap-back.
- Full Sandbox autonomous ticking is **not implemented**.
- `runtime_ready != running` remains locked.
- Adrian Vale remains Creation Sandbox-only and is not canonical.
- The second canonical Character gate remains closed.
- Do not mutate the canonical Thorne Estate/world graph while implementing Sandbox creation foundations.

---

## Mind continuation

MIND-F2 remains deferred while the current Creator Creation vertical foundation is completed.

Later route remains:
`MIND-F2 -> F3 -> F4 -> F5 -> F6 -> F7 -> Foundation Completion Review v2 -> next real Character transmigration proposal`.

---

## Production evidence boundary

Repository implementation evidence is current through PR #322. PR #321 manual Character editing was live-tested successfully by the Creator. PR #322 merge/CI is verified, but its production deployment/live command-menu state is not independently verified here.

This roadmap update is documentation-only and does not itself require or imply a runtime deployment.

---

## Exact resume point

**Repository implementation checkpoint: PR #322 merged at `366f07b4a9e1cfd0670d768132e9500f10c51b44`; CI #1154 targeted mode passed 96 tests; main/test were synchronized at that merge. PR #321 manual Character field editing/prompt cleanup passed CI #1153 with 135 tests and Creator live Telegram verification. Character creation is sufficiently closed for the next dependency family. Active next slice is I5.2 — Creation Contract Audit & Reuse Map, followed by Quantity/Measurement, Universal Grade, Universal Requirement/Access, strict Universal Item Schema, single/batch Item Creation, Sandbox Item operations, strict Universal Location Schema, Location creation/contents operations, Character↔Location binding, runtime affordance bridge and vertical acceptance. Imperial is the default presentation system. AI must generate exact registered schemas only; no guessing/extra keys. Grades are derived through named domain schemes and are separate from interaction requirements and access authorization. Do not transmigrate Sandbox objects, mutate canonical Real World state, or start full Sandbox autonomous ticking as part of these slices.**
