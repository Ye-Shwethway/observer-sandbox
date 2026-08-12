# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Purpose: deterministic project recovery across ChatGPT sessions and protection against memory drift.
Last synchronized: 2026-08-13 — P0 remote deployment/control is COMPLETE / LIVE VERIFIED. P1 Living Darian Minimum is IN PROGRESS. Home/Darian/state/action/time/event mechanics, Gemini-first live cognition, and a non-mutating live decision dry-run are verified. Continuous character autonomy remains intentionally disabled by Creator instruction and is NOT yet production-ready after autonomy-engine audit.

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

## Project scope / anti-sprawl

Observer Sandbox is intentionally small and modular, not another EIDOLON/Simiverse-scale architecture.

Initial product: one Home, one character (Darian), autonomous structured actions, persistent state/events, later Telegram observation/control, then progressively richer physiology/memory/relationships.

Core principle: **deep profile, partial simulation**.

## Architecture contract

Logical world model: graph. Physical persistence: SQLite relational tables.

Core model: Entity + Relation + State + Capability.

Definitions/templates live in Git/config. Mutable instances/runtime state live in DB. Deploys must not overwrite mutable live state.

LLM flow:
1. runtime prepares current state/topology/local capabilities;
2. model proposes exactly one structured action;
3. runtime validates action/topology/prerequisites;
4. only validated transition mutates DB;
5. simulated time advances at action/event boundaries;
6. event history is durable.

The LLM never gets arbitrary DB-write authority.

Primary architecture reference: `docs/ARCHITECTURE.md`.

## Darian profile boundary

Canonical fixture: `config/characters/darian.canonical.json`.
Runtime defaults: `config/characters/darian.runtime-defaults.json`.
DB schema version: 3.

Locked profile facts include 6'4", 215 lb, 9% body fat, IQ 140, approved RAPS values, rich measurements/genetic/visual/skill/preference/routine data, and first-class intimate anatomy.

Canonical penis measurement: 10 x 5 inches.

Sexual physiology semantics:
- `erectile_state`: flaccid | developing | erect | subsiding;
- `erection_firmness`: contextual simulated 0-100;
- flaccid baseline firmness 0 is normal, not dysfunction;
- Darian `erection_firmness_cap`: 100;
- `arousal_level`: separate dynamic field;
- runtime default: flaccid / firmness 0 / arousal 0.

## P1 established mechanics

World seed: `config/worlds/home.v1.json`.
Home v1: Bedroom, Kitchen, Bathroom, Living Room, Home Gym; 15 useful objects.
Runtime modules: `src/observer_sandbox/world.py`, `src/observer_sandbox/simulation.py`.
Live character: `char_darian`.

P1 runtime fields include location, current action, energy, hunger, thirst, sleepiness, cleanliness. Energy is reserve/high-good. Hunger/thirst/sleepiness are pressure/high-bad. Values clamp 0-100.

Validated action vocabulary: move, sleep, eat, drink, shower, rest, inspect, use, train, read, idle.

Movement is graph constrained; no teleporting. Completed actions write durable `action_completed` events. CI proves Darian can complete exactly 24 simulated hours with the deterministic `BaselineLivingPolicy` without mutating production time.

Live baseline remains intentionally stationary:
- Bedroom;
- idle;
- energy 75;
- hunger 20;
- thirst 15;
- sleepiness 15;
- cleanliness 80;
- sim time `2025-05-01T07:00:00+00:00`;
- `autonomy_enabled=false`.

## AI provider/model architecture

Model IDs are never hard-coded into character or engine logic.

Registry: Gemini, NanoGPT, OpenAI, OpenRouter.
Resolution: Provider -> Catalog -> Model Binding -> Runtime Adapter.
Binding precedence: task/role -> character/role -> engine/role -> character default -> global role -> global default.

`src/observer_sandbox/ai_runtime.py` supports structured P1 decisions for Gemini and NanoGPT. Required output keys: `action`, `duration_minutes`, `target`, `reason`.

`src/observer_sandbox/model_decision.py` resolves the logical cognition binding, enriches the state with reachable rooms/local objects, and returns an `Action`; runtime validation still remains authoritative.

Secrets are provisioned by GitHub Actions to `/var/lib/observer-sandbox/secrets.env` mode 0600. Never log or expose secret values.

### Current Gemini-first live state

NanoGPT remains implemented/subscription-first but is temporarily secondary. Gemini is the current early-P1 provider.

`src/observer_sandbox/ai_bootstrap.py` performs catalog-driven Gemini bootstrap and preserves existing user/model bindings unless explicitly forced.

Deploy #38 / run `31632060868` proved:
- Gemini secret provisioned privately;
- live Gemini catalog refresh returned 52 models;
- dynamic selector chose `gemini-3.5-flash-lite`;
- binding created for `character:char_darian / cognition`;
- service healthy;
- Darian state/time unchanged;
- `autonomy_enabled=false` unchanged.

The Gemini generateContent structured-output REST contract was corrected after the first dry-run exposed HTTP 400. Current adapter uses `responseMimeType=application/json` plus `responseJsonSchema`.

