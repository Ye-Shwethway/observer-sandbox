# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Purpose: deterministic project recovery across ChatGPT sessions and protection against memory drift.
Last synchronized: 2026-08-13 — P0 LIVE VERIFIED. P1 Living Darian autonomy is CONTINUOUSLY LIVE at 1x with wake-on-demand cognition. P2.1 Telegram Observer is transport-live and Creator-visible. Telegram presentation is human-friendly and now governed by a durable presentation contract in `AGENTS.md`, `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`, and canonical `ROADMAP.md`.

## HARD RECOVERY RULES

Read `AGENTS.md` first, then this file, then task-relevant repo files before changing the project. For roadmap/phase decisions, read `ROADMAP.md`. For Telegram work, always read `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`.
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

Latest verified activation state:
- service healthy/active;
- autonomy_enabled=true;
- autonomy_mode=normal;
- paused=false;
- speed=1.0;
- retry=null;
- continuous wake-on-demand autonomy has begun;
- first continuous cognition wake produced exactly one model call;
- first continuous action was `move -> room_gym` from Living Room, 10 simulated minutes / 10 wall minutes at 1x;
- reason: moving toward the home gym to begin the morning physical training routine;
- Gemini credential present;
- Telegram Bot API connectivity verified true;
- Telegram Owner ID and Allowed Users configured.

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
It supports pause/resume, 1x or configured speed scaling, durable pending actions, lease protection, idempotent crash recovery, error audit events, exponential backoff, and fail-closed behavior.

First production canary passed before continuous activation. Continuous activation was explicitly approved after Telegram became live.

Activation proof:
- wake-on-demand tests: CI #148 / run `31638949447`: SUCCESS;
- continuous activation run `31639042104`: SUCCESS;
- first live wake produced exactly one cognition call and one pending action;
- `.github/workflows/autonomy-control.yml` intentionally exposes explicit `enable` alongside status/canary/disable/pause/resume/speed because Creator approval has been granted.

## P2 Telegram Observer — canonical architecture

Design doc: `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`.
Canonical phase roadmap: `ROADMAP.md`.
Long-term goal is **observe the universe**, not a Darian-status-only bot.

Future navigation model:
- Universe -> Location -> Sublocation/Room -> Contents/Items
- Characters -> selected character -> current state / full profile / history / later inventory / relationships / physiology
- Provider/model browsing + refresh + binding changes later
- Owner-managed user access later

Stable IDs drive backend queries. `/darian` and `/home` are MVP convenience entry points only; they call generic character/location query services.
Telegram presentation/session state may remember selected resources later, but authoritative world state remains in runtime/DB.

## Telegram presentation contract

The presentation contract is mandatory for every future Telegram command, callback, notification, menu, browse page, and detail view. It is implementation guidance in `AGENTS.md`, detailed in `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`, and a phase-acceptance rule in `ROADMAP.md`.

Telegram output is a presentation layer only. DB/runtime timestamps remain canonical ISO values for scheduling and persistence; formatting happens only when rendering messages.

Creator-facing timestamp format is:
- `dd-mm-yyyy (Day) hh:mm AM/PM`
- example: `01-05-2025 (Thursday) 07:05 AM`
- 12-hour clock with AM/PM.

Presentation conventions:
- compact Unicode/emoji section headers and restrained dividers for mobile scanability;
- booleans rendered as human terms such as `Yes` / `No` or `ON` / `OFF`;
- actions/status labels rendered in readable title/sentence case;
- internal entity ids such as `room_gym` resolve to display names such as `Home Gym` whenever possible;
- default recent activity hides engine/control noise such as `autonomy_control`, canary bookkeeping, leases and scheduler internals and emphasizes meaningful character/world activity;
- raw canonical events remain stored and may later be exposed through a detailed/debug history mode;
- large profiles, item registries, location contents and histories are sectioned/paginated rather than dumped;
- shared formatter/helper functions should be reused instead of one-off raw strings;
- formatting may change visibility/labels/grouping only; business logic remains in query/control/runtime services.

A Telegram feature is not complete merely because the data is technically correct; normal output must be human-readable, consistent, mobile-scannable, and compliant with the presentation contract.

Relevant implementation:
- `src/observer_sandbox/telegram_bot.py` — message formatting + timestamp presentation;
- `src/observer_sandbox/observer_query.py` — resolves friendly target entity names for observer output.

UI validation/deploy proof:
- CI #156 / run `31639733118`: SUCCESS;
- Deploy #77 / run `31639643492`: SUCCESS.

## Telegram live state and boot UX

P2.1 transport is live. The Creator has confirmed the bot is alive.

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

Every Telegram polling-process boot attempts an Owner-only startup notification:

`🌌 OBSERVER SANDBOX`
`✨ Universe is alive!`
`🟢 Observer link: Online`
`🧠 Minds: Wake-on-demand`
`📡 Creator channel: Connected`

A notification failure must not prevent the bot transport from starting.

Authorization roles:
1. **Owner** — one privileged Telegram user id from `OBSERVER_TELEGRAM_OWNER_ID`; Owner precedence wins even if duplicated in normal allowlist.
2. **Allowed user** — ids from `OBSERVER_TELEGRAM_ALLOWED_USER_IDS`.
3. **Unauthorized user** — no world data/control.

Future user management remains owner-only. Environment-backed Owner ID is the bootstrap/root trust anchor until an explicit later migration changes this design.

## P2 staging

### P2.1 — Mobile Observer MVP (LIVE)
- transport live;
- Creator-facing bot confirmed alive;
- human-friendly message UI live;
- basic observation/control commands available;
- continuous autonomy live and observable through Telegram;
- shared presentation contract established and mandatory for future Telegram work.

### P2.2 — Browse the sandbox (NEXT MAJOR TELEGRAM EXPANSION)
Recommended bounded order from `ROADMAP.md`:
1. **P2.2.1 Observer Home Menu + reusable inline callback/navigation framework**;
2. location list/selection and Home -> rooms navigation;
3. room contents and item detail browsing;
4. generic character list/selection;
5. detailed profile section browsing/pagination.

P2.2 should feel like navigating the universe, not memorizing bot commands.

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
- P1 Living Darian Minimum: CORE + HARDENING + CANARY COMPLETE; CONTINUOUS AUTONOMY LIVE at 1x with wake-on-demand cognition.
- P2 Telegram Observer: ACTIVE / P2.1 LIVE; P2.2 hierarchical universe browsing is next.
- P3 Rich State & Memory: later.
- P4 First simulation module: later.
- P5 Second character: later; observer architecture is already generic/multi-character ready.

## RESUME HERE

1. Continuous autonomy is LIVE at 1x. Do not casually reset or reseed production state.
2. Preserve wake-on-demand cognition: no model calls while a physical action is pending; no periodic LLM heartbeat/reflection loop by default.
3. `/status` exposes cumulative Mind Calls for cost observation.
4. Every Telegram implementation must follow the mandatory presentation contract in `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`; `AGENTS.md` and `ROADMAP.md` reinforce it.
5. Preserve display timestamp format `dd-mm-yyyy (Day) hh:mm AM/PM`; do not mutate canonical DB timestamps just for UI.
6. Keep default activity history universe/character-focused; raw engine/control events stay durable for future detailed/debug views.
7. Telegram boot must continue to notify Owner with `Universe is alive!` while notification failure remains non-fatal.
8. Keep Telegram handlers thin; future rooms/items/full profiles/character selection go through generic query services.
9. Next bounded implementation slice: **P2.2.1 Observer Home Menu + reusable inline callback/navigation framework**, then location -> room -> contents browsing.
10. Synchronize this file after every material change/live proof.
