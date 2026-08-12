# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Purpose: deterministic project recovery across ChatGPT sessions and protection against memory drift.
Last synchronized: 2026-08-13 — P0 LIVE VERIFIED. P1 Living Darian core runtime/cognition/autonomy hardened; first production canary passed; continuous production autonomy intentionally OFF. P2.1 Telegram Observer MVP is IMPLEMENTED / CI-VALIDATED / DEPLOYED / TRANSPORT-LIVE. Telegram Bot API connectivity, Owner ID, and Allowed User configuration are live verified.

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

## Current live production

Repository: `Ye-Shwethway/observer-sandbox` (private)
VPS: `107.175.30.238`, Ubuntu 24.04
App: `/opt/observer-sandbox`
DB: `/var/lib/observer-sandbox/observer.sqlite3`
Service: `observer-sandbox` systemd
Runtime user: `observer`
Schema version: 3
DB is not publicly exposed.

Latest verified runtime state:
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
- NanoGPT credential absent;
- Telegram bot token present;
- Telegram Bot API connectivity verified true;
- Telegram Owner ID present;
- Telegram Allowed Users configured.

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

First real production autonomous action passed:
- Bedroom -> Living Room;
- 07:00 -> 07:05;
- reason: moving out of bedroom to begin morning training routine;
- canary auto-disabled afterward.

`sandboxctl autonomy canary-once` is synchronous/bounded and completes exactly one action through the normal scheduler path before auto-disabling.
Continuous production autonomy remains OFF until the Creator explicitly approves activation after Telegram observation acceptance.

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

## P2.1 implementation / live state

Implemented files:
- `src/observer_sandbox/observer_query.py` — reusable generic observer/query service;
- `src/observer_sandbox/telegram_bot.py` — Telegram Bot API transport + command routing + role-aware authorization;
- `src/observer_sandbox/service.py` — starts Telegram polling thread when token exists;
- `tests/test_observer_query.py`;
- `tests/test_telegram_bot.py`.

Telegram transport uses Bot API long polling (`getUpdates`) and `sendMessage`; no webhook, public HTTP listener, extra port, or third-party Python dependency is required for P2.1.
Polling advances offset to last processed update id + 1. Only private chats are processed.

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

Authorization roles:
1. **Owner** — one privileged Telegram user id from `OBSERVER_TELEGRAM_OWNER_ID`. Owner is automatically authorized and wins precedence even if duplicated in the normal allowlist.
2. **Allowed user** — zero or more ids from comma-separated `OBSERVER_TELEGRAM_ALLOWED_USER_IDS`.
3. **Unauthorized user** — no world data/control; `/start` and `/whoami` may reveal only caller identity/bootstrap authorization state.

The Creator currently configured their own ID in both Owner and Allowed Users. This is redundant but harmless because Owner precedence is authoritative. Future cleanup may remove the duplicate from Allowed Users without changing behavior.

`/whoami` reports Telegram user id and role for authorized callers.
Future user management should be owner-only. Ordinary allowed users must never replace, remove, demote, or self-grant Owner authority. Environment-backed Owner ID remains bootstrap/root trust anchor unless an explicit later migration changes this design.

Secrets:
- `OBSERVER_TELEGRAM_BOT_TOKEN`
- `OBSERVER_TELEGRAM_OWNER_ID`
- `OBSERVER_TELEGRAM_ALLOWED_USER_IDS`

All are provisioned through `/var/lib/observer-sandbox/secrets.env` mode 0600; values must never be logged.

Verification evidence:
- CI #137 / run `31637361430`: SUCCESS for owner/allowed separation.
- Telegram Runtime Read #1 / run `31638174375`: SUCCESS; `TELEGRAM_API_OK=true`, Owner present, Allowed Users present.
- Deploy #73 / run `31638254979`: SUCCESS; service active, production Darian/autonomy unchanged, `TELEGRAM_BOT_TOKEN_PRESENT=true`, `TELEGRAM_API_CONNECTED=true`, `TELEGRAM_OWNER_ID_PRESENT=true`, `TELEGRAM_ALLOWED_USERS_PRESENT=true`.
- Earlier Deploy #70-72 failures were verifier false-negatives, not Telegram credential failures. The deploy verifier is now JSON-parser based and fixed.

P2.1 transport is therefore LIVE. End-to-end Creator acceptance still requires the Creator to open the bot and exercise live commands such as `/whoami`, `/status`, `/watch`, and `/home` from Telegram.

## P2 staging

### P2.1 — Mobile Observer MVP (ACTIVE, transport live)
Remaining acceptance:
1. Creator opens the Telegram bot and sends `/whoami` or `/status`;
2. confirm reply role is Owner and live sandbox data is visible;
3. exercise `/watch`, `/history`, `/darian`, `/home`;
4. optionally verify `/pause`, `/resume`, `/speed` while autonomy remains disabled;
5. then decide continuous autonomy activation conditions.

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
- P2 Telegram Observer: ACTIVE. P2.1 transport LIVE; awaiting Creator end-to-end command acceptance before continuous autonomy decision.
- P3 Rich State & Memory: later.
- P4 First simulation module: later.
- P5 Second character: later; observer architecture is already generic/multi-character ready.

## RESUME HERE

1. Continuous production autonomy is OFF. Do not enable it until Creator explicitly approves after Telegram acceptance.
2. Do not redo P0/P1/Gemini/canary work unless newer evidence shows regression.
3. Telegram transport is live; next step is Creator end-to-end command test from Telegram.
4. Creator ID duplicated in Owner and Allowed Users is harmless; Owner role wins.
5. Keep Telegram handlers thin; future rooms/items/full profiles/character selection go through generic query services.
6. Continuous `enable` remains intentionally absent from remote Actions control workflow until post-Telegram approval.
7. Synchronize this file after every material change/live proof.
