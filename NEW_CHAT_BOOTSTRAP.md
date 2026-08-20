# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**  
Last synchronized: **2026-08-20**

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
5. task-relevant canonical docs/source
6. verified production/runtime evidence before live claims.

Authority order:
`current Creator instruction > current repo contracts/config/schema > verified live runtime/DB > CI/deploy evidence > bootstrap > remembered chat`.

Persistent branches: `main`, `test` only.

Workflow:
`develop on test -> focused tests -> PR/final CI -> merge to main -> runtime deploy if applicable -> verify production evidence -> sync continuity -> main/test exact synchronization`.

Do not claim production deployment from merge alone.

---

## Current implementation checkpoint

Latest merged runtime/source checkpoint:

### PR #326 — Universal Requirement & Access Foundation

Merged:
`2372a3a32f3b400a029317174fcf7260fee7f1f3`

Evidence:
- CI #1158 — **SUCCESS**;
- targeted 2 test files;
- **22 passed**;
- CLI init/status — **SUCCESS**;
- fresh DB healthy;
- schema version 21;
- no DB migration;
- no canonical world mutation.

`main` and `test` were synchronized to this merge before this docs-only continuity update.

---

## Newly completed Creator Item/Location foundation slices

### I5.2 — Creation Contract Audit & Reuse Map

Complete.

Contract:
`docs/CREATION_CONTRACT_REUSE_MAP_V1.md`.

Locked reuse decisions:
- generic Creation proposal envelope remains;
- Item/Location get strict type-specific validators beneath it;
- Creation Sandbox lifecycle/isolation remains;
- Item definition, concrete instance/stack, placement/storage and ownership remain separate concepts;
- existing inventory/value/grading/world-location semantics are reused through adapters;
- current Sandbox Character→Location `located_in` is prototype compatibility semantics, not the future universal relation; I5.13 must reconcile toward canonical `located_at` through Sandbox-owned persistence/adapters.

### I5.3 — Universal Quantity & Measurement Contract

PR #324 merged:
`a4abcbbcb932711bcf164d20bb977314afad5550`

Evidence:
- CI #1155 SUCCESS;
- 22 targeted tests passed;
- CLI init/status green;
- schema 21 healthy.

Contract:
`docs/UNIVERSAL_QUANTITY_MEASUREMENT_CONTRACT_V1.md`.

Implementation:
`src/observer_sandbox/physical_quantity.py`.

Provides presentation-independent normalized mass/length/area/volume truth with deterministic conversion.

Creator-facing default remains Imperial:
- lb;
- in;
- ft²;
- US gal.

Metric display is supported without changing physical truth.

Existing Character body/profile measurements and inventory stack persistence were not rewritten.

### I5.4 — Universal Cross-Domain Grade Contract

PR #325 merged:
`980a752160a48144ef91bf800c4f4ab8fc5bc98e`

Evidence:
- CI #1157 SUCCESS;
- **189 targeted tests passed**;
- existing Character/Profile grading regressions green;
- CLI init/status green;
- schema 21 healthy.

Contract:
`docs/UNIVERSAL_CROSS_DOMAIN_GRADING_CONTRACT_V1.md`.

Shared ordering:
`E < D < C < B < A < S < SS < SSS < X < XX`.

Existing Character RAPS/Skill/Body scheme ids and thresholds remain.

New cross-domain infrastructure:
- deterministic grade comparison;
- scheme domain/dimension metadata;
- optional read-time GradeProfile;
- explicit composite-only overall grade;
- Item resistance-load exemplar from normalized physical mass;
- Location completeness exemplar reusing L0-L4 spatial completeness.

Important:
- 55 lb can derive S Item resistance-load grade;
- that is not automatically a Character strength requirement;
- Location completeness grade is not authorization.

### I5.5 — Universal Requirement & Access Contract

Complete in PR #326.

Contract:
`docs/UNIVERSAL_REQUIREMENT_ACCESS_CONTRACT_V1.md`.

Implementation:
`src/observer_sandbox/requirements.py`.

Typed requirement leaves currently include:
- minimum grade by explicit domain/dimension;
- raw value compare;
- skill;
- Item presence;
- equipped Item;
- ownership;
- residency;
- authorization;
- state compare.

Composition:
- one leaf;
- nested `all`;
- nested `any`.

Access modes:
- public;
- owner_or_resident;
- authorized;
- restricted;
- explicit requirements.

Operating state is evaluated separately:
- open;
- closed;
- locked;
- blocked.

Core lock:

`Item Grade != interaction Requirement Grade != Location Access != Location operating state`.

Missing evidence and malformed contracts fail closed with structured reasons.

---

## Exact next implementation slice

**I5.6 — Universal Item Schema v1.**

Do this before Item Telegram creation UI.

Goal:
create one exact type-specific Item contract shared by Manual/AI, single/batch and later Location embedded-content creation.

