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
- Reuse established Real World semantics through adapters instead of cloning ontologies.
- Grades are derived interpretation, not persisted competing truth.
- Item grade, actor requirement, Location access and Location operating state remain distinct.
- `runtime_ready != running`.

---

## Current repository checkpoint

Latest merged implementation:

### PR #332 — I5.10 Universal Location Schema v1

Merge: `d670ac8e7a1ee3beaa6001011d8b04383c39533c`  
Final head: `aaf17efb4e142a5b3691bbd1eba1c9502c39143b`

Evidence:
- CI #1164 SUCCESS;
- **126 passed / 22 selected files**;
- CLI init/status green;
- fresh DB healthy;
- schema 21.

`main` and `test` synchronized to this merge before continuity work.

---

## Creator Creation foundation status

### I5.2 — Reuse Map — COMPLETE

`docs/CREATION_CONTRACT_REUSE_MAP_V1.md`

Keep generic proposal/lifecycle; add exact type validators/adapters. Preserve Item definition/instance/stack/relation/economic separation and world relation meanings.

### I5.3 — Quantity / Measurement — COMPLETE

PR #324 `a4abcbbcb932711bcf164d20bb977314afad5550`; CI #1155, 22 passed.

Normalized SI truth for mass/length/area/volume; Imperial-default Creator display; display conversion does not mutate truth.

### I5.4 — Cross-Domain Grading — COMPLETE

PR #325 `980a752160a48144ef91bf800c4f4ab8fc5bc98e`; CI #1157, 189 passed.

Grade order:
`E < D < C < B < A < S < SS < SSS < X < XX`.

Character schemes remain compatible. Item resistance load and Location completeness are explicit separate schemes.

### I5.5 — Requirements / Access — COMPLETE

PR #326 `2372a3a32f3b400a029317174fcf7260fee7f1f3`; CI #1158, 22 passed.

Typed requirements + nested all/any. Location access policy remains separate from operating state.

### I5.6 — Universal Item Schema — COMPLETE

PR #328 `5820aad0f4abf5efb4b352071cbb67ee8056071b`; CI #1159, 74 passed / 11 files.

Strict Item core + bounded modules: physical, stack, nutrition, container, resistance training. Unknown schema surface fails closed.

### I5.7 — Single Sandbox Item Creation — COMPLETE

PR #329 `74d83bc6d50a61a76becb41bc53d6cc65b354257`; CI #1160, 89 passed / 17 files.

Atomic Sandbox Item definition/instance/economic/relation materialization. Canonical state untouched.

### I5.8 — Heterogeneous Item Batch — COMPLETE

PR #330 `716b56e64fa106f633c13c55de9211a7a67e5c8b`; CI #1161, 88 passed / 15 files.

Single path = batch size 1. Write-free preview, forward `$ref` storage, cycle/dependency validation, whole-batch transaction.

### I5.9 — Item / Container Operations — COMPLETE

PR #331 `d4b60e5fdd18706cbd60da8cdde556226c826efe`; CI #1162, 99 passed / 18 files.

Browse/edit/move/store/own/carry/equip/quantity/archive/delete. Shared definitions protected. Incoming dependencies require explicit detach. Sandbox reset clears shared Item definitions too.

### I5.10 — Universal Location Schema — COMPLETE

PR #332 `d670ac8e7a1ee3beaa6001011d8b04383c39533c`; CI #1164, 126 passed / 22 files.

Strict spatial-container schema:
- identity/kind;
- parent/exposure;
- optional normalized extent;
- access + separate operating state;
- explicit interfaces/topology;
- facilities/resources/capabilities;
- minimal represented environment;
- optional economic policy;
- provenance;
- derived L0-L4 completeness/grade.

Unknown precision stays unknown. Structural parentage never implies traversal.

---

## Locked ontology

### Item

`Definition -> unique instance OR stack -> physical placement/storage -> ownership/carriage/equipment -> runtime state/history`

### Relations

- `contains` — structural/static spatial containment;
- `located_at` — dynamic physical presence;
- `stored_in` — inventory/container storage;
- `owned_by` — ownership;
- `carried_by` — carriage;
- `equipped_by` — equipped state.

Do not infer ownership from presence/storage. Do not use `contains` for ordinary movable inventory.

### Grade / access

`Item Grade != actor Requirement != Location Access != Location operating state`.

### Sandbox

