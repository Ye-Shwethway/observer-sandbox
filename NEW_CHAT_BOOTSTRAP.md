# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Purpose: deterministic project recovery across ChatGPT sessions and protection against memory drift.
Last synchronized: 2026-08-13 — P0 LIVE VERIFIED. P1 continuous autonomy remains LIVE at 1x with wake-on-demand cognition. P1 needs/recovery engine hardening is IMPLEMENTED / CI-VALIDATED / DEPLOYED after a production recovery-loop bug was identified from Telegram history. P2.1 Telegram Observer is live. P2.2.1 Observer Home + inline navigation is IMPLEMENTED / CI-VALIDATED / DEPLOYED. Per-user Telegram notifications are persistent, default ON.

## HARD RECOVERY RULES

Read `AGENTS.md`, then this file, then directly relevant repo files before material changes. For roadmap decisions read `ROADMAP.md`. For Telegram work read `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`; for proactive notifications read `docs/TELEGRAM_NOTIFICATION_POLICY.md`.

After every material repository/runtime change, update this file in the same work session.

Never conflate:
- committed/authored;
- CI-validated;
- deployed to VPS;
- DB/schema applied;
- live-runtime/behavior verified.

Authority order:
1. current Creator instruction;
2. canonical repo config/schema/architecture;
3. verified live VPS/runtime/DB evidence;
4. deployed repo/workflow evidence;
5. current CI/test evidence;
6. this bootstrap;
7. older chat/memory.

## Production topology

Repository: `Ye-Shwethway/observer-sandbox` (private)
VPS: `107.175.30.238`, Ubuntu 24.04
App: `/opt/observer-sandbox`
DB: `/var/lib/observer-sandbox/observer.sqlite3`
Service: `observer-sandbox`
Runtime user: `observer`
Schema version: 3
DB is not publicly exposed.

Previously verified autonomy baseline:
- autonomy_enabled=true;
- mode=normal;
- paused=false;
- speed=1.0;
- retry=null;
- Gemini cognition binding live;
- Telegram Bot API live;
- continuous autonomy started successfully after first production canary.

Production continues autonomously. Re-read live state when an exact current Darian state is required.

## Wake-on-demand cognition

Continuous autonomy does NOT mean continuous LLM polling.

The service ticks the scheduler about every 2 seconds, but the model is called only when:
- autonomy is enabled;
- runtime is not paused;
- retry/backoff is inactive;
- no physical action is currently pending.

While an action is pending, scheduler ticks are deterministic and produce zero additional model calls. At 1x speed, a 10-minute action produces roughly 10 wall minutes without another cognition call.

Persisted telemetry includes cumulative decision calls, last wall/sim call time and wake reason. Telegram `/status` exposes `Mind Calls`.

Do not add periodic LLM heartbeats/background reflection loops without explicit Creator approval.

## P1 Living Darian / engine contract

Canonical fixture: `config/characters/darian.canonical.json`
Runtime defaults: `config/characters/darian.runtime-defaults.json`
Autonomy policy: `config/characters/darian.autonomy-policy.json`
World seed: `config/worlds/home.v1.json`
Core simulation: `src/observer_sandbox/simulation.py`

Home v1: Bedroom, Kitchen, Bathroom, Living Room, Home Gym; 15 useful objects.
Action vocabulary: move, sleep, eat, drink, shower, rest, inspect, use, train, read, idle.

### Recovery bug discovered 2026-08-13

Creator observed repeated Telegram history entries where Darian chose `idle` with reasons such as “rest/recover low energy” but continued looping for hours.

Root cause:
- passive awake energy drift was `-3/hour`;
- `idle` added only `+1/hour`, therefore net `-2 energy/hour`;
- true `rest` was only offered when a local object had the `rest` capability, so Home Gym had no true rest option;
- rest sleep-pressure math also initially had an imbalance after passive drift.

This was an engine/action-contract bug, not primarily an LLM-quality issue.

### Recovery hardening now implemented

- targetless `rest` is a valid action in every room;
- object-backed rest (e.g. Sofa) remains valid;
- `idle` is light recovery and is no longer energy-negative after passive drift;
- `rest` provides meaningful energy recovery and lowers sleepiness after passive drift;
- `sleep` provides stronger recovery and can restore severely depleted energy over a normal overnight duration;
- deterministic baseline policy uses `rest` for low energy rather than forcing premature sleep solely because energy is low.

Current directional rates after passive drift:
- idle: net about `+1 energy/hour`;
- rest: net about `+9 energy/hour` and net lower sleep pressure;
- sleep: net about `+12 energy/hour` with strong sleep-pressure reduction.

