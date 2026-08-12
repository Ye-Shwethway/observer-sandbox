# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Purpose: deterministic project recovery across ChatGPT sessions and protection against memory drift.
Last synchronized: 2026-08-13 — P0 remote deployment/control is COMPLETE / LIVE VERIFIED. P1 Living Darian Minimum is IN PROGRESS but its autonomy-runtime hardening slice is now IMPLEMENTED / CI-VALIDATED / DEPLOYED, with real-Gemini bounded acceptance passing on a disposable VPS DB copy. Production character autonomy remains explicitly DISABLED by Creator instruction.

## HARD RECOVERY RULES

Read `AGENTS.md` first, then this file, then task-relevant repo files before changing the project.

After every material repository or verified runtime change, update this file in the same work session/change set. Never conflate committed, CI-validated, deployed, DB-applied, and live-verified state. State only the strongest level actually proven.

Authority order:
1. Explicit current Creator instruction.
2. Current canonical repo config/schema/architecture.
3. Verified live VPS/runtime/DB evidence.
4. Deployed repo/workflow evidence.
5. Current CI/test evidence.
6. This bootstrap.
7. Older chat/model memory.

GitHub config/schema = authored definitions. VPS SQLite = mutable operational reality. Python runtime = state-transition authority. AI models only propose structured actions. GitHub Actions/SSH = deployment/control transport. Telegram will be observer/control UI, not core business logic. Chat/model memory is never authoritative over newer repo/live evidence.

## Project scope / architecture

Observer Sandbox is intentionally small and modular, not another EIDOLON/Simiverse-scale architecture. Initial product: one Home, one character (Darian), persistent autonomous structured actions, later Telegram observation/control, then progressively richer physiology/memory/relationships.

Core principle: **deep profile, partial simulation**.

Logical world model: graph. Physical persistence: SQLite relational tables. Core model: Entity + Relation + State + Capability. Definitions/templates live in Git/config; mutable instances/runtime state live in DB. Deploys must not overwrite mutable live state.

LLM flow:
1. runtime builds current state + character context + valid action options;
2. model proposes one structured action;
3. runtime validates target/topology/capability/duration;
4. scheduler persists it as pending;
5. when due, runtime applies exactly one state transition and advances sim time;
6. events are durable and duplicate completion is guarded by action id.

The LLM never gets arbitrary DB-write authority.

## Darian profile boundary

Canonical fixture: `config/characters/darian.canonical.json`.
Runtime defaults: `config/characters/darian.runtime-defaults.json`.
DB schema version: 3.

Locked profile highlights include 6'4", 215 lb, 9% body fat, IQ 140, approved RAPS values, rich measurements/genetic/visual/skill/preference data, and first-class intimate anatomy. Canonical penis measurement: 10 x 5 inches.

Sexual physiology semantics:
- `erectile_state`: flaccid | developing | erect | subsiding;
- `erection_firmness`: contextual simulated 0-100;
- flaccid baseline firmness 0 is normal, not dysfunction;
- Darian `erection_firmness_cap`: 100;
- `arousal_level`: separate dynamic field;
- runtime default: flaccid / firmness 0 / arousal 0.

## P1 world/state/action mechanics

World seed: `config/worlds/home.v1.json`.
Home v1: Bedroom, Kitchen, Bathroom, Living Room, Home Gym; 15 useful objects.
Live character: `char_darian`.

Current needs/state: location, current action, energy, hunger, thirst, sleepiness, cleanliness. Energy is high-good reserve; hunger/thirst/sleepiness are high-bad pressures; values clamp 0-100.

Action vocabulary: move, sleep, eat, drink, shower, rest, inspect, use, train, read, idle.

`src/observer_sandbox/simulation.py` now has explicit action contracts:
- action-specific duration bounds;
- move target must be an adjacent room;
- idle must have no target;
- all object actions require a local object target with the matching capability;
- valid context-specific options come from `action_options()`;
- completed actions may carry an `action_id` and are idempotent against duplicate completion records.

Deterministic one-day mechanics acceptance still exists through `BaselineLivingPolicy` on test DB only.

## AI provider/model architecture

Model IDs are never hard-coded into character or engine logic.
Registry: Gemini, NanoGPT, OpenAI, OpenRouter.
Resolution: Provider -> Catalog -> Model Binding -> Runtime Adapter.
Binding precedence: task/role -> character/role -> engine/role -> character default -> global role -> global default.

Current live cognition binding: `gemini / gemini-3.5-flash-lite` for `character:char_darian / cognition`, dynamically selected from a 52-model live Gemini catalog. NanoGPT remains implemented/subscription-first but temporarily secondary.

Gemini secret is provisioned privately to `/var/lib/observer-sandbox/secrets.env` mode 0600. Never log or expose values.

Gemini structured output uses `responseMimeType=application/json` + `responseJsonSchema`.

## Cognition context hardening

`src/observer_sandbox/model_decision.py` now enriches each model decision with:
- current live needs/state/time/location;
- authoritative context-filtered `action_options` including exact target ids and duration bounds;
- Darian canonical traits, primary motivation, complexity notes;
- preferences, hobbies, habits, skills;
- time-of-day routine guidance;
- recent event summaries.