## Controlled live dry-run proof

Reusable CLI: `sandboxctl ai dry-run-decision`.
Workflow: `.github/workflows/dry-run-decision.yml`.

The dry-run loads the live credential, snapshots Darian, records event count, requests exactly one Gemini proposal, runs `validate_action`, then asserts snapshot and event count are unchanged. Any mutation fails the command.

Dry Run Darian Decision #3 / run `31632548092`: **SUCCESS**.

Gemini proposed:
- action: `rest`;
- duration: 30 minutes;
- target: `obj_bed`;
- reason: `Resting for a short duration to maintain energy.`

Validation passed and invariants proved:
- `mutated=false`;
- events before=0, after=0;
- Darian state before/after identical;
- sim time remained `2025-05-01T07:00:00+00:00`;
- `autonomy_enabled=false` remained unchanged.

This dry-run also exposed a validator gap: a non-move action can currently carry a semantically unnecessary/unchecked target (`rest` targeted `obj_bed`) and still pass. Fix before continuous autonomy.

## Autonomy-engine audit — current boundary

Continuous autonomy is NOT complete yet.

Established pieces:
- persistent world/character state;
- validated atomic action application;
- event-driven simulated time inside action application;
- deterministic one-day acceptance loop;
- model-backed decision provider;
- provider/catalog/binding abstraction;
- live Gemini structured decision generation;
- non-mutating dry-run safety path.

Missing or insufficient before production autonomy:
1. `src/observer_sandbox/service.py` currently only initializes DB and sleeps; it does not run an autonomy worker.
2. `autonomy_enabled`, `paused`, and `speed` are stored but not consumed by a live scheduling loop.
3. No persistent pending/in-progress action scheduler exists for crash-safe resume at action/event boundaries.
4. No lease/lock prevents duplicate concurrent cognition/action execution.
5. Validator target semantics are incomplete for non-move actions; object-targeted actions need local-object/capability validation and irrelevant targets should be rejected/normalized.
6. Available actions given to the model are currently a static vocabulary rather than context-filtered action specifications.
7. Model context is still too thin for believable Darian behavior: current needs/topology/local objects are present, but canonical personality, routines, preferences, skills, recent events/memory, and stronger time-of-day guidance are not yet integrated. The generic 07:00 `rest` proposal demonstrates this limitation.
8. Model-chosen duration only has a global 1-720 bound; action-specific duration/default limits are needed.
9. No robust retry/backoff/fallback path exists for API errors, rate limits, invalid JSON, invalid actions, or quota exhaustion.
10. No explicit rejected-decision/error audit events/metrics exist.
11. The existing one-day autonomy acceptance test proves `BaselineLivingPolicy`, not live-model continuous autonomy.

Do NOT set `autonomy_enabled=true` until these P1 autonomy-runtime gaps are addressed and controlled bounded-live acceptance passes.

## Production boundary

Repository: `Ye-Shwethway/observer-sandbox` private.
VPS: `107.175.30.238`, Ubuntu 24.04.
App: `/opt/observer-sandbox`.
DB: `/var/lib/observer-sandbox/observer.sqlite3`.
Service: `observer-sandbox` systemd.
SSH/runtime user: `observer`.
DB is not publicly exposed.

Deployment path: GitHub main -> Actions -> SSH/rsync -> app install -> DB init/migration -> AI-secret/cognition setup -> systemd restart -> verification.

Normal VPS work goes through GitHub Actions. Do not ask the Creator for Termux/root commands unless an unavoidable host/bootstrap-level issue cannot be handled through the established lane.

## Roadmap

- P0 Foundation & Remote Control: COMPLETE / LIVE VERIFIED.
- P0.5 Provider Layer: FOUNDATION COMPLETE; Gemini live credential/catalog/binding verified.
- Deep Character Profile: IMPLEMENTED; Darian instantiated live.
- P1 Living Darian Minimum: IN PROGRESS. Mechanics + live Gemini decision path are established, but production continuous autonomy runtime still needs the audit gaps above fixed.
- P2 Telegram Observer: after P1; include provider/model refresh/list/rebinding controls.
- P3 Rich State & Memory: later.
- P4 First simulation module: later.
- P5 Second character: later.

## RESUME HERE

1. Keep `autonomy_enabled=false` until Creator explicitly approves and P1 autonomy-runtime acceptance passes.
2. Do not redo VPS bootstrap, Gemini secret provisioning, catalog bootstrap, or dry-run plumbing.
3. Current live cognition binding is `gemini / gemini-3.5-flash-lite` for `character:char_darian / cognition`, dynamically selected from the live catalog.
4. Next work: harden action contracts/context, build the actual service autonomy scheduler/worker with pause/speed/lease/crash-resume semantics, add retries/fallback/audit logging, then run bounded live-model acceptance without turning on indefinite autonomy.
5. P2 Telegram later wraps the same provider/catalog/binding backend for model fetch/change.
6. Synchronize this file after every material change/live proof.
