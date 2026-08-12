# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Purpose: deterministic project recovery across ChatGPT sessions and protection against memory drift.
Last synchronized: 2026-08-13 — P0 remote deployment/control is COMPLETE / LIVE VERIFIED. P1 Living Darian Minimum is IN PROGRESS. Home/Darian/state/action/time/event mechanics and model-backed structured-decision adapters are implemented. The current live-cognition plan is GEMINI-FIRST for early testing; NanoGPT remains supported but is not the current primary because the Creator's subscription quota is temporarily exhausted.

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

Live baseline remains intentionally stationary until controlled real-model verification:
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

### Current Gemini-first decision

For early P1 testing use Gemini first. NanoGPT remains implemented and subscription-first but is temporarily secondary.

`src/observer_sandbox/ai_bootstrap.py` implements catalog-driven Gemini cognition bootstrap:
- enable Gemini;
- fetch the live Gemini catalog using the configured API key;
- consider usable `generateContent` Flash-family models;
- prefer stable Flash-Lite, then stable Flash;
- avoid preview/experimental/image/TTS/audio/embedding/live variants for the bootstrap selection;
- exact model IDs are never hard-coded;
- bind the selected returned model to `character:char_darian / cognition`;
- preserve any existing binding unless explicitly forced, so later Telegram/user model choices are not silently overwritten by deploys.

CLI command: `sandboxctl ai bootstrap-gemini-cognition`.

Deploy automatically attempts this bootstrap only when a non-empty `OBSERVER_GEMINI_API_KEY` exists. If no key exists, deployment remains healthy and cognition binding stays unset.

Future Telegram model control must wrap the existing provider/catalog/binding layer so the Creator can refresh provider catalogs, inspect available models, see the active binding, and change Darian/engine model assignments without code changes. Deploy must not overwrite a model choice made through Telegram.

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

P0 deployment/readback is live verified. P1 mechanics are CI validated, deployed, and live-read verified. Gemini dynamic-bootstrap code/tests are implemented; deployment with no Gemini secret safely skips binding. Continuous live autonomy remains disabled until a real Gemini credential is provisioned and one controlled model decision is verified.

## Remote operation policy

Normal VPS work goes through GitHub Actions. Do not ask the Creator for Termux/root commands unless an unavoidable host/bootstrap-level issue cannot be handled through the established lane.

## Roadmap

- P0 Foundation & Remote Control: COMPLETE / LIVE VERIFIED.
- P0.5 Provider Layer: FOUNDATION COMPLETE; Gemini/NanoGPT structured decision adapters implemented.
- Deep Character Profile: IMPLEMENTED; Darian instantiated live.
- P1 Living Darian Minimum: IN PROGRESS; real Gemini credential/catalog/binding/single-decision verification and controlled autonomy remain.
- P2 Telegram Observer: next after P1; include provider/model fetch + binding/change controls.
- P3 Rich State & Memory: later.
- P4 First simulation module: later.
- P5 Second character: later.

## RESUME HERE

1. Do not redo VPS bootstrap or P1 mechanics.
2. Keep `autonomy_enabled=false` until controlled live Gemini decision verification passes.
3. Next external requirement: GitHub Actions secret `OBSERVER_GEMINI_API_KEY`.
4. After the secret is added, deploy through the normal Actions lane. Deployment should provision the secret, refresh Gemini's live catalog, select a stable Flash-family candidate dynamically, and bind it to Darian cognition only if no binding already exists.
5. Verify credential presence, fetched catalog, selected binding, and one real structured decision. Never expose the key.
6. Only after the single-decision test passes should continuous live autonomy be enabled.
7. P2 Telegram must later provide model catalog refresh/list/selection/rebinding using this same backend, not hard-coded model IDs.
8. Synchronize this file after every material change/live proof.
