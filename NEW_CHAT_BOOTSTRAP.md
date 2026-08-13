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
- activity semantics: `docs/RESEARCH_ACTION_SEMANTICS.md`
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
- global speed is Creator-controlled and must be re-read live; Deploy #136 observed `5x`
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
- Minimum Research Action Semantics — COMPLETE / ACCEPTANCE VERIFIED / DEPLOYED.

P3.5 short-term training loop remains:
`target -> readiness -> fatigue inefficiency -> effectiveness -> effective workload -> immediate physiology`.
No accumulated stimulus, attribute/skill/body-measurement progression, grading, or tiers yet.

## Time and planning state

Global speed can change while actions are pending. Running actions keep identity/target/simulated end; only remaining wall-clock due time is rescheduled. Pause freezes countdown. Telegram status and Character Update surfaces show duration/ETA/remaining time.

Action durations remain integer simulated minutes with a minimum of 1 minute. Regression coverage proves `1 sim min @ 3600x` still schedules a positive `1/60` real-second delay and completes safely at the due boundary. Sub-minute simulation actions are not implemented.

New model-backed actions use deterministic preferred planning profiles while broad persisted legality bounds remain unchanged. Sleep remains unclamped until nap/night-sleep semantics are separated.

## Activity semantics state

`research` is the first selective semantic verb. It is legal only on the Library Research Desk, broad legal duration 10–180m, preferred planning 30–90m, and persists through ordinary first-class action/event flow. It currently produces only ordinary passive physiology/time effects; there is no knowledge inventory, skill XP, research-project state, memory consolidation, grading or progression.

The model-backed decision provider now unions legacy vocabulary with action names currently exposed by authoritative `action_options`, so later semantic verbs become choosable through world affordances without a second hard-coded model vocabulary edit.

Evidence: PR #10 merge `c50f4cf9a87b15589be3b3ea4878990da7e69d02`; main CI #366 / `31681716298` SUCCESS; Research Action Semantics Acceptance #1 / `31681716339` SUCCESS; release `8f3487feccc84ef10b045dff960097bc0c44ceb6`; Deploy #136 / `31681760620` SUCCESS.

## Exact resume point

Continue **Selective Activity/Action Semantics** one bounded verb at a time. The next high-value candidate is `monitor` on the existing Surveillance Console. Keep it first-class and observable but do not build a rich intelligence/environment subsystem merely to support the verb.

After the bounded semantics work, planned sequence remains: first read-only grading proof -> minimum training stimulus -> later adaptation/progression, unless Creator redirects.
