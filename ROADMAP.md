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

Creator controls remain typed/audited; no arbitrary admin console.

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

World object breadth expanded from 15 to 27 across the existing estate. Darian has been observed live beyond the Kitchen, including Living Room and Top-Class Home Gym. Generic short-inspect/use guidance and proactive next-action timing are live.

### Current Action ETA Observability v1
Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.

Character and Runtime surfaces expose pending target, duration, expected simulated completion and approximate remaining real time.

### Runtime Speed Control v1
Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.

Global speed may change while actions are running. Remaining wall time is rescheduled without cancelling/replanning the action. Pause freezes countdown. Creator live test verified a 60-sim-minute Heavy Bag session at `30x` with roughly 2 real minutes total wait.

Evidence: PR #8 merge `1799dd7c7723866ec15dc29a05c682de8e1d5e4a`; Runtime Speed Control Acceptance #1 / `31679969684` SUCCESS; Deploy #134 / `31680016710` SUCCESS.

### Deterministic Action Duration Planning Profiles v1
Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.

Canonical detail: `docs/DURATION_PLANNING_PROFILES.md`.

Broad persisted legality ranges remain unchanged for compatibility. Newly model-planned actions receive narrower preferred duration profiles and are deterministically normalized to the nearest preferred bound when the model requests an implausible duration.

Representative profiles:
- inspect 2–6m; Refrigerator/Pantry inspect 2–5m;
- simple use 2–10m; Stove use 10–30m;
- read 20–60m; Research Desk read 20–90m;
- train 30–90m; Heavy Bag 20–45m; Free Weights 45–90m; Combat Mat/Practice Dummy 20–60m.

Sleep remains intentionally unclamped until nap and overnight-sleep semantics are separated.

Evidence: PR #9 merge `4d7d949002a4444f6ae6424e502fa872f6d90a33`; PR CI #357 / `31680626619` SUCCESS; main CI #358 / `31680683357` SUCCESS; Duration Planning Profiles Acceptance #1 / `31680683416` SUCCESS; release `1130b2ec09c456293cdb7e6a5451cef15deffa56`; Deploy #135 / `31680728818` SUCCESS.

## Next — Selective Activity/Action Semantics

This is the approved next direction after duration profiles.

Current vocabulary remains intentionally small:
`move, sleep, eat, drink, shower, rest, inspect, use, train, read, idle`.

The next work should add one or two meaningful semantic actions only where generic `use` or `inspect` is visibly too shallow. Candidate domains from the current estate include:
- `research` — Research Desk / information work;
- `monitor` — Surveillance Console / Emergency Console;
- `maintain` or `repair` — Workshop Bench / Equipment Bench;
- `practice` — future distinction from broad physical `train` if a concrete need is proven.

Do not add all candidates at once. Each new verb should have a concrete capability/target, planning duration, validation path, first-class action/event persistence, focused tests, disposable acceptance, deployment and live observation.

## Later sequence

After activity semantics, unless Creator redirects:
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

Duration Planning Profiles v1 is deployed. Next bounded feature should be **Selective Activity/Action Semantics**, starting with the smallest high-value verb rather than another foundation rewrite or broad object expansion.
