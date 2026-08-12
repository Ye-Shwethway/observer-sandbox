# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Purpose: deterministic project recovery across ChatGPT sessions and protection against memory drift.
Last synchronized: 2026-08-13 — P0 remote deployment/control is COMPLETE / LIVE VERIFIED. P0.5 AI-provider foundation and Darian deep-profile foundation are established. P1 Living Darian Minimum has started: Home v1 + Darian runtime instantiation + validated action engine + one-day autonomous acceptance are implemented; the P1 foundation is CI-validated, deployed, and live-read verified. Live continuous autonomy remains intentionally disabled until the model decision adapter is wired.

## HARD RECOVERY RULES

Read `AGENTS.md` first, then this file, then the directly relevant current repository files before modifying the project.

After every material repository or verified runtime change, synchronize this file in the same work session/change set. Material changes include architecture decisions, schemas/migrations, canonical profile decisions, provider/model behavior, roadmap status, deployment/runtime topology, workflow behavior, live verification state, and the next resume point.

Never confuse:
- committed in GitHub;
- CI validated;
- deployed to VPS;
- schema/migration applied to the live database;
- live-runtime verified.

State only the strongest level actually proven.

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

Observer Sandbox is a small persistent AI-life sandbox, not another EIDOLON/Simiverse-scale system.

Initial product:
- one home environment;
- one character: Darian;
- AI chooses structured actions;
- runtime validates and applies them;
- user observes/controls through Telegram later;
- modules can expand physiology, memory, relationships and additional characters without rewriting the core.

Do not introduce multi-agent orchestration, giant cognition stacks, vector databases, large UI systems, or broad subsystem frameworks unless the Creator explicitly requests them and the current milestone needs them.

Core principle: **deep profile, partial simulation**.

## Current architecture contract

Logical world model: graph. Physical persistence: relational SQLite.

Core entity model:
- Entity
- Relation
- State
- Capability

Definitions/templates are authored in Git/config. Concrete instances and mutable runtime state live in the database. Deployments must not overwrite mutable live state.

LLM contract:
1. runtime prepares context and available actions;
2. model returns structured intention/action;
3. runtime validates capability, prerequisites and state;
4. runtime applies the transition;
5. runtime advances simulated time and records events;
6. observer surfaces derived human-readable state.

The LLM never receives arbitrary DB-write authority.

Primary architecture reference: `docs/ARCHITECTURE.md`.

## Persistence / schema boundary

Current database schema version: **3** (`src/observer_sandbox/db.py`).

Important tables include:
- `entities`
- `relations`
- `fields`
- `events`
- `runtime_state`
- `profile_field_definitions`
- `character_profiles`
- deep character-profile value/history/collection tables
- AI provider/model/binding/catalog-sync tables

Field modes: `canonical`, `static`, `derived`, `simulated`.

Every actively mutable profile field must have one clear update authority. A static field is not stale merely because no simulation engine owns it yet. When a future module activates a previously static field, initialize from the existing canonical baseline, transfer authority explicitly, and log the transition.

## Darian canonical profile boundary

Canonical authored fixture:
- `config/characters/darian.canonical.json`

Runtime baseline fixture:
- `config/characters/darian.runtime-defaults.json`

Importer/validation:
- `src/observer_sandbox/profile_seed.py`
- `src/observer_sandbox/profile_schema.py`
- `src/observer_sandbox/profile_schema_source_union.py`
- `src/observer_sandbox/sexual_state_schema.py`

Locked current Darian facts include:
- age 22 in the May-2025 baseline;
- height 6'4";
- weight 215 lb;
- body fat 9%;
- IQ 140;
- later approved RAPS values;
- rich body measurements, genetic maxima, visual profile, skills, preferences, habits and routines retained;
- intimate anatomy remains first-class profile data;
- canonical penis measurement: 10 x 5 inches.

Sexual-physiology semantics:
- `erectile_state`: `flaccid | developing | erect | subsiding`;
- `erection_firmness`: dynamic 0-100 physiological response;
- normal flaccid baseline means firmness `0`, not dysfunction;
- `erection_firmness_cap`: Darian ceiling `100`;
- `arousal_level`: separate dynamic state;
- runtime default is flaccid / firmness 0 / arousal 0.

Older conflicting values are historical/superseded evidence and must not silently replace the canonical seed.

## AI provider layer — current foundation

AI model IDs must never be hard-coded into character or engine logic.

Built-in providers:
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

For P1 keep cognition simple: one primary cognition binding is enough before expanding per-role bindings.

NanoGPT is first-class and subscription-first:
- default base URL `https://nano-gpt.com/api`;
- default model refresh uses `/subscription/v1/models?detailed=true`;
- subscription usage uses `/subscription/v1/usage`;
- do not force upstream provider selection for ordinary subscription traffic;
- broader catalogs remain explicit opt-in later.

Provider credentials are environment-secret references, never plaintext DB values or Telegram-visible secret text.

Expected credential names:
- `OBSERVER_GEMINI_API_KEY`
- `OBSERVER_NANOGPT_API_KEY`
- `OBSERVER_OPENAI_API_KEY`
- `OBSERVER_OPENROUTER_API_KEY`

## P1 Living Darian Minimum — current implemented slice

World seed:
- `config/worlds/home.v1.json`

Home v1 contains 5 rooms:
- Bedroom
- Kitchen
- Bathroom
- Living Room
- Home Gym

It contains 15 useful objects including bed, shower, sink, refrigerator, pantry, stove, dining table, sofa, bookshelf, drinking water, meal ingredients, free weights and heavy bag.

