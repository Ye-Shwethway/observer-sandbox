# Creator Creation Systems — Minimum Implementation Plan v1

Status: **APPROVED IMPLEMENTATION PLAN — BROAD ITEM GRADING LIVE ACCEPTANCE ACTIVE**  
Date: 2026-08-20

## Objective

Build Creator Creation through bounded reusable contracts that create realistic Sandbox content without mutating canonical Real World state.

Core rules:
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.** `runtime_ready != running`.
- AI fills/proposes structured facts; deterministic services validate, derive and mutate.
- Real World and Creation Sandbox mutable state remain isolated.
- Universal systems expose expandable sockets rather than one hard-coded implementation per entity family.

---

## Current accepted Item boundary

### Fresh Item Edit

PR #358 merged at `9c93739655fc6981a8c5bfd31a7c83a4cce16f62`; CI #1194. Creator live-confirmed current fresh approved Item Edit works.

### Universal Grading Socket Architecture v1

PR #360 merged at `9155a94bc75b800d4a10f2a39993647c78d11d9c`; CI #1195.

Canonical contract:
`docs/UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md`.

Provides:
- evaluator registry (`EvaluatorSpec`)
- dimension registry (`DimensionSpec`)
- reference profile registry (`ReferenceProfile`)
- universe grading policy (`UniverseGradingPolicy`)
- rebuildable `GradePlan`
- deterministic/read-time `GradeProfile`

Creator live-confirmed the deployed grading section on an existing Item before broad coverage expansion.

### PR #362 — Broad Item Grading Coverage Foundation

Merged at:
`b2b2d0b058bd9835cd311b78586b4ee3b09534ef`

CI **#1198** ✅ — 112 selected test files + CLI smoke.

Canonical contract:
`docs/ITEM_GRADING_COVERAGE_FOUNDATION_V1.md`.

#### Raw Item Metrics socket

`definition.modules.metrics` is now a sparse registry-driven raw-fact module.

Initial metric ids:
- `luminous_flux`
- `runtime`
- `power`
- `energy_capacity`
- `range`
- `speed`
- `data_rate`
- `digital_storage`
- `beam_distance`
- `water_resistance_depth`
- `charge_time`
- `payload_capacity`

Each registry entry defines label, canonical unit, supported input units/conversions and numeric constraints. Unknown metric ids/units reject. Normalized metrics revalidate across persistence/Edit boundaries.

Container capacity and resistance load remain in their established modules and are not duplicated.

#### AI creation integration

Single and Batch Creator AI complete forms derive nullable metric slots from the registry. Canonicalization removes null slots. Prompts direct AI to map supported measurable specs into registered metrics while leaving unknowns null.

AI must not author:
- final grades
- thresholds
- evaluator ids
- reference profiles
- unknown metrics

#### Expanded realistic Item grading coverage

Current deterministic magnitude dimensions:
- resistance load
- storage capacity
- luminous flux
- runtime
- power
- energy capacity
- range
- speed
- data rate
- digital storage
- beam distance
- water-resistance depth
- payload capacity

`charge_time` is represented but intentionally not given a monotonic-high grade because lower is normally preferable.

Grades describe **named capability magnitude**, not overall quality/safety/efficiency. Overall Item Grade remains absent without explicit composite semantics.

#### UI / Edit

Draft and approved Item detail render performance metrics and grading. Metrics are persisted raw facts; grades remain rebuildable interpretation.

Existing Item Edit recursively traverses Modules, so nested metric value/unit fields are editable without metric-family editor code. Apply still goes through strict current `item-v1` validation and existing `update_sandbox_item()` semantics.

No DB migration. No canonical Real World writes.

---

## Universal grading contract

Vocabulary:
`E < D < C < B < A < S < SS < SSS < X < XX`.

Rules:
- raw represented facts remain authority;
- arbitrary numeric fields are not automatically gradeable;
- no evidence/reference => ungraded rather than invented precision;
- universe policy gates dimensions/evaluators/references/ceilings;
- AI may provide structured evidence but deterministic evaluator owns the final grade;
- **Item Grade describes the item. Requirement Grade describes the interaction.**
- Location grade remains separate from access authorization;
- overall grade requires explicit composite semantics;
- future additions should normally be registry/socket additions, not Item-family branching.

