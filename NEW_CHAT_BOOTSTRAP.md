# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Purpose: deterministic project recovery across ChatGPT sessions and protection against memory drift.
Last synchronized: 2026-08-13 — P0 remote deployment/control is COMPLETE / LIVE VERIFIED; P0.5 AI-provider foundation and Darian deep-profile foundation are implemented; P1 Living Darian Minimum is next.

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

Logical world model: graph.
Physical persistence: relational SQLite.

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

Field modes:
- `canonical`
- `static`
- `derived`
- `simulated`

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

Darian canonical reconciliation is complete for the current seed revision. Important locked decisions include:
- age 22 in the May-2025 character baseline;
- height 6'4";
- weight 215 lb;
- body fat 9%;
- IQ 140;
- later approved RAPS values rather than conflicting older variants;
- rich body measurements, genetic maxima, visual profile, skills, preferences, habits, routines and other detailed fields are preserved rather than collapsed;
- intimate anatomy remains a first-class profile domain rather than notes-only data;
- canonical penis measurement: 10 x 5 inches;
- erection firmness is not a permanent static score.

Sexual-physiology semantics:
- `erectile_state`: `flaccid | developing | erect | subsiding`;
- `erection_firmness`: dynamic 0-100 physiological response;
- normal flaccid baseline means firmness `0`, not dysfunction;
- `erection_firmness_cap`: Darian canonical ceiling `100`;
- `arousal_level`: separate dynamic state from erection firmness;
- runtime default is flaccid / firmness 0 / arousal 0.

Older conflicting values are historical/superseded evidence and must not silently replace the canonical seed.

## AI provider layer — current foundation

AI model IDs must never be hard-coded into character or engine logic.

Built-in provider slots/adapters:
- Gemini
- NanoGPT
- OpenAI
- OpenRouter

Resolution concept:
`Provider -> Catalog -> Model Binding -> Runtime Adapter`

Binding precedence:
1. task + role
2. character + role
3. engine + role
4. character default
5. global + role
6. global default

For P1, keep actual cognition simple: activate one primary cognition binding before expanding per-role bindings.

NanoGPT is first-class and subscription-first:
- default base URL: `https://nano-gpt.com/api`;
- normal model refresh uses subscription-only catalog `/subscription/v1/models?detailed=true`;
- subscription usage endpoint supported via `/subscription/v1/usage`;
- do not force an upstream provider for ordinary subscription traffic because that may route to pay-as-you-go billing;
- broader canonical/paid/personalized catalogs may be exposed later as explicit opt-in filters.

Provider credentials are environment-secret references, never plaintext DB values or Telegram-visible secret text.

Expected credential names include:
- `OBSERVER_GEMINI_API_KEY`
- `OBSERVER_NANOGPT_API_KEY`
- `OBSERVER_OPENAI_API_KEY`
- `OBSERVER_OPENROUTER_API_KEY`

Telegram later configures provider enablement, catalog refresh and logical model bindings; Telegram must not own the underlying settings logic.

## Current verified production boundary

Repository: `Ye-Shwethway/observer-sandbox` (private).

VPS:
- host: `107.175.30.238`;
- OS baseline: Ubuntu 24.04;
- application path: `/opt/observer-sandbox`;
- persistent DB: `/var/lib/observer-sandbox/observer.sqlite3`;
- service: `observer-sandbox` under systemd;
- deployment/runtime SSH user: `observer`;
- database is not exposed publicly.

Deployment transport:
`GitHub main -> GitHub Actions -> SSH/rsync -> /opt/observer-sandbox -> venv/install -> DB init/migration -> systemd restart -> status verification`

The VPS does **not** require a GitHub deploy key/PAT for repository pulls; Actions checks out the private repo and rsyncs the files to the VPS.

Required repository Actions configuration is already provisioned:
- secrets: `VPS_HOST`, `VPS_PORT`, `VPS_USER`, `VPS_SSH_KEY`;
- variable: `VPS_DEPLOY_ENABLED=true`.

Do not expose secret values in logs, docs, chat, DB, or Telegram.

Latest live deployment proof:
- successful Deploy Observer Sandbox run: **#22**, run id `31629295673`;
- deployed code/workflow boundary proven by commit `2e4e19637a755bff55765848cf83dbfced56927a`;
- checkout, required-secret checks, SSH, rsync, package install, DB initialization, systemd restart, active check and `sandboxctl status` all passed.

Latest independent runtime-read proof:
- Runtime Read run **#1**, run id `31629365726`;
- workflow commit `52878569f2a7bc13c7ffc964f449a8e932e397fe`;
- SSH connection, systemd active read and live `sandboxctl status` passed.

Important distinction: documentation/runtime-read commits after the deployed application boundary are **not** proof that application code changed on the VPS. Use deployment workflow evidence for deployment claims.

The bootstrap/README/AGENTS commits that establish continuity are documentation/control-plane changes and do not themselves change the live simulation runtime.

## Remote-operation policy

Normal VPS work must be performed through GitHub Actions after the one-time bootstrap.

Use GitHub Actions for:
- deploy/update;
- dependency install;
- DB init/migration;
- service restart;
- health/status/runtime readback.

Do not ask the Creator to run phone/Termux commands for ordinary work. Only request a one-shot root command when an unavoidable OS/bootstrap-level permission or host configuration issue cannot be corrected through the established Actions lane.

The prior sudo issue is resolved. The exact allowed service verification command is `systemctl is-active observer-sandbox`; do not reintroduce an unapproved argument variant such as `--quiet` unless the sudoers rule is updated accordingly.

## Roadmap state

- **P0 — Foundation & Remote Control:** COMPLETE / LIVE VERIFIED.
- **P0.5 — AI Provider Layer:** FOUNDATION COMPLETE / CI-VALIDATED; live provider credentials/catalog calls are not yet the P1 acceptance criterion.
- **Deep Character Profile Foundation:** IMPLEMENTED / CI-VALIDATED; Darian canonical and runtime-default fixtures exist.
- **P1 — Living Darian Minimum:** NEXT.
- **P2 — Telegram Observer:** later.
- **P3 — Rich State & Memory:** later.
- **P4 — First plug-in simulation module (physiology/training):** later.
- **P5 — Second character:** later, only after stable single-character runtime.

P1 target:
- Home with roughly 3-5 rooms;
- 10-20 useful objects;
- instantiate Darian from canonical seed;
- initial simulated fields such as location, energy, hunger, sleepiness/current action;
- roughly 10-15 validated actions such as move, sleep, eat, drink, shower, rest, inspect, use, train and idle;
- event-driven simulated time;
- autonomous action loop;
- acceptance: Darian completes one simulated day without manual prompting.

## RESUME HERE

1. Treat P0 remote deploy/readback as **COMPLETE / LIVE VERIFIED**. Do not redo VPS bootstrap unless new evidence proves it broken.
2. Treat AI provider architecture and deep character-profile schema as established foundations; extend them rather than replacing them.
3. Read `config/characters/darian.canonical.json` and `config/characters/darian.runtime-defaults.json` before instantiating Darian.
4. Begin **P1 Living Darian Minimum** with a bounded Home/world seed and validated action loop.
5. Keep model integration simple for the first living loop: one selected cognition binding is enough; do not prematurely build fallback chains or multi-role cognition.
6. Preserve separation between canonical authored definitions and mutable live runtime state.
7. After every material change, update this file with the new strongest verified state and the exact next resume point.