Runtime/world implementation:
- `src/observer_sandbox/world.py`
- `src/observer_sandbox/simulation.py`

Darian is instantiated as `char_darian` from the canonical seed. P1 runtime fields currently include:
- `runtime.location`
- `runtime.current_action`
- `needs.energy`
- `needs.hunger`
- `needs.thirst`
- `needs.sleepiness`
- `physiology.cleanliness`

Needs semantics:
- energy = reserve; higher is better;
- hunger/thirst/sleepiness = pressure; higher is worse;
- values are clamped to 0-100.

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

Movement is graph-constrained. Non-adjacent teleporting is rejected. Actions have durations and advance simulated time at event boundaries rather than per-minute model calls. Every completed action writes an `action_completed` event containing before/after snapshots.

`DecisionProvider` is the stable action-selection boundary. `BaselineLivingPolicy` is a deterministic acceptance policy behind that same interface; it exists so P1 mechanics can be validated without hard-coding an AI model. The next step is to wire an actual selected provider/model into this interface without changing runtime validation/state-transition logic.

CLI P1 inspection/acceptance commands:
- `sandboxctl living-status`
- `sandboxctl simulate-day`

P1 CI acceptance test:
- `tests/test_p1_living.py`
- Home has exactly 5 seeded rooms and 15 seeded objects;
- Darian instantiates from canonical profile;
- invalid non-adjacent movement is rejected;
- Darian completes exactly 24 simulated hours autonomously within bounded actions;
- final needs remain in bounds and event history is durable.

Latest P1 CI proof:
- CI run **#52**, run id `31630284060`;
- commit `05b22640d942eda20eb150842abd1a16cac2ceaa`;
- pytest, DB init and status smoke all passed.

## Current verified production boundary

Repository: `Ye-Shwethway/observer-sandbox` (private).

VPS:
- host: `107.175.30.238`;
- OS: Ubuntu 24.04;
- application: `/opt/observer-sandbox`;
- persistent DB: `/var/lib/observer-sandbox/observer.sqlite3`;
- service: `observer-sandbox` under systemd;
- deployment/runtime SSH user: `observer`;
- database is not exposed publicly.

Deployment transport:
`GitHub main -> GitHub Actions -> SSH/rsync -> /opt/observer-sandbox -> venv/install -> DB init/migration -> systemd restart -> status verification`

P1 application deployment proof:
- Deploy Observer Sandbox run **#28**, run id `31630283999`;
- commit `05b22640d942eda20eb150842abd1a16cac2ceaa`;
- checkout, SSH, rsync, install, DB initialization, restart and service verification passed.

Latest P1 live read proof:
- Runtime Read run **#2**, run id `31630356571`;
- workflow commit `1de9a7490cc3c86c4f2b715c068b58ddb566a3ac`;
- service active;
- schema version 3 healthy;
- live Darian state read succeeded.

Live Darian baseline observed at that read:
- actor `char_darian`;
- location `room_bedroom` / Bedroom;
- current action `idle`;
- energy 75;
- hunger 20;
- thirst 15;
- sleepiness 15;
- cleanliness 80;
- simulation time `2025-05-01T07:00:00+00:00`.

`autonomy_enabled=false` is intentional at this boundary. Do not enable unattended continuous live progression until the actual AI decision adapter/model binding is wired and verified. CI one-day autonomous acceptance uses the deterministic decision-provider implementation and does not mutate production time.

## Remote-operation policy

Normal VPS work must be performed through GitHub Actions.

Use Actions for deploy/update, dependency install, DB init/migration, service restart and runtime readback. Do not ask the Creator to use phone/Termux for ordinary work. Only request a one-shot root command for an unavoidable host/bootstrap-level issue.

The exact allowed service verification command is `systemctl is-active observer-sandbox`; do not add an unapproved argument such as `--quiet` unless sudoers is updated accordingly.

## Roadmap state

- **P0 — Foundation & Remote Control:** COMPLETE / LIVE VERIFIED.
- **P0.5 — AI Provider Layer:** FOUNDATION COMPLETE / CI-VALIDATED.
- **Deep Character Profile Foundation:** IMPLEMENTED / CI-VALIDATED / Darian instantiated live.
- **P1 — Living Darian Minimum:** IN PROGRESS; world/state/action/event mechanics are CI-validated, deployed and live-read verified. Actual model-driven continuous autonomy is the remaining core P1 step.
- **P2 — Telegram Observer:** later.
- **P3 — Rich State & Memory:** later.
- **P4 — First plug-in simulation module:** later.
- **P5 — Second character:** later.

## RESUME HERE

1. Treat P0 remote deployment/readback as COMPLETE / LIVE VERIFIED.
2. Treat Home v1, Darian instantiation, P1 need fields, validated action engine, event-driven time and one-day deterministic autonomy acceptance as established; extend them rather than rewriting them.
3. Read `src/observer_sandbox/ai.py` and `src/observer_sandbox/simulation.py` next.
4. Implement the actual **model-backed `DecisionProvider`** using one selected cognition binding. Do not hard-code provider/model IDs.
5. Prefer Gemini or NanoGPT as the first live provider according to available secret/configuration; NanoGPT remains subscription-first.
6. Validate structured action output strictly before applying anything to the DB. Invalid model output must not mutate state.
7. Keep `autonomy_enabled=false` until model-backed decision selection and controlled live-loop behavior are verified.
8. After the next material change, synchronize this file again with the strongest proven repo/CI/deploy/live state.
