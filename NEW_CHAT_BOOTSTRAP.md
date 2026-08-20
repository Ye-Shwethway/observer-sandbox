# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**  
Last synchronized: **2026-08-20**

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. `docs/CREATOR_CREATION_IMPLEMENTATION_PLAN_V1.md`
5. `docs/UNIVERSAL_GRADING_SOCKET_ARCHITECTURE_V1.md`
6. `docs/ITEM_GRADING_COVERAGE_FOUNDATION_V1.md`
7. task-relevant canonical contracts/source
8. current branch/PR/CI/runtime evidence before completion or live claims.

Authority:
`current Creator instruction > live repo contracts/config/schema > verified runtime/DB > CI/deploy evidence > continuity docs > remembered chat`.

Persistent branches: `main`, `test` only.
Workflow: `test -> focused verification -> PR/CI -> merge main -> deploy/runtime verification when applicable -> continuity sync -> exact main/test sync`.
Do not infer production deployment from merge alone.

---

## Current checkpoint

### Fresh Item Edit — live PASS

PR #358 merged at `9c93739655fc6981a8c5bfd31a7c83a4cce16f62`; CI #1194 passed. Creator live-confirmed fresh approved Item Edit now works. Current validator accepts both authoring `{value,unit}` and its own normalized `{kind,value,unit}` representation only with the correct physical dimension.

### Universal Grading Socket v1 — accepted

PR #360 merged at `9155a94bc75b800d4a10f2a39993647c78d11d9c`; CI #1195 passed.

Core invariant:
`authoritative raw state + registered grading sockets + universe policy -> derived GradePlan -> deterministic GradeProfile`.

Sockets:
- `EvaluatorSpec`
- `DimensionSpec`
- `ReferenceProfile`
- `UniverseGradingPolicy`
- rebuildable `GradePlan`
- deterministic `GradeProfile`

Creator subsequently live-verified the deployed Item detail Grading section on an existing LED Camping Flashlight. It correctly showed explicit ungraded state because that old Item had no registered structured grading evidence.

### PR #362 — broad Item Grading Coverage Foundation — repository accepted

Merged at:
`b2b2d0b058bd9835cd311b78586b4ee3b09534ef`

CI **#1198** ✅ — 112 selected test files + CLI smoke.

Canonical contract:
`docs/ITEM_GRADING_COVERAGE_FOUNDATION_V1.md`.

New raw evidence socket:
`definition.modules.metrics`.

Initial metric registry:
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

Strict deterministic unit normalization is registry-driven. Unknown metric ids/units reject. AI provider forms are generated from the same metric registry and null slots canonicalize away.

Current realistic Item grading dimensions now include:
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

`charge_time` is raw evidence only in v1 because lower is normally preferable; no fake monotonic-high grade is produced.

Grades describe **named capability magnitude**, not vague overall quality. Overall Item Grade remains intentionally absent without an explicit composite contract.

Draft and approved Item views now expose human-facing performance metrics followed by deterministic grading. Metrics remain raw persisted facts; grades remain rebuildable interpretation. Item Edit's existing recursive Modules editor naturally exposes metric value/unit fields and strict revalidation remains authoritative.

No DB migration. No new canonical Real World mutation path.

---

## Generation hold / live acceptance gate

Creator explicitly requested foundation completion **before** broad fresh Item generation to avoid expensive later regeneration.

Therefore do **not** mass-generate fresh Items yet.

Before broad generation resumes:
1. verify deployed runtime includes PR #362 or later;
2. create one small representative fresh multi-class batch only;
3. include several classes such as a container, flashlight/device, battery/power item and training/load item;
4. verify known measurable specs enter structured metrics/modules instead of remaining only in prose;
5. verify draft metrics + dimension grades;
6. approve and verify the same semantics on approved Item details;
7. live-edit one metric-bearing Item through Preview -> Apply -> Done;
8. verify Sandbox pause restoration and Real World/canonical isolation.

Only after this representative live pass should broad Item generation resume.

---

## Grading locks

Canonical grade vocabulary:
`E < D < C < B < A < S < SS < SSS < X < XX`.

Rules:
- raw facts are authority;
- evaluator/dimension/reference/universe-policy registrations are sockets;
- unknown evidence/reference means ungraded, not fabricated precision;
- AI never owns final grade letters/thresholds;
- realistic-universe policy must not auto-admit supernatural dimensions;
- **Item Grade describes the item. Requirement Grade describes the interaction.**
- Location grade remains separate from access authorization;
- overall grade requires explicit composite semantics.

---

## Retained locks / next major feature

I5.2 through I5.10 remain complete and must not be rebuilt. Item ontology/relations, Sandbox isolation, no automatic transmigration, `runtime_ready != running`, canonical fingerprint safety and no unauthorized full Sandbox autonomous ticking remain locked.

After the Item grading representative live acceptance gate closes, resume **I5.11 — Sandbox Location Creation + Embedded Contents**.

Adrian Vale remains Sandbox-only. Second Real World Character gate remains closed.

---

## Exact resume sentence

**PR #362 merged at `b2b2d0b058bd9835cd311b78586b4ee3b09534ef` after CI #1198 passed 112 selected test files + CLI smoke. Broad Item grading foundation now includes registry-driven raw metrics, AI metric fill, deterministic normalization, expanded realistic magnitude dimensions, performance-metrics UI and Edit/revalidation compatibility. Do not mass-generate fresh Items yet; verify #362 deployment with one small representative multi-class fresh batch and one metric Edit/Apply/Done pass. If that live gate passes, broad fresh Item generation can resume before I5.11.**
