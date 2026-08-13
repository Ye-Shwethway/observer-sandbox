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
- Development proceeds by minimum runnable vertical slices.
- Repeated expansion follows **exemplar-first, then batch-by-pattern**: prove one new structural pattern, then batch equivalent follow-ons into one PR, one pre-merge disposable production-copy dry-run, and one deploy/readback.

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
No accumulated stimulus, strength/skill progression, hypertrophy/body measurements, grading, or tiers are implemented.

## Post-P3.5 stabilization

- Autonomy Breadth + Time Observability v1 — DEPLOYED / ACCEPTANCE VERIFIED.
- Current Action ETA Observability v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Runtime Speed Control v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Deterministic Action Duration Planning Profiles v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Minimum action timing invariant — CI VERIFIED: `1 sim min @ 3600x` remains a positive `1/60` real-second due interval.

## Selective Activity/Action Semantics

### Research v1 — exemplar
Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.

- first-class `research` action, legal 10–180m;
- Research Desk only;
- preferred 30–90m;
- existing capability/colocation validation and first-class action/event persistence reused;
- model vocabulary can now pick semantic verbs exposed by authoritative action options;
- no knowledge, XP, memory or progression subsystem.

Evidence: PR #10 merge `c50f4cf9a87b15589be3b3ea4878990da7e69d02`; Research Action Semantics Acceptance #1 / `31681716339` SUCCESS; Deploy #136 / `31681760620` SUCCESS.

### Activity Semantics Batch 1 — Monitor
Status: COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED.

Research v1 established the structural pattern. Batch 1 then applied the same pattern across three equivalent console affordances in one development cycle:
- Surveillance Console;
- Secure Communications Terminal;
- Emergency Console.

`monitor` contract:
- first-class action;
- legal duration 5–120m;
- preferred planning 15–45m;
- local object + `monitor` capability + colocation;
- passive physiology/time plus ordinary first-class action/event evidence only;
- no findings, alerts, communications payload, intelligence engine or environment engine.

Batch execution evidence:
- one branch/PR (#11);
- PR CI #374 / `31682656794` SUCCESS;
- **pre-merge** Activity Semantics Batch 1 Acceptance #1 / `31682656839` SUCCESS on one disposable copy of live production DB, covering all three targets, zero model calls, unsupported Media Console rejected;
- PR #11 merged at `8a8f14b7da13ac0ab0ecbb461fefcdfc3639d7f8` only after the batch was green;
- release `5e650c11ef6c144f4816f3d77704562cba3156d6`;
- Deploy #137 / `31682743508` SUCCESS;
- production readback healthy: schema v4, autonomy enabled/normal/unpaused, Gemini preserved, Telegram connected, speed 5x at that snapshot.

This validates the new expansion policy. Do not return to one-PR/one-deploy-per-equivalent-item expansion unless rollback/risk boundaries require it.

## Next planned sequence

Do not add more verbs just for breadth. `maintain/repair/diagnose/practice` may require distinct state or consequences and should become new exemplars only when a concrete runnable need appears.

Unless Creator redirects:
1. first read-only grading proof on one existing raw value;
2. minimum training stimulus evidence on one target/domain;
3. minimum adaptation/progression only after stimulus + recovery semantics are explicit.

## Deferred boundaries

Not implemented:
- accumulated stimulus/adaptation;
- attribute/skill/body-measurement progression;
- universal grading/tier evaluation;
- inventory/resource depletion;
- rich memory/relationship/environment engines;
- exterior/Tahoe traversal;
- schema v5.

## Current resume point

The exemplar-first/batch expansion workflow is proven and Monitor Batch 1 is live. The next proposed bounded feature is the **first read-only grading proof on one existing raw value**; no implementation should begin until Creator direction confirms that next slice.