Prompt contract explicitly tells the model to choose an action/target pair from `action_options`, obey per-action duration bounds, and let physiological needs/safety override routine preferences.

## Persistent autonomy runtime

`src/observer_sandbox/autonomy.py` implements the live scheduler. `src/observer_sandbox/service.py` calls one scheduler tick every ~2 seconds.

Important semantics:
- if `autonomy_enabled=false`, no model call is made;
- if `paused=true`, no planning/completion occurs;
- `speed` controls wall-time duration for newly planned actions;
- at most one scheduler transition occurs per tick;
- pending actions persist in `runtime_state`;
- `runtime.current_action` reflects an in-progress pending action;
- completion advances simulation time only when due;
- lease key prevents concurrent scheduler ownership;
- action ids make completion recovery idempotent after a crash between durable completion and pending cleanup;
- API/decision/completion failures are recorded as `autonomy_error` events and enter exponential backoff (capped at 300 seconds);
- failure policy is fail-closed/backoff rather than silently switching Darian to scripted behavior.

Operational readback: `sandboxctl autonomy-status` shows enabled/paused/speed/pending/retry/current character state.

Tests in `tests/test_autonomy_runtime.py` cover disabled/paused no-model-call behavior, target contract rejection, pending persistence, speed-derived due time, completion, and crash-resume duplicate prevention.

CI #86 / run `31633300247`: SUCCESS after serialization fix; all tests + init/status checks passed.

## Live model proofs

### Non-mutating dry-run
`Dry Run Darian Decision` #3 / run `31632548092`: SUCCESS. Real Gemini proposal was validated with state/event-count invariants unchanged.

### Bounded scheduler acceptance
Workflow: `.github/workflows/autonomy-acceptance.yml`.
Bounded Autonomy Acceptance #1 / run `31633358752`: SUCCESS.

Safety design: copy production SQLite DB to a disposable `/tmp` DB, enable autonomy only in that copy, use live Gemini, plan exactly one action, advance to its due wall time, complete exactly one action, assert pending cleanup and sim-time advancement, delete the copy, then read production state.

Real Gemini proposal on the disposable copy:
- action: `move`;
- target: `room_bathroom`;
- duration: 5 minutes;
- reason: `Starting the morning with disciplined physical maintenance.`

Disposable-copy result moved Bedroom -> Bathroom and sim time 07:00 -> 07:05. Production DB remained untouched.

## Current verified production boundary

Repository: `Ye-Shwethway/observer-sandbox` private.
VPS: `107.175.30.238`, Ubuntu 24.04.
App: `/opt/observer-sandbox`.
DB: `/var/lib/observer-sandbox/observer.sqlite3`.
Service: `observer-sandbox` systemd.
SSH/runtime user: `observer`.
DB is not publicly exposed.

Deploy #49 / run `31633422733`: SUCCESS for deployed scheduler-status CLI.
Runtime Read #4 / run `31633460236`: SUCCESS and verified:
- service active;
- schema v3 healthy;
- `autonomy_enabled=false`;
- `paused=false`;
- `speed=1.0`;
- `pending_action=null`;
- `retry=null`;
- Darian still Bedroom / idle / 2025-05-01 07:00 UTC / baseline needs unchanged;
- Gemini credential present;
- NanoGPT credential absent.

Normal VPS work goes through GitHub Actions. Do not ask the Creator for Termux/root commands unless an unavoidable host/bootstrap-level issue cannot be handled through the established lane.

## Roadmap

- P0 Foundation & Remote Control: COMPLETE / LIVE VERIFIED.
- P0.5 Provider Layer: FOUNDATION COMPLETE; Gemini live credential/catalog/binding verified.
- Deep Character Profile: IMPLEMENTED; Darian instantiated live.
- P1 Living Darian Minimum: IN PROGRESS. World/state/action/model/scheduler mechanics are now hardened and bounded-live accepted. Production autonomy is still intentionally disabled pending Creator review/approval and any final P1 policy refinements.
- P2 Telegram Observer: after P1; include status/watch/history/pause/resume/speed plus provider/model refresh/list/rebinding controls.
- P3 Rich State & Memory: later.
- P4 First simulation module: later.
- P5 Second character: later.

## RESUME HERE

1. Do not redo VPS bootstrap, Gemini secret/catalog binding, action hardening, scheduler, or bounded acceptance unless newer evidence shows a regression.
2. Keep production `autonomy_enabled=false` until Creator explicitly approves enabling it.
3. Current live cognition binding is `gemini / gemini-3.5-flash-lite` for Darian.
4. Review the current autonomy behavior/policy before enabling production. Core scheduler safety path is implemented and bounded-live accepted; likely remaining P1 work is policy quality, control commands, and deciding the exact activation/start semantics.
5. P2 Telegram later wraps the same runtime + provider/catalog/binding backend; do not duplicate business logic in the bot.
6. Synchronize this file after every material change/live proof.
