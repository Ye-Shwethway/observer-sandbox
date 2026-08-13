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
- Schema v4 is the current composable foundation. Do not introduce schema v5 without a concrete missing invariant.
- Development proceeds by minimum runnable vertical slices, not subsystem-first expansion.

## Foundation / P0 / P1

- Foundation schema v4 — COMPLETE.
- P0 Foundation & Remote Control — COMPLETE / LIVE VERIFIED.
- P0.5 AI Provider Layer — FOUNDATION COMPLETE; Darian preserves configured Gemini cognition.
- P1 Living Darian Minimum — CONTINUOUS AUTONOMY LIVE / ENGINE HARDENING PASSED.

## P2 — Telegram Observer

- P2.1 Mobile Observer MVP — LIVE.
- P2.2 Browse the Sandbox — COMPLETE / LIVE UX VERIFIED.
- P2.3.1 Restore Basic Stats — COMPLETE / LIVE UX VERIFIED.

Creator controls remain typed and audited; do not expand them into arbitrary editing/admin-console behavior.

## P3 — Richer Simulation Vertical Slices

- P3.1 Systemic Training Fatigue / Recovery — COMPLETE / LIVE UX VERIFIED.
- P3.2 Targeted Training Session — COMPLETE / ACCEPTANCE VERIFIED.
- P3.3 Training Readiness Modifier — COMPLETE / DEPLOYED / LIVE UX VERIFIED.
- P3.4 Training Effectiveness Outcome — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- P3.5 Effective Training Load — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.

P3.5 completes the current short-term loop:
`target -> readiness -> fatigue inefficiency -> effectiveness -> effective workload -> immediate physiology`.

No accumulated stimulus, strength/skill progression, hypertrophy/body measurements, grading, or tiers are implemented.

## Post-P3.5 stabilization — Autonomy Breadth + Time Observability v1

Status: DEPLOYED / ACCEPTANCE VERIFIED / LIVE OBSERVATION PARTIAL.

Canonical detail: `docs/AUTONOMY_BREADTH_TIME_OBSERVABILITY.md`.

Delivered:
- world object breadth expanded from 15 to 27 instances across the existing estate topology;
- seven previously sparse non-kitchen purposeful rooms acceptance-proven to expose legal targets;
- Darian policy v1.4 discourages serial same-room inspect/use loops and default kitchen-appliance behavior;
- normal guidance prefers quick inspect 2–6 sim min and simple use 2–10 while persisted compatibility bounds remain unchanged;
- proactive Character Update completion messages expose completed duration and, when normal next planning succeeds, mandatory next action/duration/expected-update information;
- time semantics remain linear and runtime-owned.

Creator production observation already confirmed Darian moved beyond the Kitchen into the Living Room; deploy #133 later observed him training in the Top-Class Home Gym. Long-run diversity remains an observational property rather than deterministic CI evidence.

## Post-P3.5 stabilization — Current Action ETA Observability v1

Status: COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / CREATOR LIVE UX VERIFICATION PENDING.

Canonical detail: `docs/CURRENT_ACTION_ETA_OBSERVABILITY.md`.

Character `/darian`, `/watch`, character-browser card and Runtime `/status` now show, for an existing pending action:
- friendly target;
- planned simulated duration;
- approximate full real wait at recorded planning speed;
- expected simulated completion timestamp;
- approximate remaining real time from durable `due_wall_time`.

No pending action means no invented ETA. This is presentation-only: no time advance, scheduler mutation, action change or schema change.

Evidence:
- PR #7 merge `17200b1468753f17f10e3951b2f2c474bef32989`;
- PR CI #344 / `31678482152` SUCCESS;
- main CI #346 / `31678671631` SUCCESS;
- Current Action ETA Acceptance #2 / `31678671655` SUCCESS on candidate code + config against disposable production DB copy, zero model calls;
- release commit `70399f872ca35960989c3257a0735eb063b26253`;
- Deploy #133 / `31678730719` SUCCESS with service healthy, schema v4, normal/unpaused/1x autonomy, pending action preserved, Gemini binding preserved, Telegram connected.

The first ETA acceptance attempt failed only because candidate staging omitted `config/`; no failed candidate was deployed.

## Current architecture opportunities — discussion candidates, not authorization

The existing v4 foundation is sufficient for the next bounded slices. Current bottlenecks are behavior/domain semantics rather than a missing general runtime foundation.

Potential next directions to discuss:

1. **Deterministic action-duration planning profiles** — separate safe planning/preferred ranges from broad persisted legality bounds so routine inspect/use/read/move/etc. durations are consistently realistic without invalidating existing pending actions.
2. **Autonomy decision quality / recent-action anti-repeat refinement** — recent event context already exists in cognition. Improve only if live behavior shows repetition remains despite current event window and v1.4 guidance; do not build a full memory engine just for short-term repetition.
3. **Selective activity vocabulary/world affordance expansion** — add concrete action semantics or fixtures only where generic `inspect/use/read/train` proves too shallow in production; avoid adding objects merely to inflate choice count.
4. **Training progression architecture** — before body measurements or attributes mutate, explicitly design stimulus/adaptation semantics and their relation to recovery/effective workload. Current effectiveness/effective-minutes are sockets, not progression authorization.
5. **First grading slice** — grading is derived from raw authoritative values and should begin in one narrow domain only when a concrete progression/requirement/view needs it; schema v4 does not need a broad grading rewrite first.
6. **Later systems** — inventory/depletion, P4 rich memory/relationships, P5 second production character, environment, Tahoe traversal remain demand-driven and later unless live behavior creates a concrete need.

## Deferred boundaries

Not implemented:
- deterministic action-duration planning profiles;
- accumulated stimulus/adaptation;
- attribute/skill/body-measurement progression;
- soreness/injury or detailed exercise programming;
- inventory/resource depletion;
- universal grading/tier evaluation;
- rich memory/relationship/environment engines;
- exterior/Tahoe traversal;
- schema v5.

## Current resume point — CREATOR DISCUSSION

Current-action ETA observability is deployed. **Do not automatically implement another slice.** Review current architecture and live behavior with the Creator and select the next minimum-runnable direction explicitly.

Preserve schema v4, 1x wake-on-demand autonomy, globally scoped ids, actor-scoped scheduler state, first-class actions/events, Telegram presentation rules, profile/runtime separation, typed/audited Creator control, and incremental expansion only through explicitly authorized minimum-runnable needs.
