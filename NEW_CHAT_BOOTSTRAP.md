# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Last synchronized: 2026-08-13

## Startup / authority

Read `AGENTS.md`, then this file, then `ROADMAP.md`, then task-relevant contracts.

Key contracts:
- core/runtime/schema/action: `docs/ARCHITECTURE.md`, `docs/COMPOSABLE_RUNTIME_ARCHITECTURE_AUDIT.md`
- Telegram: `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`, `docs/TELEGRAM_NOTIFICATION_POLICY.md`
- Creator controls: `docs/CREATOR_CONTROL_POLICY.md`
- training/physiology: `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`, P3.3–P3.5 docs
- autonomy/time: `docs/AUTONOMY_BREADTH_TIME_OBSERVABILITY.md`, `docs/CURRENT_ACTION_ETA_OBSERVABILITY.md`, `docs/RUNTIME_SPEED_CONTROL.md`, `docs/DURATION_PLANNING_PROFILES.md`
- future grading: `docs/FUTURE_GRADING_SYSTEM.md`

Authority: current Creator instruction > canonical repo/contracts > verified live VPS/runtime/DB > deployed workflow evidence > CI/tests > this bootstrap > older chat/memory.

## Development policy

Use minimum runnable expansion:
`minimum required state -> minimum behavior/evidence -> minimum Creator-facing surface -> focused tests -> disposable acceptance -> deploy/readback -> Creator acceptance -> next slice`.

Do not pre-build broad inventory, grading, memory, relationships, environment, combat, training progression, or regional systems merely because extension sockets exist.

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
- Creator may change global speed live; most recent Creator-verified test used `30x`
- Gemini cognition binding preserved
- Telegram connected private Creator observer

Production continues autonomously. Re-read live state whenever exact current Darian action/stats/speed matter.

## Canonical runtime rule

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`

LLMs propose structured actions only. Deterministic runtime owns legality and mutation. First-class actions/events preserve target, modifiers, outcome, state changes, location, participants and timing evidence.

## Proven feature state

- P2.2 Browse the Sandbox — COMPLETE / LIVE UX VERIFIED.
- P2.3.1 Restore Basic Stats — COMPLETE / LIVE UX VERIFIED.
- P3.1 Systemic Training Fatigue / Recovery — COMPLETE / LIVE UX VERIFIED.
- P3.2 Targeted Training Session — COMPLETE / ACCEPTANCE VERIFIED.
- P3.3 Training Readiness Modifier — COMPLETE / DEPLOYED / LIVE UX VERIFIED.
- P3.4 Training Effectiveness Outcome — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- P3.5 Effective Training Load — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.
- Autonomy Breadth + Time Observability v1 — DEPLOYED / ACCEPTANCE VERIFIED; broader estate use observed live.
- Current Action ETA Observability v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Runtime Speed Control v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED / LIVE UX VERIFIED.
- Deterministic Action Duration Planning Profiles v1 — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.

P3.5 short-term training loop remains:
`target -> readiness -> fatigue inefficiency -> effectiveness -> effective workload -> immediate physiology`.
No accumulated stimulus, attribute/skill/body-measurement progression, grading, or tiers yet.

## Time and planning state

Global speed can change while actions are pending. Running actions keep identity/target/simulated end; only remaining wall-clock due time is rescheduled. Pause freezes countdown. Telegram status and Character Update surfaces show duration/ETA/remaining time.

New model-backed actions now use deterministic preferred planning profiles while broad persisted legality bounds remain unchanged. Representative v1 profiles: inspect 2–6m, use 2–10m, read 20–60m, Heavy Bag 20–45m, Free Weights 45–90m. Sleep remains unclamped until nap/night-sleep semantics are separated.

## Exact resume point

The approved next direction is **Selective Activity/Action Semantics expansion**. Current action vocabulary is still shallow (`move/sleep/eat/drink/shower/rest/inspect/use/train/read/idle`). Add only a very small number of meaningful verbs where generic `use`/`inspect` is clearly inadequate, reusing schema-v4 `action_definitions`, capabilities, validation, first-class actions/events and duration profiles.

Likely first semantic candidates from current estate affordances: `research`, `monitor`, `maintain/repair`, or `practice`. Do not implement all at once. Choose the smallest useful vertical slice and validate/deploy it before adding another.

After activity semantics, planned discussion sequence remains: first read-only grading proof -> minimum training stimulus -> later adaptation/progression, unless Creator redirects.
