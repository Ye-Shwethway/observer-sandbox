# Creator Creation Systems — Minimum Implementation Plan v1

Status: **APPROVED IMPLEMENTATION PLAN — ITEM GRADING COVERAGE EXPANSION ACTIVE**  
Date: 2026-08-20

## Objective

Build Creator Creation through bounded reusable contracts that create realistic Sandbox content without mutating canonical Real World state.

Core rules:
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.** `runtime_ready != running`.
- AI fills/proposes structured facts; deterministic services validate, derive and mutate.
- Real World and Creation Sandbox mutable state remain isolated.
- Universal systems should expose expandable sockets instead of requiring one hard-coded implementation per entity family.

---

## Current accepted Item boundary

### Fresh Item Edit

PR #358 merged at `9c93739655fc6981a8c5bfd31a7c83a4cce16f62`; CI #1194 passed.

Creator subsequently live-confirmed fresh approved Item Edit works. The earlier `modules.physical.mass.kind` error was a validator idempotence bug: authoring `{value,unit}` normalized/persisted to `{kind,value,unit}` but was not reaccepted. Current validation accepts its own normalized representation only with the correct physical dimension and keeps arbitrary extras invalid.

### Universal Grading Socket Architecture v1 + Item Coverage v1

PR **#360** merged at:
`9155a94bc75b800d4a10f2a39993647c78d11d9c`

CI **#1195** passed targeted regression + CLI smoke.

Canonical contract:
`docs/UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md`.

Core invariant:
`authoritative raw state + registered grading sockets + universe policy -> derived GradePlan -> deterministic GradeProfile`.

Implemented extension points:
- evaluator registry (`EvaluatorSpec`);
- dimension registry (`DimensionSpec`);
- reference-profile registry (`ReferenceProfile`);
- universe grading policy (`UniverseGradingPolicy`);
- rebuildable `GradePlan`;
- deterministic/read-time `GradeProfile` resolver.

V1 Item adapter/UI:
- full Creator draft payloads normalize through the strict current Item validator before grading;
- approved Items use their normalized persisted facts directly;
- current `resistance_load` dimension reuses `item-resistance-load-v1`;
- 55 lb-equivalent resistance remains S;
- draft review and approved Item detail can render `Resistance Load: S · Expert`;
- ordinary Items with no registered applicable dimension show an explicit ungraded state;
- no fabricated overall Item grade;
- raw `.txt` export remains technical authoring data and does not gain GradePlan authority;
- no DB migration or new persisted GradePlan/grade authority.

The default realistic-universe policy is explicit/fail-closed. Future supernatural dimensions are not automatically accepted simply because they are registered.

PR #360 live Telegram rendering remains separately evidence-gated until deployment/Creator verification.

---

## Universal grading contract

Canonical vocabulary:
`E < D < C < B < A < S < SS < SSS < X < XX`.

Rules:
- shared vocabulary, domain-specific raw meaning/evaluators;
- grades derive from authoritative raw facts;
- arbitrary numbers are not automatically gradeable;
- no evidence/reference => ungraded rather than invented precision;
- overall grades require explicit composite semantics;
- universe policy controls allowed dimensions/evaluators/reference profiles/ceilings;
- **Item Grade describes the item. Requirement Grade describes the interaction.**
- no automatic Item-grade -> Character-requirement mapping;
- Location grade is separate from access authorization;
- AI may later propose applicability mappings, but all ids must resolve through registries/policy/evidence and final grade remains deterministic.

Normal extension pattern:
`EvaluatorSpec + DimensionSpec + optional ReferenceProfile + UniverseGradingPolicy allowance`.

Do not add central Item-family branching such as backpack/flashlight/sword-specific grading code.

---

## Completed Creator foundation — do not rebuild

