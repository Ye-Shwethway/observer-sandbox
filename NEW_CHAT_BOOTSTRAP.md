# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Purpose: deterministic project recovery across ChatGPT sessions and protection against memory drift.
Last synchronized: 2026-08-13 — P0 remote deployment/control is COMPLETE / LIVE VERIFIED. P1 Living Darian Minimum core runtime, Gemini cognition, authored autonomy policy, persistent scheduler, behavior-quality matrix, first production canary, and bounded canary/control gate are IMPLEMENTED / CI-VALIDATED / DEPLOYED / LIVE VERIFIED. Production continuous character autonomy remains explicitly DISABLED.

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

`src/observer_sandbox/simulation.py` has explicit action contracts:
- action-specific duration bounds;
- move target must be an adjacent room;
- idle must have no target;
- all object actions require a local object target with the matching capability;
- valid context-specific options come from `action_options()`;
- completed actions may carry an `action_id` and are idempotent against duplicate completion records.

Deterministic one-day mechanics acceptance remains available through `BaselineLivingPolicy` on test DB only.

## AI provider/model architecture

Model IDs are never hard-coded into character or engine logic.
Registry: Gemini, NanoGPT, OpenAI, OpenRouter.
Resolution: Provider -> Catalog -> Model Binding -> Runtime Adapter.
Binding precedence: task/role -> character/role -> engine/role -> character default -> global role -> global default.

Current live cognition binding: `gemini / gemini-3.5-flash-lite` for `character:char_darian / cognition`, dynamically selected from a 52-model live Gemini catalog. NanoGPT remains implemented/subscription-first but temporarily secondary.

Gemini secret is provisioned privately to `/var/lib/observer-sandbox/secrets.env` mode 0600. Never log or expose values.
Gemini structured output uses `responseMimeType=application/json` + `responseJsonSchema`.

## Authored Darian autonomy policy

Character-specific policy lives in `config/characters/darian.autonomy-policy.json`.
Current policy revision: `darian-autonomy-p1-v1.2`.

The policy is character behavior guidance, not runtime safety authority. Universal action legality remains in the runtime validator.

Policy content includes:
- immediate physiology/safety outranks discretionary routines;
- critical thresholds: sleepiness >=80, energy <=20, thirst >=75, hunger >=80;
- strong thresholds: sleepiness >=65, energy <=30, thirst >=55, hunger >=60, cleanliness <=40;
- routine windows: morning training 07-11, midday productive 11-17, evening wind-down 17-22, night sleep 22-07;
- recent-event repetition guidance over the latest 8 events;
- reasons should be short and naturally grounded in the active need/routine/purpose;
- critical night sleep at a usable bed gets recommended overnight duration 360-540 minutes rather than a short nap.

`src/observer_sandbox/model_decision.py` enriches each decision with current needs/state/time/location, authoritative `action_options`, canonical traits/motivation/preferences/habits/skills, recent events, the authored policy, and computed decision signals.

## Cognition behavior-quality proof

Evaluator: `src/observer_sandbox/behavior_eval.py`.
Workflow: `.github/workflows/cognition-behavior-eval.yml`.
Safety: scenarios run against a disposable production-DB copy on the VPS using the live Gemini credential; production DB is read back afterward.

Cognition Behavior Eval #4 / run `31634364165`: **SUCCESS, 5/5** with real Gemini:
1. morning-ready -> move toward morning training path;
2. strong thirst -> hydration path with thirst-grounded reason;
3. strong hunger -> food path with hunger-grounded reason;
4. critical night sleepiness -> bed sleep for **480m**;
5. poor cleanliness -> Bathroom/hygiene path.

CI #107 / run `31634364163`: SUCCESS for the same behavior-quality head.

## Persistent autonomy runtime

`src/observer_sandbox/autonomy.py` implements the live scheduler. `src/observer_sandbox/service.py` calls one scheduler tick every ~2 seconds.

Semantics:
- `autonomy_enabled=false` => no model call;
- `paused=true` => no planning/completion;
- `speed` controls wall-time duration for normal newly planned actions;
- at most one scheduler transition per tick;
- pending actions persist in `runtime_state`;
- `runtime.current_action` reflects pending activity;
- completion advances sim time only when due;
- lease prevents concurrent scheduler ownership;
- action ids make crash recovery idempotent;
- API/decision/completion failures create `autonomy_error` events and exponential backoff capped at 300s;
- failure policy is fail-closed/backoff, never silent scripted substitution.

Operational readback: `sandboxctl autonomy-status` or `sandboxctl autonomy status`.

## Live model proofs

### Non-mutating dry-run
`Dry Run Darian Decision` #3 / run `31632548092`: SUCCESS. Real Gemini proposal passed runtime validation while state/event counts remained unchanged.

### Bounded scheduler acceptance on disposable DB
`.github/workflows/autonomy-acceptance.yml`.
Bounded Autonomy Acceptance #1 / run `31633358752`: SUCCESS. Real Gemini planned and completed one action on a production-DB copy; production DB remained untouched.

### Production cognition behavior matrix
Cognition Behavior Eval #4 / run `31634364165`: SUCCESS, 5/5.

### First real production canary — LIVE VERIFIED
Autonomy Control #1 / run `31635032005` armed the first production canary. This exposed an activation-semantics flaw: the original `canary-once` command bounded **action count** but not **wall time**; at speed 1.0 it armed the normal scheduler and could remain enabled until the action's real due wall time.

