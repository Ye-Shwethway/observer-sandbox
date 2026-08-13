# Observer Sandbox — New Chat Bootstrap

Status: ACTIVE
Purpose: deterministic project recovery across ChatGPT sessions and protection against memory drift.
Last synchronized: 2026-08-13 — P0 LIVE VERIFIED. P1 continuous autonomy remains LIVE at 1x with wake-on-demand cognition. P1 full basic-physiology recovery + generic item-effect hardening is IMPLEMENTED / CI-VALIDATED / DEPLOYED. P2.1 Telegram Observer is live. P2.2.1 Observer Home + inline navigation is IMPLEMENTED / CI-VALIDATED / DEPLOYED. Per-user Telegram notifications are persistent, default ON.

## HARD RECOVERY RULES

Read `AGENTS.md`, then this file, then directly relevant repo files before material changes. For roadmap decisions read `ROADMAP.md`. For Telegram work read `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`; for proactive notifications read `docs/TELEGRAM_NOTIFICATION_POLICY.md`; for living-needs, recovery, world-resource or item-effect work read `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`.

After every material repository/runtime change, update this file in the same work session.

Never conflate:
- committed/authored;
- CI-validated;
- deployed to VPS;
- DB/schema/seed applied;
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

## P1 Living Darian / physiology and item-effect contract

Canonical fixture: `config/characters/darian.canonical.json`
Runtime defaults: `config/characters/darian.runtime-defaults.json`
Autonomy policy: `config/characters/darian.autonomy-policy.json`
World seed: `config/worlds/home.v1.json`
Core simulation: `src/observer_sandbox/simulation.py`
Canonical physiology/effect design: `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`

Home v1: Bedroom, Kitchen, Bathroom, Living Room, Home Gym; 15 useful objects.
Action vocabulary: move, sleep, eat, drink, shower, rest, inspect, use, train, read, idle.

### Recovery-loop bug discovered 2026-08-13

Creator observed repeated Telegram history where Darian selected `idle` with reasons such as rest/recover low energy but remained depleted.

Original root causes:
- passive energy drain exceeded idle recovery, making idle net energy-negative;
- true rest was only available through local rest-capable objects;
- recovery rate interactions were not tested directionally.

The fix established targetless rest, corrected idle/rest/sleep directionality, and then expanded into a complete five-stat physiology + item-effect contract.

### Current five-stat baseline

All values clamp to `0..100`.
- energy: high is good;
- hunger: high is bad;
- thirst: high is bad;
- sleepiness: high is bad;
- cleanliness: high is good.

Passive per simulated hour:
- energy `-2.0`;
- hunger `+2.5`;
- thirst `+3.0`;
- sleepiness `+3.0`;
- cleanliness `-0.8`.

Intrinsic action effects per hour are defined separately from target/item effects:
- sleep: energy `+11`, sleepiness `-15`, hunger `+0.5`, thirst `+0.75` before passive combination;
- rest: energy `+10`, sleepiness `-4` before passive combination;
- idle: energy `+3` before passive combination;
- train: energy `-10`, hunger `+4`, thirst `+6`, cleanliness `-6` before passive combination;
- read: energy `-0.5` before passive combination.

Directional net examples:
- 1h idle: about `+1 energy`;
- 1h targetless rest: about `+8 energy` and `-1 sleepiness`;
- 8h sleep from severe depletion provides strong energy/sleep-pressure recovery while still increasing hunger/thirst by a bounded amount.

### Generic world/item effects

Home world revision is `home-v1.1-effects`.

World objects may author action-specific `effects`; runtime seeding persists them as `game.effects`. `action_options()` includes matching effect metadata so cognition can see deterministic consequences. `apply_action()` applies those effects after passive/intrinsic action effects.

Current authored recovery resources:
- Drinking Water / drink: thirst `-55`;
- Sink / drink: thirst `-35`;
- Meal Ingredients / eat: hunger `-50`, energy `+8`, thirst `+2`;
- Pantry / eat: hunger `-40`, energy `+5`, thirst `+1`;
- Shower / shower: cleanliness set to `100`;
- Rest and Bed/Sleep provide intrinsic energy/sleep-pressure recovery.