All Creator Item/Location mutable state must remain Sandbox-owned. Continue zero-canonical-mutation acceptance with `canonical_state_fingerprint()`.

---

## Active dependency chain

Completed:

`I5.2 reuse -> I5.3 quantity -> I5.4 grading -> I5.5 requirements/access -> I5.6 Item schema -> I5.7 single Item -> I5.8 batch -> I5.9 Item operations -> I5.10 Location schema`

Next:

`I5.11 Location creation + embedded contents -> I5.12 contents operations -> I5.13 Character/Location binding/readiness -> I5.14 runtime affordances -> I5.15 vertical acceptance`.

---

## I5.11 — Sandbox Location Creation + Embedded Contents — NEXT

### Objective

Materialize one strict I5.10 Location into isolated Sandbox state, optionally with typed Item contents, without creating a parallel Item model.

### Empty Location path

`Location payload -> I5.10 validation -> relation/topology/economic validation -> preview -> atomic Sandbox materialization`.

### Furnished/populated Location path

`Location payload + contents manifest -> I5.10 validation + I5.6/I5.8 Item validation -> whole graph preview -> atomic apply`.

### Required semantics

- active same-Sandbox parent when `parent_ref` is resolved;
- structural parent graph acyclic;
- parent uses structural `contains`, not `located_at`;
- explicit interface destinations validate active same-Sandbox Locations when resolved;
- Location access/economic/topology state stored only in Sandbox-owned persistence;
- embedded unique/movable Items use `located_at` to the Location unless their exact manifest says `stored_in` another typed container;
- fixed structural fixtures may use structural containment only when the composition contract explicitly marks them structural;
- Item definitions/instances/economics reuse I5.6-I5.9 services/storage;
- validate the complete graph before Item/Location writes;
- whole Location+contents apply succeeds or fails atomically;
- no automatic `runtime_ready` and no autonomous execution.

Do not allow Location generation to invent an arbitrary unvalidated `contents` properties bag.

### Acceptance target

Prove:
- empty strict Location;
- furnished Location with unique Item + stack/container relationship;
- parent and interface target validation;
- parent-cycle failure;
- invalid embedded Item means zero new Location/Item graph;
- economic/access/topology data remain Sandbox-only;
- canonical fingerprint unchanged.

---

## I5.12 — Location Contents Operations

Support add existing Item, create Item, create Item batch, move/remove Item and create child Location. Preserve relation distinctions and explicit dependency policies.

---

## I5.13 — Character ↔ Location Binding & Runtime Readiness

Reconcile legacy Sandbox Character `located_in` toward canonical `located_at` through Sandbox-owned adapters/persistence.

A Location name alone is insufficient. Target readiness should require an active **usable** represented place, conceptually L3+, plus explicit AI binding/runtime dependencies unless implementation evidence requires a narrower rule.

---

## I5.14 — Runtime Affordance Bridge

Executable options derive from machine-readable Item/fixture capabilities, resources, environment, access and explicit requirements. Location labels and LLM plausibility do not create actions.

---

## I5.15 — Vertical Acceptance

Prove a complete isolated Sandbox vertical:
- exact Character;
- exact usable Location;
- typed contents;
- correct relations/economics;
- binding/readiness;
- deterministic legal options;
- canonical fingerprint unchanged.

Full Sandbox autonomous ticking remains separately unauthorized.

---

## Transmigration / Character locks

Nothing transmigrates automatically. I6 remains planning/validation only unless Creator expands scope.

Adrian Vale remains Sandbox-only. The second real Character gate remains closed.

Character Manual/AI exact parity and existing Sandbox profile/edit/grade-target behavior must not be weakened by Item/Location work.

---

## Runtime / deploy evidence boundary

PR/CI evidence above proves repository acceptance only. Do not claim current production deployment or live Telegram behavior from these merges without separate deploy/boot evidence.

---

## Exact resume point

**PR #332 merged at `d670ac8e7a1ee3beaa6001011d8b04383c39533c`; CI #1164 passed 126 tests across 22 selected files, CLI init/status green, schema 21 healthy. I5.2–I5.10 are complete. Next: I5.11 Sandbox Location Creation + Embedded Contents. Reuse the strict I5.10 Location validator and I5.6/I5.8 Item contracts, validate parent/topology/content dependencies before one atomic Sandbox apply, preserve relation meanings, do not infer runtime readiness, and do not mutate canonical Real World state.**