The live model nevertheless planned exactly one valid production action:
- action: `move`;
- target: `room_living`;
- duration: 5 minutes;
- reason: `Moving out of the bedroom to begin the morning training routine.`;
- action id: `2d856b9e-6feb-4420-a716-03987c1719b6`.

A temporary recovery workflow was used only to complete that already-planned action through the authoritative `autonomy_tick()` scheduler at its due point; it did not bypass validation/state-transition/idempotency logic.

Production Canary Completion #2 / run `31635250326`: **SUCCESS**.
Live result:
- Bedroom -> Living Room;
- sim time `2025-05-01T07:00:00+00:00` -> `2025-05-01T07:05:00+00:00`;
- energy 75.0 -> 74.75;
- hunger 20.0 -> 20.333;
- thirst 15.0 -> 15.417;
- sleepiness 15.0 -> 15.292;
- cleanliness 80.0 -> 79.9;
- current action returned to idle;
- pending cleared;
- canary auto-disabled;
- mode returned to normal;
- retry remained null.

This is the first real production autonomous Darian action.

## Permanent bounded canary fix

The wall-time flaw found by the first live canary is now fixed in code.

`run_canary_once()` in `src/observer_sandbox/autonomy.py` now makes the user-facing canary synchronous and bounded:
1. arm canary mode;
2. plan exactly one model action through the normal scheduler;
3. preserve the authored simulated duration;
4. advance the scheduler directly to that action's due point for canary verification instead of waiting minutes/hours of wall time;
5. complete through normal `autonomy_tick()` / validator / state-transition / lease / action-id path;
6. verify auto-disable, normal mode, and no pending action before returning.

The low-level `arm_canary_once()` remains only as a primitive for tests/service coordination.
`sandboxctl autonomy canary-once` now calls `run_canary_once()` and exits nonzero if the canary does not finish safely.

CI #120 / run `31635452458`: SUCCESS for synchronous bounded canary tests.
Deploy #62 / run `31635371198`: SUCCESS for bounded canary runtime.
Deploy #63 / run `31635404645`: SUCCESS for CLI integration.

Temporary one-time trigger and recovery workflow used for the first live canary were removed after the permanent fix. `.github/workflows/autonomy-control.yml` is restored to manual `workflow_dispatch` only.

## Production activation/control gate

CLI commands:
- `sandboxctl autonomy status`
- `sandboxctl autonomy enable`
- `sandboxctl autonomy disable`
- `sandboxctl autonomy pause`
- `sandboxctl autonomy resume`
- `sandboxctl autonomy speed <value>` where 0 < value <= 3600
- `sandboxctl autonomy canary-once` (synchronous bounded canary)

Remote manual workflow: `.github/workflows/autonomy-control.yml`.
It exposes safe commands: status, canary-once, disable, pause, resume, speed.
It deliberately does **not** expose continuous `enable` yet. Continuous production enable remains gated on explicit Creator approval and a later intentional control change.

## Current verified production boundary

Repository: `Ye-Shwethway/observer-sandbox` private.
VPS: `107.175.30.238`, Ubuntu 24.04.
App: `/opt/observer-sandbox`.
DB: `/var/lib/observer-sandbox/observer.sqlite3`.
Service: `observer-sandbox` systemd.
SSH/runtime user: `observer`.
DB is not publicly exposed.

Latest verified live state after first production canary:
- service healthy/active;
- schema v3;
- `autonomy_enabled=false`;
- `mode=normal`;
- `paused=false`;
- `speed=1.0`;
- `pending_action=null`;
- `retry=null`;
- Darian is now in **Living Room**, idle, at `2025-05-01T07:05:00+00:00`;
- Gemini credential present;
- NanoGPT credential absent.

Normal VPS work goes through GitHub Actions. Do not ask the Creator for Termux/root commands unless an unavoidable host/bootstrap-level issue cannot be handled through the established lane.

## Roadmap

- P0 Foundation & Remote Control: COMPLETE / LIVE VERIFIED.
- P0.5 Provider Layer: FOUNDATION COMPLETE; Gemini live credential/catalog/binding verified.
- Deep Character Profile: IMPLEMENTED; Darian instantiated live.
- P1 Living Darian Minimum: **CORE IMPLEMENTATION + HARDENING + FIRST PRODUCTION CANARY COMPLETE / LIVE VERIFIED.** Continuous production autonomy remains OFF by deliberate gate. The remaining P1 decision is whether to permit continuous autonomy and under what initial speed/observation conditions.
- P2 Telegram Observer: after P1 activation decision; status/watch/history/pause/resume/speed plus provider/model refresh/list/rebinding controls should wrap the existing backend.
- P3 Rich State & Memory: later.
- P4 First simulation module: later.
- P5 Second character: later.

## RESUME HERE

1. Production continuous autonomy is currently OFF. Do not enable it without explicit Creator approval.
2. Do not redo VPS bootstrap, Gemini secret/catalog binding, action hardening, scheduler, cognition policy, behavior matrix, or first production canary unless newer evidence shows a regression.
3. Current live cognition binding is `gemini / gemini-3.5-flash-lite` for Darian.
4. First real production action already occurred successfully: Bedroom -> Living Room, 07:00 -> 07:05, then auto-disable.
5. `sandboxctl autonomy canary-once` is now synchronous and bounded; do not recreate the temporary trigger/recovery workflow.
6. Continuous `enable` remains intentionally absent from the remote Actions control workflow. Add/use it only after a separate explicit Creator decision.
7. P2 Telegram later wraps the same runtime/provider/catalog/control backend; do not duplicate business logic in the bot.
8. Synchronize this file after every material change/live proof.