---

## Completed Creator foundation — do not rebuild

- I0 Creator authority hardening
- I1 universal creation proposal/socket core
- I2 isolated Creation Sandbox persistence/lifecycle
- I2.5 Sandbox clock/speed/pause/readiness/AI binding
- I3 Character + Location representation proof
- I4 Creator Studio proposal lifecycle
- I4.1 Sandbox Character configuration UX
- I5/I5.1 Sandbox Observer foundations
- Character Manual/AI + profile/edit/grade-target parity
- explicit Real/Sandbox runtime controls
- I5.2 reuse map
- I5.3 universal quantity/measurement
- I5.4 cross-domain grading
- I5.5 requirements/access
- I5.6 Universal Item Schema v1
- I5.7 single Sandbox Item materialization
- I5.8 atomic heterogeneous Item Batch
- I5.9 Item/container operations
- I5.10 Universal Location Schema v1
- Item Creator Studio Single/Batch AI/manual flows
- realism/self-correction, economic valuation, human review + raw export
- approved Item detail
- Item edit/save parity + diagnostics
- atomic Character+Item cleanup
- Universal Grading Socket v1
- broad Item Metrics + Grading Coverage Foundation v1

Locked Item ontology:
`Item Definition -> concrete unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Relations retain distinct `contains`, `located_at`, `stored_in`, `owned_by`, `carried_by`, `equipped_by` semantics. Ownership never follows automatically from location/storage.

---

# CURRENT ACCEPTANCE SLICE

## Representative live proof before mass fresh Item generation

Creator explicitly requested a broad foundation first so large Item catalogs do not have to be regenerated later.

Repository foundation is accepted, but **do not mass-generate fresh Items yet**.

After PR #362 deployment:
1. generate one small representative fresh batch only;
2. cover several classes, preferably container + flashlight/device + battery/power item + resistance/load item;
3. verify known measurable specs populate structured metrics/modules instead of prose only;
4. verify Preview shows human normalized metrics and deterministic grades;
5. verify absent evidence remains honestly ungraded;
6. approve and verify approved details preserve the same semantics;
7. edit one metric-bearing Item -> Preview -> Apply -> Done;
8. verify pre-edit Sandbox pause state restores;
9. verify Real World/canonical state remains unchanged.

If this representative live pass succeeds, broad normal Item generation may resume. Later new dimensions should be additive socket registrations; old Items must never receive invented backfills for raw facts they do not contain.

---

# NEXT AFTER REPRESENTATIVE ITEM ACCEPTANCE

## I5.11 — Sandbox Location Creation + Embedded Contents

Required semantics:
- active same-Sandbox parent validation
- acyclic structural parent graph
- structural parent uses `contains`
- interface destinations validate active same-Sandbox Locations
- embedded Items reuse I5.6/I5.8 contracts/services/storage
- movable Items normally use `located_at`, unless exact graph establishes `stored_in` a typed container
- validate complete Location + contents graph before writes
- atomic whole-graph success or zero partial graph
- no automatic runtime readiness
- no autonomous ticking
- no canonical writes

Then I5.12 Location Contents Operations -> I5.13 Character ↔ Location Binding & Runtime Readiness -> I5.14 Item/Location Runtime Affordance Bridge -> I5.15 Sandbox Vertical Acceptance.

---

## I6 / Character locks

Transmigration remains planning-only. Nothing transmigrates automatically. Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed. Existing Character parity contracts stay locked. Full Sandbox autonomous ticking remains separately unauthorized.

---

## Exact resume point

**PR #362 merged at `b2b2d0b058bd9835cd311b78586b4ee3b09534ef`; CI #1198 passed 112 selected test files + CLI smoke. Broad Item grading foundation now includes registry-driven raw metrics, AI metric fill/canonicalization, expanded realistic magnitude dimensions, performance-metrics UI and metric Edit/revalidation compatibility. Hold mass fresh generation until #362 is deployed and one representative multi-class batch + metric Edit/Apply/Done live pass succeeds. Then normal Item generation can resume and I5.11 follows.**