Reuse:
- `docs/INVENTORY_ITEM_ARCHITECTURE.md`;
- `src/observer_sandbox/inventory.py` semantic split;
- `src/observer_sandbox/physical_quantity.py`;
- cross-domain grading in `grading.py`;
- `requirements.py`;
- `economic_value.py` policy semantics;
- generic creation envelope;
- Creation Sandbox isolation/lifecycle.

Canonical Item conceptual chain:

`universal definition -> concrete unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Do not collapse these into one arbitrary properties bag.

### I5.6 schema rules

Use:
`strict core + strict conditional modules`.

Required direction:
- exact registered core fields;
- module selection determines exact legal module fields;
- unknown AI-created fields reject;
- unique/stackable semantics explicit;
- physical quantities normalize through I5.3;
- Item grade derives only from registered I5.4 schemes;
- use/action requirements use I5.5 explicitly;
- economic policy uses existing classification/treatment semantics;
- placement/storage/ownership are relation facts, not reusable definition identity;
- Sandbox staging does not write canonical Item/inventory/economy tables.

Do not include broad future fields without a concrete represented use.

---

## Subsequent authorized route

After I5.6:

### I5.7 — Single Item Creation
`Manual/AI -> exact Item validator -> preview -> approve -> isolated Sandbox materialization`.

Single Item should use the same service boundary as batch size 1.

### I5.8 — Item Batch Creation
Heterogeneous exact Item proposals, internal references, whole-batch validation and atomic all-or-nothing apply.

### I5.9 — Sandbox Item / Container Operations
Browse/inspect/edit/move/store/own/carry/equip/quantity/archive/delete with explicit dependency handling.

### I5.10 — Universal Location Schema v1
Replace name-only arbitrary-properties Location prototype with strict spatial-container contract.

### I5.11 — Location Creation + Embedded Contents
Empty or furnished Location. Embedded new Items invoke the exact Item/batch contracts.

### I5.12 — Location Contents Operations
Add existing/new/batch Items, remove/move Items, create child Location. Preserve relation distinctions.

### I5.13 — Character ↔ Location Binding & Runtime Readiness
Reconcile Sandbox dynamic presence to canonical `located_at` semantics; require a usable place rather than a name-only Location.

### I5.14 — Item / Location Runtime Affordance Bridge
Legal options derive from represented fixtures/items/resources/environment/capabilities/access/requirements rather than Location labels or model invention.

### I5.15 — Sandbox Vertical Acceptance
Prove strict Character + usable Location + typed Items + correct relations + economics + binding/readiness/options with canonical fingerprint unchanged.

Full Sandbox autonomous ticking remains separately unauthorized.

---

## Existing Character creation locks

Character creation remains the strictness exemplar:
- AI fills exact creation-owned schema;
- registered data types are authoritative;
- runtime/derived fields excluded;
- skills are sparse relevant canonical rows;
- Manual and AI exact field-set parity;
- section editing remains in current section after accepted input;
- consumed prompt cards are removed;
- Sandbox profile browser/edit/grade-target parity exists;
- Real/Sandbox runtime controls remain isolated.

Do not loosen Character exactness for Item/Location convenience.

---

## Sandbox / canonical isolation

Creation Sandbox objects do not count as canonical Real World entities.

Do not write Sandbox Item/Location creation into canonical:
- `entity_definitions`;
- `entities`;
- `inventory_stacks`;
- ordinary canonical relations;
- economic value/asset/account/net-worth tables;
- Real World scheduler/runtime state.

Sandbox may reuse the same semantic contracts through Sandbox-owned adapters/storage.

`canonical_state_fingerprint()` remains the important zero-mutation acceptance tool.

---

## Staging/transmigration locks

Lifecycle:
`Draft -> Sandbox Approved -> Sandbox Active -> Tested/Revised -> Ready for Transmigration -> Canonical Approved -> Canonical Active`.

Nothing transmigrates automatically.

I6 remains planning/validation only unless the Creator explicitly changes scope.

Adrian Vale remains Sandbox-only and must not be transmigrated as a side effect of this work.

The second real Character gate remains closed.

---

## Runtime status

Real World and Sandbox clocks/speed/pause are separate.

`runtime_ready != running` remains locked.

Full Sandbox autonomous ticking is still not implemented.

The current I5.3-I5.5 changes are foundation source changes; do not infer production deployment from merge/CI alone. Verify push/deploy/boot evidence separately before any live-runtime claim.

---

## Exact resume point

**Latest merged implementation is PR #326 at `2372a3a32f3b400a029317174fcf7260fee7f1f3`; CI #1158 passed 22 targeted tests, CLI init/status green and schema 21 healthy. I5.2 Creation Reuse Map, I5.3 Quantity/Measurement, I5.4 Cross-Domain Grading and I5.5 Requirements/Access are complete. Next: I5.6 Universal Item Schema v1. Implement the exact schema/validator first; do not build Item Telegram creation UI yet; preserve definition/instance/stack/relation/economic separation and zero canonical mutation.**