Food/drink/shower actions without matching authored effects are rejected. Refrigerator and Dining Table no longer expose fake eat/drink behavior solely because they are near food.

Future items such as an energy drink use this same effect profile instead of requiring hard-coded simulation branches. Finite consumables, quantities, temporary stimulant modifiers, cooldowns/tolerance and inventory depletion remain later work; do not model a finite item as infinitely reusable until that layer exists.

### Persistent-action migration rule

Pending autonomy actions persist across service restarts. World/capability/effect changes must account for pending plans.

During the first item-effect rollout, production had a persisted `eat -> Pantry` plan created under the prior world definition. Removing Pantry's eat capability would have made the pending action fail only because of deployment. Pantry was therefore preserved as a renewable ready-food abstraction with an authored eat effect, and Deploy #86 successfully applied that compatibility definition.

### Validation and live evidence

Regression suite now checks:
- rest/idle/sleep recovery direction;
- strong overnight recovery;
- water thirst restoration;
- food hunger + secondary effects;
- shower cleanliness restoration;
- effect metadata in legal action options;
- rejection of restorative target actions without authored effects;
- bounded-day state remains within `0..100`.

Evidence:
- full physiology/item-effect engine commit `8d44e04a236d89860326d22e5a8039159851df95`;
- full recovery/effect test commit `9aa2246e187f9f809b717b081076dea1095e98b8`;
- CI #178: SUCCESS;
- Pantry compatibility CI #180: SUCCESS;
- engine Deploy #85: SUCCESS;
- Pantry compatibility Deploy #86: SUCCESS.

Live readback from Deploy #85 after the Creator-reported depleted snapshot showed:
- Kitchen;
- sim time `2025-05-01T12:40:00+00:00`;
- energy `23.832`;
- hunger `63.665`;
- thirst `28.335` (already recovered from the previously reported ~72.1);
- sleepiness `34.835`;
- cleanliness `43.2`;
- pending `eat -> Pantry`, duration 20m, reason: hunger recovery;
- decision_calls `15`;
- autonomy enabled, normal, unpaused, 1x.

The exact live state continues to advance. Do not treat the above as current forever. The next completed Pantry meal/rest/shower actions provide live behavioral proof for the newly generic item-effect/restoration path.

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

Next Telegram slice after this P1 engine checkpoint:
**P2.2.2 Location hierarchy / room detail browsing**
- Home/world -> rooms;
- room occupants;
- items/objects;
- exits/relations;
- current room activity;
- Back -> Universe -> Observer Home.

Item-detail views should eventually show authored capabilities/effects using the same human-friendly presentation contract.

## Roadmap snapshot

- P0 Foundation & Remote Control: COMPLETE / LIVE VERIFIED.
- P0.5 Provider Layer: FOUNDATION COMPLETE.
- P1 Living Darian Minimum: CONTINUOUS AUTONOMY LIVE; full five-stat physiology restoration + generic item-effect hardening deployed and CI-validated.
- P2 Telegram Observer: ACTIVE; P2.1 live, P2.2.1 complete, P2.2.2 next.
- P3 Rich State & Memory: later.
- P4 First richer simulation module: later.
- P5 Second character: later; observer architecture already generic/multi-character ready.

## RESUME HERE

1. Do not reset/reseed production state casually; continuous autonomy is live at 1x.
2. Preserve wake-on-demand cognition and cost-control policy.
3. Preserve the five-stat recovery + generic `game.effects` contract in `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`.
4. Watch the next post-deploy live recovery completions (Pantry meal, rest, shower) and confirm stats move as authored; use exact live evidence before claiming behavioral proof.
5. Future Energy Drink or other consumables should use effect profiles, but do not add infinite consumable semantics before quantity/inventory/temporary-modifier rules exist.
6. Resume P2.2.2 location/room browsing after this engine hardening checkpoint.
7. Preserve Telegram presentation and notification contracts.
8. Synchronize this file after every material change/live proof.