- I0 Creator authority hardening;
- I1 universal creation proposal/socket core;
- I2 isolated Creation Sandbox persistence/lifecycle;
- I2.5 Sandbox clock/speed/pause/readiness/AI binding;
- I3 Character + Location representation proof;
- I4 Creator Studio proposal lifecycle;
- I4.1 Sandbox Character configuration UX;
- I5/I5.1 Sandbox Observer foundations;
- Character Manual/AI + profile/edit/grade-target parity;
- explicit Real/Sandbox runtime controls;
- I5.2 reuse map;
- I5.3 universal quantity/measurement;
- I5.4 cross-domain grading;
- I5.5 requirements/access;
- I5.6 Universal Item Schema v1;
- I5.7 single Sandbox Item materialization;
- I5.8 atomic heterogeneous Item Batch;
- I5.9 Item/container operations;
- I5.10 Universal Location Schema v1;
- Item Creator Studio Single/Batch AI/manual flows;
- Item realism/self-correction, human review + raw export;
- approved Item detail/economic presentation;
- Sandbox Item edit/save parity + diagnostics;
- atomic Character+Item Sandbox cleanup;
- human-friendly Item money display;
- Universal Grading Socket Architecture v1 + first Item socket coverage.

Locked Item ontology:
`Item Definition -> concrete unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Relations retain distinct `contains`, `located_at`, `stored_in`, `owned_by`, `carried_by`, `equipped_by` semantics. Ownership never follows automatically from location/storage.

---

# CURRENT DEVELOPMENT FAMILY

## Item Grading Coverage expansion

V1 proves the scalable socket architecture but does **not** claim exhaustive grading for all possible Items. Only evidence-backed registered dimensions receive grades.

Next bounded work:
1. verify PR #360 grading display live when deployed;
2. inventory current Item schema/modules for additional raw properties that already support defensible grading semantics;
3. add reusable evaluator/dimension/reference registrations only where their meaning is grounded;
4. if generation-time semantic classification is useful, add a strict structured AI GradePlan applicability proposal;
5. AI-proposed ids must already exist in the registries and be permitted by the active universe policy;
6. deterministic evaluator remains final grade authority;
7. uncovered Items remain valid and explicitly ungraded;
8. do not invent durability/quality/efficiency/category baselines without underlying raw facts and evaluator/reference authority;
9. overall Item grade remains deferred until a defensible explicit composite contract exists, including critical-dimension and missing-evidence behavior.

This work should make future dimensions easy to add without rewriting Item creation/materialization/UI navigation core.

---

# NEXT AFTER Item Grading Coverage checkpoint

## I5.11 — Sandbox Location Creation + Embedded Contents

Objective: materialize strict I5.10 Locations in isolated Sandbox state, optionally with typed Item contents, while reusing Item contracts rather than inventing a Location-only contents model.

Required semantics:
- active same-Sandbox parent validation;
- acyclic structural parent graph;
- structural parent uses `contains`;
- interface destinations validate active same-Sandbox Locations;
- embedded Items reuse I5.6/I5.8 contracts/services/storage;
- movable Items normally use `located_at`, unless exact graph establishes `stored_in` a typed container;
- validate complete Location + contents graph before writes;
- atomic whole-graph success or zero partial graph;
- no automatic runtime readiness;
- no autonomous ticking;
- no canonical writes.

Then I5.12 Location Contents Operations -> I5.13 Character ↔ Location Binding & Runtime Readiness -> I5.14 Item/Location Runtime Affordance Bridge -> I5.15 Sandbox Vertical Acceptance.

---

## I6 / Character locks

Transmigration remains inactive/planning-only. Nothing transmigrates automatically. Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed. Existing Character parity contracts stay locked. Full Sandbox autonomous ticking remains separately unauthorized.

---

## Test / release policy

- smallest relevant tests while iterating;
- socket acceptance must prove new registrations can be added without resolver-core edits;
- universe-policy tests must prove unauthorized dimensions do not auto-enter a universe;
- UI is human-readable; technical export may preserve raw canonical/authoring representation;
- PR CI is repository acceptance gate;
- deploy/live behavior is verified separately from merge;
- continuity docs update after material work and persistent branches exact-sync after acceptance.

---

## Exact resume point

**Creator live-confirmed fresh Item Edit works after PR #358. PR #360 merged at `9155a94bc75b800d4a10f2a39993647c78d11d9c` with CI #1195 green. Universal Grading Socket v1 now provides evaluator/dimension/reference/universe-policy sockets plus rebuildable GradePlan and deterministic GradeProfile; current Item resistance-load grading is registry-driven and uncovered Items remain explicitly ungraded. Continue evidence-backed Item Grading Coverage through socket registrations and, where useful, registry/policy-constrained AI applicability planning. Do not hard-code Item families or fabricate reference scales. Resume I5.11 after the grading-coverage checkpoint.**
