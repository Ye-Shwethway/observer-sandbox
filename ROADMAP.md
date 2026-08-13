# Observer Sandbox Roadmap

Status: ACTIVE

This roadmap tracks the smallest useful vertical slices for the Observer Sandbox. Keep the project intentionally modular; deepen each phase only when it improves the Creator's ability to observe or operate the universe.

## Global product principles

- Runtime/world state remains authoritative in the Python/SQLite core.
- AI models propose structured cognition; they do not directly mutate world state.
- Telegram is a Creator-facing observer/control adapter, not a second simulation engine.
- Continuous cognition remains wake-on-demand: no periodic LLM heartbeat or background reflection loop by default.
- New features should prefer generic ids/query services over Darian/Home-specific backend contracts.
- World/location topology follows `docs/WORLD_LOCATION_NODE_MODEL.md`; locations are recursively nestable graph nodes.
- Telegram presentation quality is part of acceptance, not optional polish. All Telegram work must follow `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`.
- Basic living physiology and item effects follow `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`.

## Simulation recovery correctness

Needs/recovery behavior is an engine contract, not prompt flavor text.

- An action described as recovery must move its primary recovery state in the correct direction after all passive time drift is included.
- Every basic physiological stat must have at least one valid reachable restoration path.
- `rest` must increase energy and reduce sleep pressure; `sleep` must provide stronger energy/sleep-pressure recovery than ordinary rest; `idle` may provide only light recovery but must not paradoxically drain energy when cognition is using it as a pause.
- Hunger must be recoverable through authored food targets; thirst through authored drink targets; cleanliness through authored wash/shower targets.
- Target/item effects are authored in the world definition, persisted as `game.effects`, surfaced through legal `action_options()`, and deterministically applied by the engine.
- Food/drink/shower actions without matching authored physiological effects must be rejected rather than silently pretending to restore a need.
- Recovery math is regression-tested as before/after state, not only by checking that an action validates.
- Persistent pending actions must be considered during world/effect migrations; do not invalidate a live pending action without an explicit safe migration/revalidation path.

## World / location graph contract

- `observer_universe` is the generic world root.
- `home` is the stable **Thorne Estate location node**, not a world root.
- Current structure is `Observer Universe -> Thorne Estate -> Floor/Zone -> Room -> Object`.
- A later South Lake Tahoe regional node may be inserted above Thorne Estate without changing the estate id.
- Future locations such as Quasi's home become sibling nodes under the appropriate regional node.
- Containment and traversal remain separate: `contains` describes hierarchy, `connected_to` describes legal movement.
- The unimplemented estate exterior exists as a locked boundary node with no traversable edge.
- Stable P1 room ids are retained where practical to preserve runtime state/history/pending actions.
- Canonical mansion structure and provisional floor placement must remain explicitly distinguishable.

## Telegram presentation acceptance rule

Every new Telegram command, callback, notification, menu, browse page, or detail view must preserve the established presentation contract:

- visible simulated timestamps: `dd-mm-yyyy (Day) hh:mm AM/PM` in 12-hour format;
- internal timestamps remain canonical ISO-8601;
- use human-readable names instead of internal ids in normal views;
- use concise sections, whitespace, restrained icons, and consistent labels for mobile scanability;
- prefer friendly ON/OFF and Yes/No status text over raw booleans;
- suppress engine/control bookkeeping from default observer history;
- paginate/section large data rather than dumping it;
- keep formatting in shared presentation helpers and backend semantics in query/control services.

A Telegram slice is not complete if its data is technically correct but presented as a raw log/database dump.

## Notification policy

Telegram proactive notifications are **default ON per authorized user**. Preferences are persisted independently per user and survive bot/service restarts.

Canonical commands:
- `/notify on`
- `/notify off`

Compatibility aliases include `/notification on|off`, `/notifications on|off`, `/notion/on`, `/notion/off`.

The shared preference gates boot and successful action-completion push notifications. Completed character actions should push a concise human-friendly summary; planning/in-progress/bookkeeping ticks should not.

## P0 — Foundation & Remote Control

Status: COMPLETE / LIVE VERIFIED

- repository/runtime foundation
- persistent SQLite
- VPS deployment and systemd service
- GitHub Actions remote deployment/readback

## P0.5 — AI Provider Layer