Recovery invariants are now canonical in `ROADMAP.md`:
- recovery-labeled actions must improve the relevant need after all passive drift;
- every critical need needs at least one reachable corrective action path;
- cognition must not be forced into an action whose deterministic effect contradicts its reason;
- recovery behavior is tested with before/after state assertions.

Validation evidence:
- engine implementation commit `843a637a26fae373e51ffa42329f6336214fa38c`;
- follow-up sleep-pressure correction commit `ce29b8743c4606e446c9aca3a24fe8c238627c0e`;
- CI #172 / run `31659870325`: SUCCESS;
- latest-main CI #173 / run `31659901086`: SUCCESS;
- Deploy #82 / run `31659870317`: SUCCESS.

Evidence level: recovery engine code is deployed and regression-tested. A post-fix production `rest`/`sleep` completion observed through Telegram will be the live behavioral proof; do not claim that specific behavior proof until observed.

## AI provider layer

Architecture: Provider -> Catalog -> Model Binding -> Runtime Adapter.
Providers include Gemini, NanoGPT, OpenAI, OpenRouter.
Current cognition binding: Gemini / dynamically selected Flash-Lite model for `character:char_darian / cognition`.
Model IDs are not hard-coded into character logic.

## Telegram Observer

Design: `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`
Notification contract: `docs/TELEGRAM_NOTIFICATION_POLICY.md`
Roadmap: `ROADMAP.md`

Long-term goal: **observe the universe**, not merely Darian status.

Future navigation:
- Universe -> Location -> Room -> Contents/Items;
- Characters -> selected character -> state/profile/history/inventory/relationships/physiology;
- AI provider/model browsing and binding changes;
- owner-managed user access.

Telegram handlers remain thin adapters over generic query/control services. Runtime/SQLite remains authoritative.

### Presentation contract

All Telegram commands/callbacks/notifications/menus must remain human-friendly and mobile-scannable.

Visible simulated timestamp format:
`dd-mm-yyyy (Day) hh:mm AM/PM`
Example: `01-05-2025 (Thursday) 07:05 AM`

Normal views:
- use friendly entity names instead of internal IDs;
- use restrained emoji/dividers and clear whitespace;
- use ON/OFF and Yes/No instead of raw booleans;
- hide engine/control bookkeeping from default observer history;
- section/paginate large views;
- preserve raw canonical DB data internally.

## Telegram authorization and notifications

Roles:
- Owner from `OBSERVER_TELEGRAM_OWNER_ID`;
- Allowed users from `OBSERVER_TELEGRAM_ALLOWED_USER_IDS`;
- Unauthorized users receive no world/control data.

Owner wins precedence if duplicated in allowed list.

Notifications are per-user, persistent and default ON.
Canonical commands:
- `/notify on`
- `/notify off`

Supported aliases include `/notification on|off`, `/notifications on|off`, `/notion/on`, `/notion/off`.

The global notification preference gates proactive notifications including `Universe is alive!`; interactive replies are never suppressed by it.

## P2.2 state

P2.2.1 Observer Home + inline navigation: IMPLEMENTED / CI-VALIDATED / DEPLOYED.

`/start` opens Observer Home with buttons:
- Universe
- Characters
- Runtime
- History

Callbacks use stable IDs such as `nav:universe`, `loc:room_gym`, `char:char_darian`, re-check authorization and edit existing messages to reduce clutter.

Next Telegram slice after engine hardening:
**P2.2.2 Location hierarchy / room detail browsing**
- Home/world -> rooms;
- room occupants;
- items/objects;
- exits/relations;
- current room activity;
- Back -> Universe -> Observer Home.

Then item detail browsing, selected-character session state, and profile section browsing/pagination.

## Roadmap snapshot

- P0 Foundation & Remote Control: COMPLETE / LIVE VERIFIED.
- P0.5 Provider Layer: FOUNDATION COMPLETE.
- P1 Living Darian Minimum: CONTINUOUS AUTONOMY LIVE; needs/recovery engine hardening deployed and CI-validated.
- P2 Telegram Observer: ACTIVE; P2.1 live, P2.2.1 complete, P2.2.2 next.
- P3 Rich State & Memory: later.
- P4 First richer simulation module: later.
- P5 Second character: later; observer architecture already generic/multi-character ready.

## RESUME HERE

1. Do not reset/reseed production state casually; continuous autonomy is live at 1x.
2. Preserve wake-on-demand cognition and cost-control policy.
3. Recovery action semantics are now an explicit engine invariant; do not regress idle/rest/sleep directionality.
4. Watch for the next post-fix live recovery completion in Telegram and verify energy/sleepiness move in the expected direction.
5. Resume P2.2.2 location/room browsing after this engine hardening checkpoint.
6. Preserve Telegram presentation and notification contracts.
7. Synchronize this file after every material change/live proof.
