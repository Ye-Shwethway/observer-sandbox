# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Purpose: deterministic project recovery across ChatGPT sessions and protection against memory drift.
Last synchronized: 2026-08-13 — P0 is LIVE VERIFIED. P1 Living Darian core runtime/cognition/autonomy is hardened and first production canary passed; continuous production autonomy remains intentionally OFF. P2.1 Telegram Observer MVP code is IMPLEMENTED / CI-VALIDATED / DEPLOYED. Telegram authorization now separates one privileged Owner identity from ordinary Allowed Users. Telegram transport is not live yet because no bot token is provisioned.

## HARD RECOVERY RULES

Read `AGENTS.md` first, then this file, then task-relevant repo files before changing the project.
After every material repository or verified runtime change, update this file in the same work session/change set.
Never conflate committed, CI-validated, deployed, DB-applied, and live-verified state.

Authority order:
1. Explicit current Creator instruction.
2. Current canonical repo config/schema/architecture.
3. Verified live VPS/runtime/DB evidence.
4. Deployed repo/workflow evidence.
5. Current CI/test evidence.
6. This bootstrap.
7. Older chat/model memory.

Telegram is a Creator-facing observer/control adapter only. Python runtime remains state-transition authority. AI models only propose structured actions. Telegram handlers must not become a second business-logic layer.

## Project architecture

Observer Sandbox is intentionally small/modular. Core principle: **deep profile, partial simulation**.
Logical world model: graph; persistence: SQLite relational tables; core model: Entity + Relation + State + Capability.
Definitions/templates live in Git/config; mutable instances/runtime state live in DB. Deploys must not overwrite mutable live state.

LLM decision flow:
1. runtime builds current state + character context + valid action options;
2. model proposes one structured action;
3. runtime validates target/topology/capability/duration;
4. scheduler persists pending action;
5. when due, runtime applies exactly one transition and advances sim time;
6. durable events + action ids protect recovery/idempotency.

## Current live production

Repository: `Ye-Shwethway/observer-sandbox` (private)
VPS: `107.175.30.238`, Ubuntu 24.04
App: `/opt/observer-sandbox`
DB: `/var/lib/observer-sandbox/observer.sqlite3`
Service: `observer-sandbox` systemd
Runtime user: `observer`
Schema version: 3
DB is not publicly exposed.

Latest verified state:
- service healthy/active;
- autonomy_enabled=false;
- autonomy_mode=normal;
- paused=false;
- speed=1.0;
- pending_action=null;
- retry=null;
- Darian: Living Room / idle / 2025-05-01T07:05:00+00:00;
- energy 74.75, hunger 20.333, thirst 15.417, sleepiness 15.292, cleanliness 79.9;
- Gemini credential present;
- NanoGPT credential absent.

## Darian / P1 boundary

Canonical fixture: `config/characters/darian.canonical.json`
Runtime defaults: `config/characters/darian.runtime-defaults.json`
Autonomy policy: `config/characters/darian.autonomy-policy.json` (`darian-autonomy-p1-v1.2`)
World seed: `config/worlds/home.v1.json`

Home v1: Bedroom, Kitchen, Bathroom, Living Room, Home Gym; 15 useful objects.
Action vocabulary: move, sleep, eat, drink, shower, rest, inspect, use, train, read, idle.
Action validator enforces action-specific duration bounds, room adjacency, local object/capability requirements, and context-specific action options.

AI provider architecture: Provider -> Catalog -> Model Binding -> Runtime Adapter.
Registry includes Gemini, NanoGPT, OpenAI, OpenRouter. Model IDs are not hard-coded into character/engine logic.
Current live cognition binding: `gemini / gemini-3.5-flash-lite` for `character:char_darian / cognition`, dynamically selected from the live Gemini catalog.

Persistent scheduler: `src/observer_sandbox/autonomy.py`; service ticks about every 2 seconds.
It supports disabled/paused state, speed scaling, durable pending actions, lease protection, idempotent crash recovery, error audit events, exponential backoff, and fail-closed behavior.

Real Gemini behavior matrix passed 5/5: morning training path, thirst/hydration, hunger/food, critical overnight sleep (480m), hygiene.

First real production autonomous action already passed:
- Bedroom -> Living Room;
- 07:00 -> 07:05;
- reason: moving out of bedroom to begin morning training routine;
- canary auto-disabled afterward.

`sandboxctl autonomy canary-once` is synchronous/bounded and completes exactly one action through the normal scheduler path before auto-disabling.
Continuous production autonomy remains OFF until the Telegram observation surface is usable and the Creator explicitly approves activation.

## P2 Telegram Observer — canonical architecture

Design doc: `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`.
Long-term goal is **observe the universe**, not a Darian-status-only bot.

Future navigation model:
- Universe -> Location -> Sublocation/Room -> Contents/Items
- Characters -> selected character -> current state / full profile / history / later inventory / relationships / physiology
- Provider/model browsing + refresh + binding changes later
- Owner-managed user access later

Stable IDs drive backend queries. `/darian` and `/home` are MVP convenience entry points only; they call generic character/location query services.
Telegram presentation/session state may remember selected resources later, but authoritative world state remains in runtime/DB.

## P2.1 implementation state

Implemented files:
- `src/observer_sandbox/observer_query.py` — reusable generic observer/query service;
- `src/observer_sandbox/telegram_bot.py` — Telegram Bot API transport + command routing + role-aware authorization;
- `src/observer_sandbox/service.py` — starts Telegram polling thread only when token exists;
- `tests/test_observer_query.py`;
- `tests/test_telegram_bot.py`.

