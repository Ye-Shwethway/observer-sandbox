# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Purpose: deterministic project recovery across ChatGPT sessions and protection against memory drift.
Last synchronized: 2026-08-13 — P0 remote deployment/control is COMPLETE / LIVE VERIFIED. P1 Living Darian Minimum is IN PROGRESS. Home/Darian/state/action/time/event mechanics and model-backed structured-decision adapters are implemented. Gemini-first live cognition is now provisioned and bound from the live catalog, while character autonomy remains intentionally disabled by Creator instruction.

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

## P1 Living Darian Minimum — established mechanics

World seed: `config/worlds/home.v1.json`.

Home v1: Bedroom, Kitchen, Bathroom, Living Room, Home Gym; 15 useful objects.

Runtime modules: `src/observer_sandbox/world.py`, `src/observer_sandbox/simulation.py`.

Live character: `char_darian`.

P1 runtime fields include location, current action, energy, hunger, thirst, sleepiness, cleanliness. Energy is reserve/high-good. Hunger/thirst/sleepiness are pressure/high-bad. Values clamp 0-100.

Validated actions: move, sleep, eat, drink, shower, rest, inspect, use, train, read, idle.

Movement is graph constrained; no teleporting. Completed actions write durable `action_completed` events. CI proves Darian can complete exactly 24 simulated hours with bounded deterministic acceptance policy without mutating production time.

Live baseline remains intentionally stationary until explicitly enabled later:
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

`src/observer_sandbox/ai_runtime.py` supports structured P1 decisions for Gemini and NanoGPT. Required output keys: `action`, `duration_minutes`, `target`, `reason`. `src/observer_sandbox/model_decision.py` resolves the logical cognition binding and still passes the returned action through runtime validation.

Secrets are provisioned by GitHub Actions to `/var/lib/observer-sandbox/secrets.env` mode 0600. Never log or expose secret values.

### Current Gemini-first live state

For early P1 testing use Gemini first. NanoGPT remains implemented and subscription-first but is temporarily secondary.

`src/observer_sandbox/ai_bootstrap.py` implements catalog-driven Gemini cognition bootstrap:
- enable Gemini;
- fetch the live Gemini catalog using the configured API key;
- consider usable `generateContent` Flash-family models;
- prefer stable Flash-Lite, then stable Flash;
- avoid preview/experimental/image/TTS/audio/embedding/live variants for bootstrap selection;
- exact model IDs are never hard-coded;
- bind the selected returned model to `character:char_darian / cognition`;
- preserve any existing binding unless explicitly forced, so later Telegram/user model choices are not silently overwritten by deploys.

CLI command: `sandboxctl ai bootstrap-gemini-cognition`.

Live verification from Deploy #38 / run id `31632060868` / commit `16ffaed0069c0297b119aa728867f7333b5017b2`:
- `OBSERVER_GEMINI_API_KEY` was present in GitHub Actions and provisioned to VPS private `secrets.env` without exposure;
- Gemini catalog refresh succeeded with **52 models**;
- dynamic bootstrap selected **`gemini-3.5-flash-lite`** from the returned live catalog;
- binding created: provider `gemini`, scope `character:char_darian`, role `cognition`, model `gemini-3.5-flash-lite`;
- service restarted and was active;
- live runtime stayed healthy on schema v3;
- Darian's location/needs/current action/sim time remained unchanged;
- `autonomy_enabled=false` remained unchanged as explicitly requested.

This binding is a current operational choice, not a hard-coded architectural default. Later Telegram model controls must use the same provider/catalog/binding backend to refresh available models, inspect active bindings, and change model assignments without code changes. Deploy must preserve an existing user-selected binding unless explicitly forced.

NanoGPT remains subscription-safe: subscription catalog/usage/generation paths are retained and no upstream-provider forcing is used by default.

## Production boundary

Repository: `Ye-Shwethway/observer-sandbox` private.
VPS: `107.175.30.238`, Ubuntu 24.04.
App: `/opt/observer-sandbox`.
DB: `/var/lib/observer-sandbox/observer.sqlite3`.
Service: `observer-sandbox` systemd.
SSH/runtime user: `observer`.
DB is not publicly exposed.

Deployment path: GitHub main -> Actions -> SSH/rsync -> app install -> DB init/migration -> optional AI-secret/cognition setup -> systemd restart -> status/living-state/binding verification.

P0 deployment/readback is live verified. P1 mechanics are CI validated, deployed, and live-read verified. Gemini credential provisioning, live catalog fetch, and Darian cognition binding are now live verified. Continuous live autonomy remains disabled by Creator instruction.

## Remote operation policy

Normal VPS work goes through GitHub Actions. Do not ask the Creator for Termux/root commands unless an unavoidable host/bootstrap-level issue cannot be handled through the established lane.

## Roadmap

- P0 Foundation & Remote Control: COMPLETE / LIVE VERIFIED.
- P0.5 Provider Layer: FOUNDATION COMPLETE; Gemini/NanoGPT structured decision adapters implemented; Gemini live credential/catalog/binding verified.
- Deep Character Profile: IMPLEMENTED; Darian instantiated live.
- P1 Living Darian Minimum: IN PROGRESS; real Gemini cognition is bound, but live autonomy is intentionally not enabled yet. Next safe step is a controlled one-decision verification that does not begin continuous progression.
- P2 Telegram Observer: next after P1; include provider/model fetch + binding/change controls.
- P3 Rich State & Memory: later.
- P4 First simulation module: later.
- P5 Second character: later.

## RESUME HERE

1. Do not redo VPS bootstrap, secret provisioning, or Gemini catalog bootstrap unless newer evidence shows a problem.
2. Keep `autonomy_enabled=false` until Creator explicitly approves enabling it.
3. Current live cognition binding is `gemini / gemini-3.5-flash-lite` for `character:char_darian / cognition`, selected dynamically from a 52-model live catalog.
4. Next safe verification is one controlled Gemini decision proposal with mutation either disabled or tightly bounded; do not start a continuous autonomous loop yet.
5. P2 Telegram must later provide model catalog refresh/list/selection/rebinding using this same backend, not hard-coded model IDs.
6. Synchronize this file after every material change/live proof.
