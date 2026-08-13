# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then `ROADMAP.md`, then task-relevant contracts.

Authority: current Creator instruction > canonical repo/contracts > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > older chat/memory.

## Development policy

Use minimum runnable expansion, plus the repository-wide **exemplar-first, then batch-by-pattern** rule in `AGENTS.md`.

For a new structural pattern: prove one small exemplar end-to-end. Once that invariant is green/deployed, structurally equivalent follow-ons should normally use one branch/PR, one focused test suite, one **pre-merge disposable production-copy dry-run covering the whole batch**, iterative fixes if needed, then merge only when the whole batch is green, followed by one deploy/readback. Items requiring a new state/authority/runtime invariant leave the batch and become a new exemplar.

## Production baseline

- repo `Ye-Shwethway/observer-sandbox`
- VPS `/opt/observer-sandbox`
- DB `/var/lib/observer-sandbox/observer.sqlite3`
- systemd `observer-sandbox`
- SQLite schema v4
- world root `world_observer_universe`
- estate `loc_thorne_estate`
- world revision `thorne-estate-v3.0-scoped-ids`
- Darian autonomy enabled / normal / wake-on-demand
- global speed is Creator-controlled and must be re-read live; Deploy #137 observed `5x`
- Gemini cognition binding preserved
- Telegram connected private Creator observer

Production continues autonomously. Re-read live state whenever exact current Darian action/stats/speed matter.

## Canonical runtime rule

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`

LLMs propose structured actions only. Deterministic runtime owns legality and mutation.

## Proven feature state

- P2.2 Browse the Sandbox — COMPLETE / LIVE UX VERIFIED.
- P2.3.1 Restore Basic Stats — COMPLETE / LIVE UX VERIFIED.
- P3.1 Systemic Training Fatigue / Recovery — COMPLETE / LIVE UX VERIFIED.
- P3.2 Targeted Training Session — COMPLETE / ACCEPTANCE VERIFIED.
- P3.3 Training Readiness Modifier — COMPLETE / DEPLOYED / LIVE UX VERIFIED.
- P3.4 Training Effectiveness Outcome — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- P3.5 Effective Training Load — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Autonomy Breadth + Time Observability v1 — DEPLOYED / ACCEPTANCE VERIFIED.
- Current Action ETA Observability v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Runtime Speed Control v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Deterministic Action Duration Planning Profiles v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Research Action Semantics v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Activity Semantics Batch 1 (`monitor`) — COMPLETE / PRE-MERGE PRODUCTION-COPY ACCEPTANCE VERIFIED / DEPLOYED.

## Activity semantics state

`research` remains the exemplar semantic verb: Research Desk only, legal 10–180m, preferred 30–90m.

Batch 1 proves the batching policy on the same invariant. `monitor` is first-class, legal 5–120m, preferred 15–45m, and is authored on exactly three console targets:
- Surveillance Console;
- Secure Communications Terminal;
- Emergency Console.

All three use the same local-object capability/colocation validation, model option-derived vocabulary, passive physiology/time behavior and first-class action/event persistence. No findings, alerts, communications payloads, intelligence engine or environment subsystem is created.

Pre-merge evidence: PR #11 branch CI #374 / `31682656794` SUCCESS and Activity Semantics Batch 1 Acceptance #1 / `31682656839` SUCCESS against one disposable copy of the live production DB, covering all three targets with zero model calls and rejecting an unsupported Media Console.

Merge/release: PR #11 merge `8a8f14b7da13ac0ab0ecbb461fefcdfc3639d7f8`; release `5e650c11ef6c144f4816f3d77704562cba3156d6`; Deploy #137 / `31682743508` SUCCESS. Deploy readback: service healthy, schema v4, autonomy enabled/normal/unpaused, speed 5x at snapshot, Gemini preserved, Telegram connected.

## Time and planning state

Action duration remains integer simulated minutes with minimum 1 minute. Regression coverage proves `1 sim min @ 3600x` schedules a positive `1/60` real-second delay and completes safely. Sleep remains intentionally unclamped until nap/night-sleep semantics are separated.

## Exact resume point

The exemplar-first/batch expansion pattern is now proven in production. Do not keep adding semantic verbs merely to fill vocabulary. `maintain/repair/diagnose/practice` each risk requiring materially different state or consequences and should become new exemplars only when a concrete runnable need exists.

Unless Creator redirects, resume the planned sequence with the **first read-only grading proof on one existing raw value**, preserving raw authoritative values and deriving any grade from a named scheme without schema v5.
