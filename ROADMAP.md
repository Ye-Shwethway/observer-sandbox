# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-13

## Product principles

- Python/SQLite runtime/world state is authoritative.
- AI proposes structured cognition; it never directly mutates arbitrary world state.
- Telegram is a Creator-facing observer/control adapter, not a simulation engine.
- Cognition remains wake-on-demand; no periodic LLM heartbeat by default.
- Canonical runtime composition:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Schema v4 remains the current composable foundation. Do not introduce schema v5 without a concrete missing invariant.
- Repeated expansion follows **exemplar-first, then batch-by-pattern**: prove one structural pattern, then batch equivalent follow-ons into one PR, one pre-merge disposable production-copy dry-run, and one deploy/readback.

## Foundation / P0 / P1

- Foundation schema v4 — COMPLETE.
- P0 Foundation & Remote Control — COMPLETE / LIVE VERIFIED.
- P0.5 AI Provider Layer — FOUNDATION COMPLETE; Darian preserves configured Gemini cognition.
- P1 Living Darian Minimum — CONTINUOUS AUTONOMY LIVE / ENGINE HARDENING PASSED.

## P2 — Telegram Observer

- P2.1 Mobile Observer MVP — LIVE.
- P2.2 Browse the Sandbox — COMPLETE / LIVE UX VERIFIED.
- P2.3.1 Restore Basic Stats — COMPLETE / LIVE UX VERIFIED.

## P3 — Richer Simulation Vertical Slices

- P3.1 Systemic Training Fatigue / Recovery — COMPLETE / LIVE UX VERIFIED.
- P3.2 Targeted Training Session — COMPLETE / ACCEPTANCE VERIFIED.
- P3.3 Training Readiness Modifier — COMPLETE / DEPLOYED / LIVE UX VERIFIED.
- P3.4 Training Effectiveness Outcome — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- P3.5 Effective Training Load — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.

P3.5 short-term training loop:
`target -> readiness -> fatigue inefficiency -> effectiveness -> effective workload -> immediate physiology`.
No accumulated stimulus, strength/skill progression, hypertrophy/body measurements, or adaptation yet.

## Post-P3.5 stabilization

- Autonomy Breadth + Time Observability v1 — DEPLOYED / ACCEPTANCE VERIFIED.
- Current Action ETA Observability v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Runtime Speed Control v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Deterministic Action Duration Planning Profiles v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Minimum action timing invariant — CI VERIFIED.

## Selective Activity/Action Semantics

### Research v1 — exemplar
Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.

### Activity Semantics Batch 1 — Monitor
Status: COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED.

`monitor` is authored on Surveillance Console, Secure Communications Terminal and Emergency Console with the same capability/colocation/action-event invariant. No findings/intelligence/environment subsystem was added.

Evidence: PR #11 merge `8a8f14b7da13ac0ab0ecbb461fefcdfc3639d7f8`; acceptance `31682656839`; Deploy #137 `31682743508` SUCCESS.

## Read-only grading

### Grading exemplar — Strength
Status: COMPLETE / PRE-MERGE ACCEPTANCE VERIFIED / DEPLOYED.

- raw `raps_pa.strength = 90` remains authoritative and unchanged;
- named proof scheme `raps-100-proof-v1` derives `Grade S`;
- grade is query/presentation metadata, not a second source of truth;
- Telegram Attributes displays raw value plus derived grade;
- no schema change.

Evidence: PR #12 merge `d0bdabc1faaede8adb6c3e8dd29a9b5ff9ba3cb3`; Read-Only Grading Proof Acceptance #1 `31683547092`; Deploy #138 `31683632205` SUCCESS.

### Attribute Grading Batch 1
Status: COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED.

The Strength exemplar pattern is expanded to **36 explicitly opted-in compatible 0..100 Attributes-section fields**.

Boundaries:
- `raps_ia.iq` is excluded because it uses a different scale;
- `Skills` collection is excluded and requires its own grading family;
- `Body` measurements/composition are excluded and require a **separate exemplar + batch** because units, normalization and calculation semantics differ materially;
- explicit field membership prevents future numeric fields from silently inheriting this scheme;
- raw profile values remain unchanged.

Evidence: PR #13 merge `76bcf7fe7225a9504909f9d939bbcdd673bac7c6`; CI #386 SUCCESS; Attribute Grading Batch 1 Acceptance #3 `31683936844` SUCCESS; release `d14cae7ef88fc9e157caa5fa0b930f36aba3cf77`; Deploy #139 `31684009154` SUCCESS.

## Grading family rule

Do not use one numeric evaluator merely because multiple domains contain numbers.

- 0..100 compatible Attributes: current `raps-100-proof-v1` family.
- IQ: separate scale/evaluator if grading becomes useful.
- Skills: separate family because progression/experience semantics may differ.
- Body measurements/composition: separate exemplar and batch; evaluator may need units, body composition, stature/proportion context and/or genetic ceilings rather than flat thresholds.

## Next planned sequence

The current grading architecture is proven without schema v5. Before long-term training progression:
1. define/prove the separate **Body grading family** only if Creator wants body grades now; do not reuse attribute thresholds by default;
2. otherwise proceed to **minimum training stimulus evidence** on one target/domain;
3. minimum adaptation/progression only after stimulus + recovery semantics are explicit.

## Deferred boundaries

Not implemented:
- accumulated stimulus/adaptation;
- attribute/skill/body-measurement progression;
- body-measurement grading evaluator;
- IQ/skills grading evaluators;
- inventory/resource depletion;
- rich memory/relationship/environment engines;
- exterior/Tahoe traversal;
- schema v5.

## Current resume point

Attribute Grading Batch 1 is live. Body measurements are explicitly a separate grading family. The next implementation decision is **Body grading exemplar** versus **Minimum Training Stimulus**, with body grading requiring its own calculation design rather than inheriting the attribute evaluator.
