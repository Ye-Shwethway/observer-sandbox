# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Purpose: deterministic project recovery across ChatGPT sessions and protection against memory drift.
Last synchronized: 2026-08-13 — P0 remote deployment/control is COMPLETE / LIVE VERIFIED. P0.5 AI-provider foundation and Darian deep-profile foundation are established. P1 Living Darian Minimum is IN PROGRESS: Home v1, Darian runtime instantiation, validated action engine, event-driven time, one-day autonomous acceptance, model-backed structured decision adapters, and private AI-secret provisioning are implemented. Continuous live autonomy remains intentionally disabled until a real cognition provider/model is configured and verified.

## HARD RECOVERY RULES

Read `AGENTS.md` first, then this file, then the directly relevant current repository files before modifying the project.

After every material repository or verified runtime change, synchronize this file in the same work session/change set. Never confuse committed, CI-validated, deployed, migration-applied, and live-runtime-verified state. State only the strongest level actually proven.

Authority order:
1. Explicit current Creator instruction.
2. Current canonical repository config/schema and architecture contracts.
3. Verified live VPS/runtime/database evidence.
4. Deployed repository/workflow evidence.
5. Current CI/test evidence.
6. This bootstrap.
7. Older handoffs or chat/model memory.

> GitHub config/schema = authored canonical definitions.  
> VPS SQLite = mutable operational reality.  
> Python runtime = validation/state-transition authority.  
> AI model = proposes structured intentions; it never directly mutates world state.  
> GitHub Actions/SSH = deployment/control transport, not world-state authority.  
> Telegram = observer/control UI, not business-logic authority.  
> Chat/model memory = never authoritative over newer repo/live evidence.

## Project intent and anti-sprawl rule

Observer Sandbox is a small persistent AI-life sandbox, not another EIDOLON/Simiverse-scale system. Start with one home and one character, keep the runtime modular, and add richer physiology/memory/relationships later without rewriting the core.

Do not introduce multi-agent orchestration, giant cognition stacks, vector databases, large UI systems, or broad subsystem frameworks unless the Creator explicitly requests them and the current milestone needs them.

Core principle: **deep profile, partial simulation**.

## Architecture contract

Logical world model: graph. Physical persistence: relational SQLite.

Core entity model: Entity + Relation + State + Capability.

Definitions/templates are authored in Git/config. Concrete instances and mutable runtime state live in the database. Deployments must not overwrite mutable live state.

LLM contract:
1. runtime prepares context and allowed actions;
2. model returns one structured intention/action;
3. runtime validates topology, capabilities, prerequisites and state;
4. runtime applies the transition;
5. runtime advances simulated time and records events;
6. observer surfaces derived human-readable state.

The LLM never receives arbitrary DB-write authority.

Primary architecture reference: `docs/ARCHITECTURE.md`.

## Persistence / profile boundary

Current database schema version: **3**.

Important tables include `entities`, `relations`, `fields`, `events`, `runtime_state`, deep profile tables, and AI provider/model/binding/catalog tables.

Field modes: `canonical`, `static`, `derived`, `simulated`. Every actively mutable field must have one clear update authority.

Darian canonical fixture:
- `config/characters/darian.canonical.json`

Runtime baseline fixture:
- `config/characters/darian.runtime-defaults.json`

Current locked profile decisions include age 22 in the May-2025 baseline, height 6'4", weight 215 lb, body fat 9%, IQ 140, approved RAPS values, rich body/genetic/visual/skill/preference/routine data, and first-class intimate anatomy.

Canonical penis measurement: **10 x 5 inches**.

Sexual physiology semantics:
- `erectile_state`: `flaccid | developing | erect | subsiding`;
- `erection_firmness`: contextual simulated 0-100 response;
- flaccid baseline firmness 0 does not mean dysfunction;
- `erection_firmness_cap`: Darian 100;
- `arousal_level`: separate dynamic state;
- runtime default: flaccid / firmness 0 / arousal 0.

## AI provider layer

Model IDs must never be hard-coded into character or engine logic.

Built-in provider registry:
- Gemini
- NanoGPT
- OpenAI
- OpenRouter

Resolution concept: `Provider -> Catalog -> Model Binding -> Runtime Adapter`.

Binding precedence:
1. task + role
2. character + role
3. engine + role
4. character default
5. global + role
6. global default

NanoGPT remains subscription-first:
- base `https://nano-gpt.com/api`;
- catalog `/subscription/v1/models?detailed=true`;
- usage `/subscription/v1/usage`;
- live subscription generation `/subscription/v1/chat/completions`;
- do not force upstream provider selection for normal subscription traffic.

Gemini and NanoGPT now have P1 structured-decision generation support in `src/observer_sandbox/ai_runtime.py`.

Structured decision schema:
- `action`
- `duration_minutes`
- `target`
- `reason`

`src/observer_sandbox/model_decision.py` implements `ModelDecisionProvider`, enriches the snapshot with reachable rooms/local objects, resolves the logical `cognition` binding, and asks the selected model for exactly one structured action. Model output is still subject to the normal runtime validator; invalid AI output must never mutate the DB.

Unit coverage in `tests/test_model_decision.py` proves that a NanoGPT-bound structured decision can resolve without direct world mutation.

Provider credentials remain secret references only. The deploy workflow now optionally provisions these GitHub Actions secrets to a private VPS file:
- `OBSERVER_GEMINI_API_KEY`
- `OBSERVER_NANOGPT_API_KEY`
- `OBSERVER_OPENAI_API_KEY`
- `OBSERVER_OPENROUTER_API_KEY`

VPS secret file:
- `/var/lib/observer-sandbox/secrets.env`
- owned/writable by the `observer` runtime user;
- mode 0600;
- never log or expose values.

