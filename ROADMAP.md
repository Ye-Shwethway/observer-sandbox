# Observer Sandbox Roadmap

Status: **ACTIVE**  
Roadmap synchronized: **2026-08-20**

## Operating principles

- Current Creator instruction, live repo/schema, verified runtime/DB and current CI/deploy evidence outrank remembered chat context.
- AI proposes structured facts; deterministic contracts validate, derive and mutate.
- Telegram is observer/control, never simulation authority.
- **Create anywhere safely; canon nowhere automatically.**
- **Schema-valid does not imply universe-compatible.**
- **Created is not alive.** `runtime_ready != running`.
- Universal systems use expandable registry/socket patterns rather than family-specific switchboards.
- `canonical_state_fingerprint()` remains a high-value zero-canonical-mutation invariant.

---

## Current repository checkpoint

### Fresh Item Edit

Creator live-confirmed PR #358 works. Fresh approved Items enter Item Edit and revalidate current normalized physical quantities correctly.

### PR #360 — Universal Grading Socket v1

Merged `9155a94bc75b800d4a10f2a39993647c78d11d9c`; CI #1195 ✅.

Provides evaluator/dimension/reference/universe-policy sockets, rebuildable GradePlan and deterministic GradeProfile. Creator live-confirmed deployed Item grading UI on an existing Item.

### PR #362 — Broad Item Grading Coverage Foundation

Merged:
`b2b2d0b058bd9835cd311b78586b4ee3b09534ef`

CI **#1198** ✅ — 112 selected test files + CLI smoke.

Canonical contract:
`docs/ITEM_GRADING_COVERAGE_FOUNDATION_V1.md`.

Foundation now adds a generic sparse `definition.modules.metrics` socket backed by `ItemMetricRegistry` rather than one schema module per Item family.

Initial metric evidence catalog:
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
- charge time
- payload capacity

Provider AI forms derive metric slots from the registry. Null slots are removed. Known supported specs can be mapped into metrics; unknown values remain null. AI never authors final grades, thresholds, evaluator ids or reference profiles.

Expanded realistic Item grading dimensions:
- resistance load
- storage capacity from existing container volume
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

`charge_time` is represented but intentionally not graded monotonic-high because lower is normally preferable.

These grades describe **capability magnitude**, not generic quality. Overall Item Grade remains deferred until an explicit defensible composite exists.

Draft + approved Item UI now exposes performance metrics and derived grades. Metrics persist as raw facts; GradePlan/Profile remain read-time/rebuildable. Existing recursive Item Edit exposes nested metric value/unit fields and strict validator re-entry is acceptance-tested.

No DB migration. No canonical Real World writes.

---

## Universal grading locks

Vocabulary:
`E < D < C < B < A < S < SS < SSS < X < XX`.

Rules:
1. raw represented facts remain authority;
2. arbitrary numeric fields are not automatically gradeable;
3. registered evaluator/dimension/reference/universe policy controls grading semantics;
4. missing evidence/reference -> ungraded, not invented precision;
5. realistic universe does not auto-admit supernatural dimensions;
6. AI may fill/propose represented facts but deterministic evaluator owns final grade;
7. **Item Grade describes the item; Requirement Grade describes the interaction**;
8. Location grade is not access authorization;
9. overall grade requires explicit composite semantics;
10. new coverage should normally be added by registration, not resolver or Item-family rewrites.

---

## Completed Creator foundation — retained

I5.2–I5.10 remain complete:
- I5.2 Creation Contract Reuse Map
- I5.3 Universal Quantity / Measurement
- I5.4 Universal Cross-Domain Grading
- I5.5 Requirements / Access
- I5.6 Universal Item Schema v1
- I5.7 Single Sandbox Item materialization
- I5.8 Atomic heterogeneous Item Batch
- I5.9 Item / Container Operations
- I5.10 Universal Location Schema v1

Item Creator Studio retains strict Single/Batch AI/manual creation, realism/self-correction, economic valuation, human review + raw export, approved details, Item Edit parity/diagnostics, and Character/Item cleanup.

Locked Item ontology:
`Definition -> unique instance OR stack -> placement/storage -> ownership/carriage/equipment -> runtime state/history`.

Relations remain distinct: `contains`, `located_at`, `stored_in`, `owned_by`, `carried_by`, `equipped_by`. Ownership is orthogonal to physical placement/storage.

---

# CURRENT ACCEPTANCE — broad grading foundation live proof

Creator explicitly requested avoiding large Item regeneration until foundation is broad enough.

Therefore **do not mass-generate fresh Items yet**.

Required representative live sequence after PR #362 deployment:
1. create one small fresh multi-class batch only;
2. include representative container + flashlight/device + battery/power + resistance/load Item where practical;
3. verify known quantitative specs populate structured modules/metrics rather than prose only;
4. verify normalized performance metrics in draft detail;
5. verify deterministic applicable grades and honest ungraded state where evidence is absent;
6. approve and verify approved details retain the same metrics/grades;
7. live-edit one metric-bearing Item -> Preview -> Apply -> Done;
8. verify pre-edit pause state restoration;
9. verify Real World/canonical state unchanged.

If this representative live gate passes, the broad grading foundation is accepted for normal fresh Item generation. Further future dimensions can be added through sockets without changing existing creation/navigation core, though newly desired raw facts not represented on an old Item may still require explicit edit rather than invented backfill.

---

# NEXT AFTER REPRESENTATIVE ITEM ACCEPTANCE

### I5.11 — Sandbox Location Creation + Embedded Contents

Required semantics remain:
- strict I5.10 Location materialization;
- active same-Sandbox parent validation;
- acyclic structural parent graph;
- structural parent uses `contains`;
- interface destinations validate active same-Sandbox Locations;
- embedded Items reuse I5.6/I5.8 contracts;
- movable Items normally use `located_at`, or exact `stored_in` typed containers;
- validate whole Location + contents graph before writes;
- atomic apply/rollback;
- no automatic runtime readiness;
- no autonomous execution;
- no canonical writes.

Then I5.12 Location Contents Operations -> I5.13 Character/Location Binding & Runtime Readiness -> I5.14 Runtime Affordance Bridge -> I5.15 Sandbox Vertical Acceptance.

---

## Transmigration / Character locks

Nothing transmigrates automatically. I6 remains planning/validation only unless Creator expands scope. Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed. Existing Character parity stays locked. Full Sandbox autonomous ticking remains separately unauthorized.

---

## Exact resume point

**PR #362 merged at `b2b2d0b058bd9835cd311b78586b4ee3b09534ef`; CI #1198 is green across 112 selected test files + CLI smoke. Broad Item grading foundation now has registry-driven raw metrics, provider AI metric fill, deterministic normalization, 13 realistic Item magnitude dimensions including existing resistance load/storage capacity, human metrics+grading UI, and Item Edit revalidation compatibility. Hold mass Item generation until #362 deploys and one representative multi-class fresh batch + metric Edit/Apply/Done live pass succeeds. Then resume normal Item generation and proceed to I5.11.**