Status: FOUNDATION COMPLETE

- provider registry and live model catalogs
- dynamic bindings
- Gemini live cognition
- no hard-coded character model ids

## P1 — Living Darian Minimum

Status: CONTINUOUS AUTONOMY LIVE / ENGINE HARDENING CHECKPOINT PASSED

- persistent character state and world graph
- validated action contract
- cognition context and recovery-aware policy
- scheduler / lease / crash recovery
- wake-on-demand LLM cognition and call telemetry
- 1x continuous production autonomy
- all five current basic physiology stats have restoration paths
- generic world-object `game.effects` contract
- bounded accelerated production-copy recovery acceptance lane

## P2 — Telegram Observer

Status: ACTIVE

### P2.1 — Mobile Observer MVP

Status: LIVE

- private bot transport
- Owner / Allowed User authorization split
- `/status`, `/watch`, `/history`, `/darian`, `/home`
- pause/resume/speed controls
- `Universe is alive!` boot notification
- human-friendly presentation contract
- persistent per-user notification preference, default ON
- successful action-completion proactive push implementation deployed; live receipt confirmation tracked separately

### P2.2 — Browse the Sandbox

Status: IN PROGRESS

Goal: move from command-driven status checks to hierarchical Creator observation.

1. **Observer Home Menu + inline navigation — IMPLEMENTED / DEPLOYED**
   - `/start` opens a compact Observer Home dashboard.
   - inline buttons: Universe, Characters, Runtime, History.
   - callback routing uses stable ids/action keys.
   - reusable Back/Home navigation established.

2. **Location hierarchy / Thorne Estate — IN PROGRESS**

   **P2.2.2A — Interior node foundation — IMPLEMENTED IN REPO; validation/deploy evidence tracked separately**
   - flat five-room Home seed replaced by recursive location-node graph;
   - `observer_universe -> home(Thorne Estate) -> floors/zones -> rooms`;
   - stable P1 room ids retained for existing core rooms;
   - canonical mansion areas represented, with non-source floor assignments marked provisional;
   - exterior boundary exists but is locked and non-traversable;
   - generic query layer exposes parent, child locations, objects, occupants, residents, exits, access/kind metadata;
   - topology seeding safely rebuilds seed-owned containment/adjacency without resetting character runtime state.

   **P2.2.2B — Telegram estate browser — NEXT**
   - Universe -> Thorne Estate -> floor/zone -> room;
   - room detail shows occupants, objects, exits and current activity;
   - Back follows actual parent node rather than hard-coded Home assumptions;
   - locked exterior is visible as unavailable, never as a legal movement affordance.

3. **Item browsing — AFTER P2.2.2B**
   - room contents -> item list -> item detail;
   - show capabilities plus authored effects using human-readable labels;
   - later expose quantity/temporary modifiers only after those systems exist.

4. **Character selection**
   - generic character list exists;
   - add selected-character session state so future views follow the selected character;
   - no Telegram handler may assume `char_darian` forever.

5. **Profile section browsing**
   - character -> Profile -> section menu;
   - identity/appearance/body/traits/skills/preferences/physiology and later additional sections;
   - paginate large sections.

P2.2 acceptance: the Creator can navigate from Universe to a location/estate, descend through sublocations to a room, inspect contents, open an item, select a character, and browse profile sections without typing internal ids or receiving raw dumps.

### P2.3 — Creator Control Expansion

Status: LATER

- owner-only user management
- provider/model catalog browsing and refresh
- live model binding changes
- richer runtime controls
- scoped history/event filters
- notification/watch-category preferences

## P3 — Rich State & Memory

Status: LATER

Add richer durable state and memory only after the Creator-facing observer surface is mature enough to inspect it.

## P4 — First Simulation Module

Status: LATER

Introduce the first richer autonomous simulation module without expanding into EIDOLON-scale orchestration.

## P5 — Second Character

Status: LATER

Add Quasi after generic character selection/profile/navigation is already proven through P2.2.

## Current resume point

Finish validation/deployment of **P2.2.2A Thorne Estate interior node foundation**, then implement **P2.2.2B Telegram estate browser** on the generic recursive location-query contract. Preserve continuous 1x wake-on-demand cognition, stable ids, the locked exterior boundary, Telegram presentation rules, and the shared per-user notification gate.