`src/observer_sandbox/secrets.py` self-loads non-empty values into the runtime environment before model decisions, avoiding another root/systemd bootstrap change.

Runtime Read may report only boolean credential presence, never values.

## P1 Living Darian Minimum — implemented mechanics

World seed: `config/worlds/home.v1.json`.

Home v1 contains 5 rooms:
- Bedroom
- Kitchen
- Bathroom
- Living Room
- Home Gym

Home v1 contains 15 useful objects including bed, shower, sink, refrigerator, pantry, stove, dining table, sofa, bookshelf, drinking water, meal ingredients, free weights and heavy bag.

Runtime/world modules:
- `src/observer_sandbox/world.py`
- `src/observer_sandbox/simulation.py`

Darian is instantiated as `char_darian` from the canonical fixture.

Current P1 live/runtime fields:
- `runtime.location`
- `runtime.current_action`
- `needs.energy`
- `needs.hunger`
- `needs.thirst`
- `needs.sleepiness`
- `physiology.cleanliness`

Semantics:
- energy = reserve; high is good;
- hunger/thirst/sleepiness = pressure; high is bad;
- values are clamped 0-100.

Validated P1 action vocabulary:
- move
- sleep
- eat
- drink
- shower
- rest
- inspect
- use
- train
- read
- idle

Movement is graph-constrained. Non-adjacent teleporting is rejected. Actions have durations and advance simulated time at event boundaries. Every completed action writes an `action_completed` event with before/after snapshots.

`DecisionProvider` is the stable selection interface. `BaselineLivingPolicy` is deterministic and exists only for mechanics/acceptance testing. `ModelDecisionProvider` is the live AI-compatible implementation.

CLI:
- `sandboxctl living-status`
- `sandboxctl simulate-day`

P1 acceptance test `tests/test_p1_living.py` proves Home/Darian seeding, invalid movement rejection, exactly 24 simulated hours of bounded autonomous activity, durable events and bounded final needs.

## Current verified production boundary

Repository: `Ye-Shwethway/observer-sandbox` (private).

VPS:
- host `107.175.30.238`;
- Ubuntu 24.04;
- app `/opt/observer-sandbox`;
- DB `/var/lib/observer-sandbox/observer.sqlite3`;
- service `observer-sandbox`;
- SSH/runtime user `observer`;
- DB not publicly exposed.

Deployment transport:
`GitHub main -> Actions -> SSH/rsync -> app install -> DB init/migration -> systemd restart -> status/living-state verification`.

P1 mechanics live proof:
- CI run #52 / id `31630284060` passed the first living acceptance slice.
- Deploy run #28 / id `31630283999` deployed the living mechanics.
- Runtime Read #2 / id `31630356571` verified service active, schema v3 healthy, and live Darian state.

Observed live Darian baseline:
- location Bedroom;
- current action idle;
- energy 75;
- hunger 20;
- thirst 15;
- sleepiness 15;
- cleanliness 80;
- sim time `2025-05-01T07:00:00+00:00`.

Latest model/secret-path validation:
- CI run #60 / id `31630745170`: **SUCCESS**.
- Deploy run #33 / id `31630745178`: **SUCCESS**.
- deploy steps included optional AI secret provisioning plus install/init/restart/living-status verification.
- deployed commit: `6c8edef3cf65bab3434836172b28cb1dc62ace17`.

`autonomy_enabled=false` remains intentional. Do not turn on unattended continuous production progression merely because the deterministic acceptance loop or model adapter exists. First verify a real provider credential, refresh its catalog, bind one concrete model to `character:char_darian / cognition`, obtain a valid structured decision, and confirm runtime validation behavior.

## Remote-operation policy

Normal VPS work goes through GitHub Actions. Do not ask the Creator for Termux/root commands unless an unavoidable host-level bootstrap issue cannot be handled through the established lane.

Exact sudo service verification command remains `systemctl is-active observer-sandbox`; do not add `--quiet` unless sudoers changes too.

## Roadmap state

- **P0 — Foundation & Remote Control:** COMPLETE / LIVE VERIFIED.
- **P0.5 — AI Provider Layer:** FOUNDATION COMPLETE / CI-VALIDATED / model decision adapters implemented for Gemini + NanoGPT.
- **Deep Character Profile Foundation:** IMPLEMENTED / CI-VALIDATED / Darian instantiated live.
- **P1 — Living Darian Minimum:** IN PROGRESS. World/state/action/time/event mechanics are live; structured model-decision path is implemented and deployed; live provider credential/catalog/binding/decision verification and controlled continuous autonomy remain.
- **P2 — Telegram Observer:** later.
- **P3 — Rich State & Memory:** later.
- **P4 — First plug-in simulation module:** later.
- **P5 — Second character:** later.

## RESUME HERE

1. Do not redo P0 or VPS bootstrap.
2. Keep `autonomy_enabled=false` until live AI selection is proven.
3. Read `src/observer_sandbox/ai.py`, `ai_runtime.py`, `model_decision.py`, and `simulation.py` before continuing P1.
4. Use Runtime Read credential-presence booleans to see whether NanoGPT or Gemini is provisioned.
5. If NanoGPT is available, prefer it first because the Creator already uses a subscription and wants subscription quota efficiency. Keep the subscription-only catalog/generation path.
6. Refresh the selected provider catalog, choose a real returned model ID, and create the logical character cognition binding. Never invent or hard-code a model ID.
7. Add a controlled one-decision live verification before continuous autonomy. The model proposes; runtime validation decides; failed/invalid model output must leave world state unchanged.
8. After every material change or live proof, synchronize this file again.
