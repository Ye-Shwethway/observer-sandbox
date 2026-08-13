# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then `ROADMAP.md`, then task-relevant contracts.

Core/runtime/schema/action: `docs/ARCHITECTURE.md` + `docs/COMPOSABLE_RUNTIME_ARCHITECTURE_AUDIT.md`.
Spatial: `docs/WORLD_LOCATION_NODE_MODEL.md`.
Character/profile: `docs/CHARACTER_PROFILE_SCHEMA.md`.
Telegram: `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md` + `docs/TELEGRAM_NOTIFICATION_POLICY.md`.
Creator controls: `docs/CREATOR_CONTROL_POLICY.md`.
Needs/training: `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`, `docs/P3_3_TRAINING_READINESS_MODIFIER.md`, `docs/P3_4_TRAINING_EFFECTIVENESS.md`, `docs/P3_5_EFFECTIVE_TRAINING_LOAD.md`.
Autonomy breadth/time: `docs/AUTONOMY_BREADTH_TIME_OBSERVABILITY.md`.
Current-action timing: `docs/CURRENT_ACTION_ETA_OBSERVABILITY.md`.
Future grading: `docs/FUTURE_GRADING_SYSTEM.md`.

Authority: current Creator instruction > canonical repo/contracts > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > older chat/memory. Never conflate committed, CI-validated, acceptance-verified, deployed, DB-applied, and Creator-live-verified states.

## Development policy

Use minimum runnable expansion:
`minimum required state -> minimum behavior/evidence -> minimum Creator-facing surface -> focused tests -> disposable acceptance -> deploy/readback -> Creator acceptance -> next slice`.

Do not pre-build large inventory, grading, memory, relationship, environment, combat, training, or regional systems merely because extension sockets exist.

## Production baseline

- repo `Ye-Shwethway/observer-sandbox`
- VPS `/opt/observer-sandbox`
- DB `/var/lib/observer-sandbox/observer.sqlite3`
- systemd `observer-sandbox`
- SQLite schema v4
- world root `world_observer_universe`
- estate `loc_thorne_estate`
- world revision `thorne-estate-v3.0-scoped-ids`
- Darian autonomy enabled / normal / unpaused / 1x / wake-on-demand
- Gemini cognition binding preserved
- Telegram connected private Creator observer

Production continues autonomously. Re-read live state whenever exact current Darian action/stats matter.

## Canonical runtime rule

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`

LLMs propose structured actions only. Deterministic runtime owns legality and mutation. First-class action instances/events preserve target, modifiers, outcome, state changes, location, participants and timing evidence.

## Proven feature state

- P2.2 Browse the Sandbox — COMPLETE / LIVE UX VERIFIED.
- P2.3.1 Restore Basic Stats — COMPLETE / LIVE UX VERIFIED.
- P3.1 Systemic Training Fatigue / Recovery — COMPLETE / LIVE UX VERIFIED.
- P3.2 Targeted Training Session — COMPLETE / ACCEPTANCE VERIFIED.
- P3.3 Training Readiness Modifier — COMPLETE / DEPLOYED / LIVE UX VERIFIED.
- P3.4 Training Effectiveness Outcome — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- P3.5 Effective Training Load — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Autonomy Breadth + Time Observability v1 — DEPLOYED / ACCEPTANCE VERIFIED; Creator already observed broader location use, but diversity remains observational rather than deterministic CI truth.
- Current Action ETA Observability v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / CREATOR LIVE UX VERIFICATION PENDING.

P3.5 completes the current short-term training loop:
`target -> readiness -> fatigue inefficiency -> effectiveness -> effective workload -> immediate physiology`.
It does not implement accumulated stimulus, attribute/skill gain, body-measurement progression, grading, or tiers.

## Current Action ETA evidence

Character `/darian`, `/watch`, character-browser card, and Runtime `/status` now show pending target, planned duration, expected simulated completion and approximate remaining real time when a pending action exists. No ETA is invented when no action is pending. Simulation time/scheduler semantics are unchanged.

Evidence:
- PR #7 merge `17200b1468753f17f10e3951b2f2c474bef32989`;
- PR CI #344 / `31678482152` SUCCESS;
- main CI #346 / `31678671631` SUCCESS;
- Current Action ETA Acceptance #2 / `31678671655` SUCCESS on candidate code + config and disposable production DB copy, zero model calls;
- release commit `70399f872ca35960989c3257a0735eb063b26253`;
- Deploy #133 / `31678730719` SUCCESS;
- production readback healthy: schema v4, autonomy enabled/normal/unpaused/1x, pending action preserved, Gemini preserved, Telegram connected.

The first ETA acceptance attempt failed only because candidate staging omitted `config/`; no failed candidate was deployed.

## Deferred boundaries

Still not implemented:
- deterministic action-duration planning profiles;
- accumulated training stimulus/adaptation;
- attribute/skill/body-measurement progression;
- soreness/injury and detailed exercise programming;
- inventory/resource depletion;
- universal grading/tier evaluation;
- rich memory/relationship/environment engines;
- exterior/Tahoe traversal;
- schema v5.

## Exact resume point — DISCUSSION

Current-action ETA observability is deployed. The Creator explicitly requested that development now pause for a roadmap/current-architecture discussion before selecting the next slice.

Do **not** automatically implement another slice. Re-read current roadmap/architecture and discuss the highest-leverage options. Preserve schema v4, 1x wake-on-demand autonomy, globally scoped ids, actor-scoped runtime, first-class actions/events, Telegram presentation rules, profile/runtime separation, typed/audited Creator control, and minimum-runnable expansion.
