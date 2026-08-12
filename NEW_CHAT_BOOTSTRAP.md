# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Purpose: deterministic project recovery across ChatGPT sessions and protection against memory drift.
Last synchronized: 2026-08-13 — P0 LIVE VERIFIED. P1 Living Darian autonomy is CONTINUOUSLY LIVE at 1x with wake-on-demand cognition. P2.1 Telegram Observer is live. P2.2.1 Observer Home + inline navigation is IMPLEMENTED / CI-VALIDATED / DEPLOYED. Per-user Telegram notifications are persistent, default ON, and governed by a shared notification policy.

## HARD RECOVERY RULES

Read `AGENTS.md` first, then this file, then task-relevant repo files before changing the project. For roadmap/phase decisions, read `ROADMAP.md`. For Telegram work, always read `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`; for proactive notifications also read `docs/TELEGRAM_NOTIFICATION_POLICY.md`.
After every material repository or verified runtime change, update this file in the same work session/change set.
Never conflate committed, CI-validated, deployed, DB-applied, and live-runtime verified state.

Authority order:
1. Explicit current Creator instruction.
2. Current canonical repo config/schema/architecture.
3. Verified live VPS/runtime/DB evidence.
4. Deployed repo/workflow evidence.
5. Current CI/test evidence.
6. This bootstrap.
7. Older chat/model memory.

Telegram is a Creator-facing observer/control adapter only. Python runtime remains state-transition authority. AI models only propose structured actions. Telegram handlers must not become a second business-logic layer.

## Current production baseline

Repository: `Ye-Shwethway/observer-sandbox` (private)
VPS: `107.175.30.238`, Ubuntu 24.04
App: `/opt/observer-sandbox`
DB: `/var/lib/observer-sandbox/observer.sqlite3`
Service: `observer-sandbox` systemd
Runtime user: `observer`
Schema version: 3
DB is not publicly exposed.

Previously verified continuous-autonomy baseline:
- service healthy/active;
- autonomy_enabled=true;
- autonomy_mode=normal;
- paused=false;
- speed=1.0;
- retry=null;
- continuous wake-on-demand autonomy started successfully;
- first continuous cognition wake produced exactly one model call;
- first continuous action was `move -> room_gym` from Living Room, 10 simulated minutes / 10 wall minutes at 1x;
- reason: moving toward the home gym to begin the morning physical training routine;
- Gemini credential present;
- Telegram Bot API connectivity verified true;
- Telegram Owner ID and Allowed Users configured.

Do not treat the first-action snapshot above as the current simulated moment forever; production continues autonomously. Re-read live runtime when an exact current Darian state is required.

## Wake-on-demand cognition policy

Continuous autonomy does NOT mean continuous LLM polling.

The service may tick the scheduler about every 2 seconds, but the model mind is called only at a real decision boundary:
- autonomy is enabled;
- runtime is not paused;
- retry/backoff is not active;
- no physical action is currently pending.

While an action is pending, all scheduler ticks are deterministic and make zero LLM calls. At 1x speed, a 10-minute action creates roughly 10 wall minutes with no new cognition call; a 60-minute action creates roughly one wall hour with no new cognition call.

`src/observer_sandbox/autonomy.py` persists cognition telemetry:
- `cognition_wake_stats.decision_calls`;
- last model-call wall time;
- last model-call simulated time;
- last wake reason;
- next/queued wake reason at action boundaries.

`/status` exposes the durable `Mind Calls` count. Tests verify repeated scheduler ticks during an in-progress action do not increment model calls and that the next model wake occurs only after the action boundary.

This is the cost-control baseline for free-key operation and future paid-provider cost reduction. Do not add background reflection loops, periodic LLM heartbeats, or model calls on every service tick without explicit Creator approval.

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
It supports pause/resume, speed scaling, durable pending actions, lease protection, idempotent crash recovery, error audit events, exponential backoff, and fail-closed behavior.

First production canary passed before continuous activation. Continuous activation was explicitly approved after Telegram became live.

Activation proof:
- wake-on-demand tests: CI #148 / run `31638949447`: SUCCESS;
- continuous activation run `31639042104`: SUCCESS;
- first live wake produced exactly one cognition call and one pending action;
- `.github/workflows/autonomy-control.yml` exposes explicit `enable` alongside status/canary/disable/pause/resume/speed because Creator approval has been granted.

## P2 Telegram Observer — canonical architecture

Design doc: `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`.
Notification contract: `docs/TELEGRAM_NOTIFICATION_POLICY.md`.
Canonical phase roadmap: `ROADMAP.md`.
Long-term goal is **observe the universe**, not a Darian-status-only bot.

Future navigation model:
- Universe -> Location -> Sublocation/Room -> Contents/Items
- Characters -> selected character -> current state / full profile / history / later inventory / relationships / physiology
- Provider/model browsing + refresh + binding changes later
- Owner-managed user access later

Stable IDs drive backend queries. `/darian` and `/home` remain convenience entry points only; generic list/get query services now support worlds, locations and characters.

