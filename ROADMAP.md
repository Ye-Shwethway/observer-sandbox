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

P3.5 completes the current short-term training loop:
`target -> readiness -> fatigue inefficiency -> effectiveness -> effective workload -> immediate physiology`.
No accumulated stimulus, strength/skill progression, hypertrophy/body measurements, grading, or tiers are implemented.

## Post-P3.5 stabilization

### Autonomy Breadth + Time Observability v1
Status: DEPLOYED / ACCEPTANCE VERIFIED / LIVE OBSERVATION POSITIVE.
World object breadth expanded 15→27 and broader estate use has been observed live.

### Current Action ETA Observability v1
Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
Character and Runtime surfaces expose pending target, duration, expected simulated completion and approximate remaining real time.

### Runtime Speed Control v1
Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
Global speed may change while actions are running; remaining wall time is rescheduled without cancelling/replanning. Creator verified a 60-sim-minute action at 30x. Speed is not a fixed baseline and must be read live; Deploy #136 later observed 5x.

### Deterministic Action Duration Planning Profiles v1
Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
Broad persisted legality ranges stay compatible while newly model-planned actions use narrower deterministic preferred ranges. Sleep remains intentionally unclamped until nap/night-sleep semantics are separated.

### Minimum action timing invariant
Status: CI VERIFIED.
Action duration remains integer simulated minutes with minimum 1 minute. `1 sim min @ 3600x` yields a positive `1/60` real-second due-time delta and safely transitions from in-progress before due to complete after due. No extra wall-delay clamp or sub-minute time unit is needed now.

## Selective Activity/Action Semantics

### Research v1
Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.

Canonical detail: `docs/RESEARCH_ACTION_SEMANTICS.md`.

Delivered:
- first-class `research` action, legal duration 10–180m;
- Research Desk is the only authored research target;
- preferred Research Desk planning duration 30–90m;
- generic capability/colocation validation and first-class action/event persistence reused;
- model vocabulary now includes semantic verbs currently exposed by authoritative action options;
- ordinary passive physiology/time only; no knowledge, XP, memory or progression subsystem.

Evidence: PR #10 merge `c50f4cf9a87b15589be3b3ea4878990da7e69d02`; PR CI #365 / `31681648655` SUCCESS; main CI #366 / `31681716298` SUCCESS; Research Action Semantics Acceptance #1 / `31681716339` SUCCESS; release `8f3487feccc84ef10b045dff960097bc0c44ceb6`; Deploy #136 / `31681760620` SUCCESS.

### Next semantic candidate — Monitor

The next bounded semantic slice should add `monitor` to the existing Surveillance Console only. It should reuse schema-v4 action definitions/capabilities, duration planning, model option-derived vocabulary, validation and first-class events. It may represent purposeful surveillance observation but must not invent a full intelligence findings, alert, environment, or world-event subsystem.

After `monitor`, decide whether another semantic verb is actually useful before adding one. `maintain` is a safer later candidate than `repair`, because repair would require a concrete damaged-state invariant.

## Later sequence

After bounded activity semantics, unless Creator redirects:
1. first read-only grading slice on one existing raw value;
2. minimum training stimulus evidence on one target/domain;
3. minimum adaptation/progression only after stimulus + recovery semantics are explicit.

Later/demand-driven: inventory/depletion, soreness/injury, detailed exercise programming, rich memory/relationships, environment, P5 second character, Tahoe traversal.

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

Research v1 is deployed. Continue with **Minimum Monitor Action Semantics** as the next bounded activity slice. Do not broaden it into an intelligence/environment subsystem.