Telegram transport uses official Bot API long polling (`getUpdates`) and `sendMessage`; no webhook, public HTTP listener, extra port, or third-party Python dependency is required for P2.1.
Polling advances `offset` to last processed update id + 1 to avoid duplicate updates.
Only private chats are processed.

Current MVP commands:
- `/start`, `/help`
- `/status`
- `/watch`
- `/history [n]`
- `/darian`
- `/home`
- `/pause`
- `/resume`
- `/speed <value>`
- `/whoami`

## Telegram authorization model

Authorization is deliberately split into three roles:

1. **Owner** — one privileged Telegram user id from `OBSERVER_TELEGRAM_OWNER_ID`. Owner is automatically authorized and does not need to appear in the normal allowlist.
2. **Allowed user** — zero or more ids from comma-separated `OBSERVER_TELEGRAM_ALLOWED_USER_IDS`. These users can use the currently exposed observer/control surface but are not the root authority for future user management.
3. **Unauthorized user** — no world data/control. `/start` and `/whoami` may reveal only that caller's own Telegram id and authorization state for bootstrap.

`/whoami` reports both Telegram user id and role for authorized callers.

Future user management should be owner-only and may add persistent list/add/remove/role operations. Ordinary allowed users must never be able to replace, remove, demote, or self-grant Owner authority. The environment-backed Owner ID remains the bootstrap/root trust anchor unless a later explicit migration changes this design.

Telegram credential/config secrets:
- `OBSERVER_TELEGRAM_BOT_TOKEN`
- `OBSERVER_TELEGRAM_OWNER_ID`
- `OBSERVER_TELEGRAM_ALLOWED_USER_IDS`

All are provisioned only through `/var/lib/observer-sandbox/secrets.env` mode 0600; values are never logged.

GitHub deployment provisions all three fields separately and reports only boolean presence for the bot token / owner id.

Authorization tests cover:
- unauthorized identity-only bootstrap;
- Owner authorized without duplicate allowlist entry;
- Allowed User distinct from Owner;
- unauthorized users denied world/control data;
- existing MVP observer/control commands remain functional for authorized users.

CI #137 / run `31637361430`: SUCCESS.
Deploy #69 / run `31637361275`: SUCCESS.
The owner/allowed-user role split is therefore code-validated and deployed. Telegram transport remains inactive until a bot token is provided.

## P2 staging

### P2.1 — Mobile Observer MVP (ACTIVE)
Acceptance: Creator can independently open Telegram and inspect/control the basic live sandbox without relying on ChatGPT narration.
Remaining steps:
1. create/select Telegram bot via BotFather;
2. add GitHub Actions secret `OBSERVER_TELEGRAM_BOT_TOKEN`;
3. deploy and verify Bot API connectivity;
4. Creator sends `/start` or `/whoami` to retrieve Telegram user id;
5. set that id as GitHub Actions secret `OBSERVER_TELEGRAM_OWNER_ID`;
6. optionally configure `OBSERVER_TELEGRAM_ALLOWED_USER_IDS` separately for additional users; Owner must not be duplicated there;
7. redeploy;
8. live-test `/whoami`, `/status`, `/watch`, `/history`, `/darian`, `/home`, pause/resume/speed;
9. only then consider continuous autonomy activation.

### P2.2 — Browse the sandbox
- location list/selection;
- room navigation;
- room contents and item details;
- character list/selection;
- detailed profile section browsing/pagination.

### P2.3 — Creator control expansion
- owner-only user management;
- provider/model catalog browse/refresh;
- dynamic binding change;
- richer controls/history filtering;
- later watch/notification preferences.

## Roadmap

- P0 Foundation & Remote Control: COMPLETE / LIVE VERIFIED.
- P0.5 Provider Layer: FOUNDATION COMPLETE; Gemini live binding verified.
- Deep Character Profile: IMPLEMENTED / live Darian instantiated.
- P1 Living Darian Minimum: CORE + HARDENING + FIRST PRODUCTION CANARY COMPLETE / LIVE VERIFIED; continuous autonomy OFF.
- P2 Telegram Observer: ACTIVE. P2.1 code/deploy foundation complete; Owner vs Allowed User architecture implemented/deployed; waiting for Telegram bot credential + Owner ID live acceptance.
- P3 Rich State & Memory: later.
- P4 First simulation module: later.
- P5 Second character: later; observer architecture is already generic/multi-character ready.

## RESUME HERE

1. Do not enable continuous production autonomy before Telegram is live unless Creator explicitly overrides this gate.
2. Do not redo P0/P1/Gemini/canary work unless newer evidence shows regression.
3. P2.1 code is already deployed; next blocker is `OBSERVER_TELEGRAM_BOT_TOKEN`.
4. After token provisioning, deploy, then use `/start` or `/whoami` to obtain Creator Telegram user id without exposing world data.
5. Set Creator id in `OBSERVER_TELEGRAM_OWNER_ID`; do not duplicate it in `OBSERVER_TELEGRAM_ALLOWED_USER_IDS`.
6. Additional users belong only in `OBSERVER_TELEGRAM_ALLOWED_USER_IDS`; future user-management mutations must be Owner-only.
7. Keep Telegram handlers thin; add future rooms/items/full profiles/character selection through generic query services rather than bot-specific DB logic.
8. Continuous `enable` remains intentionally absent from remote Actions control workflow until post-Telegram approval.
9. Synchronize this file after every material change/live proof.