## Telegram presentation contract

The presentation contract is mandatory for every future Telegram command, callback, notification, menu, browse page, and detail view. It is implementation guidance in `AGENTS.md`, detailed in `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`, and a phase-acceptance rule in `ROADMAP.md`.

Creator-facing simulated timestamp format:
- `dd-mm-yyyy (Day) hh:mm AM/PM`
- example: `01-05-2025 (Thursday) 07:05 AM`
- DB/runtime timestamps remain canonical ISO-8601 internally.

Presentation conventions:
- compact Unicode/emoji headers and restrained dividers;
- friendly `Yes/No`, `ON/OFF`, title/sentence-case actions;
- internal ids resolve to human-readable names in normal views;
- default activity history hides engine/control bookkeeping;
- raw canonical events remain available for later technical/debug views;
- large profiles/contents/histories are hierarchical, sectioned or paginated;
- shared formatter/helpers are reused; business logic stays in backend services.

## P2.1 live surface

Current commands include:
- `/start`, `/help`
- `/status`
- `/watch`
- `/history [n]`
- `/darian`
- `/home`
- `/notify on|off`
- `/pause`
- `/resume`
- `/speed <value>`
- `/whoami`

Compatibility notification aliases:
- `/notification on|off`
- `/notifications on|off`
- `/notion/on`
- `/notion/off`

Authorization roles remain Owner / Allowed / Unauthorized. Owner precedence wins even if duplicated in normal allowlist.

## Telegram notification policy

Notifications are **default ON per authorized user**. Absence of a saved preference means enabled.

Preferences are persisted separately by Telegram user ID and survive service restarts/deployments. Interactive command/callback replies are not suppressed by this setting; it gates proactive notifications.

Current proactive use:
- Owner service-start notification `Universe is alive!`.

Future proactive events must reuse the same global per-user gate. Category-specific preferences may later sit underneath it. Do not create unrelated notification toggles for each new feature.

## P2.2.1 — Observer Home + inline navigation

Status: IMPLEMENTED / CI-VALIDATED / DEPLOYED.

`/start` now opens a compact Observer Home dashboard showing current Darian summary, simulated time, notification state and access role.

Inline buttons:
- `🌍 Universe`
- `👥 Characters`
- `🕒 Runtime`
- `📜 History`

Callback navigation:
- uses stable payloads such as `nav:universe`, `loc:room_gym`, `char:char_darian` rather than display labels;
- re-checks authorization server-side;
- edits the existing Telegram message instead of producing a new message for every navigation step;
- provides Back / Observer Home navigation;
- generic query layer now exposes `list_worlds`, `list_locations`, and `list_characters`.

Validation/deploy proof:
- CI #166 / run `31640797930`: SUCCESS after navigation/notification test alignment;
- Deploy #80 / run `31640709163`: SUCCESS; inline navigation + persistent notification code deployed.

Later roadmap/document-only commits do not change this runtime proof.

## P2 staging

### P2.1 — Mobile Observer MVP
Status: LIVE.

### P2.2 — Browse the sandbox
Status: IN PROGRESS.

Completed:
1. P2.2.1 Observer Home Menu + reusable inline callback/navigation framework.

Next:
2. **P2.2.2 Location hierarchy / room detail browsing**
   - Home/world -> rooms;
   - open room;
   - occupants;
   - objects/items;
   - exits/relations;
   - current room activity;
   - Back -> Universe -> Observer Home.

Then:
3. item detail browsing;
4. selected-character session state;
5. profile section browsing/pagination.

### P2.3 — Creator control expansion
- owner-only user management;
- provider/model catalog browse/refresh;
- dynamic binding change;
- richer controls/history filtering;
- later category-specific watch/notification preferences layered under the global notification gate.

## Roadmap

- P0 Foundation & Remote Control: COMPLETE / LIVE VERIFIED.
- P0.5 Provider Layer: FOUNDATION COMPLETE; Gemini live binding verified.
- Deep Character Profile: IMPLEMENTED / live Darian instantiated.
- P1 Living Darian Minimum: CONTINUOUS AUTONOMY LIVE at 1x with wake-on-demand cognition.
- P2 Telegram Observer: ACTIVE; P2.1 LIVE; P2.2.1 IMPLEMENTED/DEPLOYED; P2.2.2 room hierarchy is next.
- P3 Rich State & Memory: later.
- P4 First simulation module: later.
- P5 Second character: later; observer architecture is already generic/multi-character ready.

## RESUME HERE

1. Continuous autonomy is LIVE at 1x. Do not casually reset or reseed production state.
2. Preserve wake-on-demand cognition; no periodic LLM heartbeats/reflection by default.
3. Preserve the mandatory Telegram presentation contract.
4. Preserve per-user proactive notifications default ON and use the shared notification gate.
5. `/start` is now the primary Observer Home; extend the callback framework rather than creating a parallel navigation system.
6. Next bounded implementation slice: **P2.2.2 Location hierarchy / room detail browsing**.
7. Synchronize this file after every material change/live proof.
