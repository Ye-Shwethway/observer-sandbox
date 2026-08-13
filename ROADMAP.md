# Observer Sandbox Roadmap

Status: ACTIVE

This roadmap tracks the smallest useful vertical slices for the Observer Sandbox. Keep the project intentionally modular; deepen each phase only when it improves the Creator's ability to observe or operate the universe.

## Global product principles

- Runtime/world state remains authoritative in the Python/SQLite core.
- AI models propose structured cognition; they do not directly mutate world state.
- Telegram is a Creator-facing observer/control adapter, not a second simulation engine.
- Continuous cognition remains wake-on-demand: no periodic LLM heartbeat or background reflection loop by default.
- New features should prefer generic ids/query services over Darian/Home-specific backend contracts.
- World/location topology and globally scoped identity follow `docs/WORLD_LOCATION_NODE_MODEL.md`.
- Composable runtime design follows the LEGO-like expression `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> validated transition -> State Changes + Events` and the pre-expansion audit in `docs/COMPOSABLE_RUNTIME_ARCHITECTURE_AUDIT.md`.
- Telegram presentation quality is part of acceptance, not optional polish. All Telegram work must follow `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`.
- Basic living physiology and item effects follow `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`.

## Simulation recovery correctness

Needs/recovery behavior is an engine contract, not prompt flavor text.

- An action described as recovery must move its primary recovery state in the correct direction after all passive time drift is included.
- Every basic physiological stat must have at least one valid reachable restoration path.
- `rest` must increase energy and reduce sleep pressure; `sleep` must provide stronger recovery; `idle` must not paradoxically drain energy when used as a pause.
- Hunger, thirst and cleanliness require authored restorative targets/effects.
- Target/item effects are authored in world definitions, persisted as `game.effects`, surfaced through legal `action_options()`, and deterministically applied by the engine.
- Recovery math is regression-tested as before/after state.
- Persistent pending actions must be considered during world/effect migrations.

## World / location graph and identity contract

- canonical root: `world_observer_universe`;
- Thorne Estate: `loc_thorne_estate`;
- current structure: `world_observer_universe -> loc_thorne_estate -> floor/zone -> room -> object`;
- all spatial/resource ids are globally unique, type-prefixed, place-scoped and path-independent;
- display names may repeat across places; ids may not collide;
- containment/topology belongs in relations rather than mutable full paths embedded in ids;
- future `loc_south_lake_tahoe` may be inserted above `loc_thorne_estate` without renaming the estate/interior nodes;
- future residences such as `loc_quasi_home` can be siblings and may safely contain their own Kitchen/Bedroom/etc.;
- `contains` describes hierarchy; `connected_to` describes legal movement;
- the unimplemented estate exterior is a locked boundary with no traversable edge;
- deterministic baseline routing derives from the authored graph rather than a hard-coded five-room route table;
- prototype ids `home`, `observer_universe`, `zone_*`, `room_*` and generic estate `obj_*` ids are retired.

The physical SQLite table schema remains version 3 because the existing entity/relation model already supports these identities and recursive graph relationships; the clean break is a world identity/data migration rather than a table-shape migration.

## Proposed pre-expansion composable runtime hardening gate

Status: **AUDITED / PROPOSED — IMPLEMENTATION REQUIRES CREATOR APPROVAL**

The one-time architecture audit found several Darian-only prototype assumptions that should be removed before broad world expansion or a second autonomous character. Canonical audit: `docs/COMPOSABLE_RUNTIME_ARCHITECTURE_AUDIT.md`.

Recommended bounded sequence:

1. actor-scoped autonomy/runtime state so multiple characters can hold independent pending actions, leases/retries and cognition telemetry;
2. first-class action instance envelope with stable action id, actor/participants, target/resources, place, planned start/end time, conditions/modifiers and status;
3. data-driven action-definition registry instead of allowing the Python action switch/constant layer to grow indefinitely;
4. first-class condition/modifier/effect contract supporting additive/set/multiplicative and future temporary/source/stack semantics;
5. queryable event envelope with location, participants, action/causal references and structured state-change summaries;
6. definition/template vs concrete instance vs runtime-state distinction, plus explicit ownership/possession/dynamic-location semantics before inventory expands;
7. fresh-DB, legacy-development migration and accelerated autonomy acceptance after the hardening cutover.

This is a small generic foundation pass, not a large EIDOLON/Simiverse-style rewrite. Full inventory, relationships, memory, environment/weather and complex group synchronization remain deferred to their feature slices.

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

Telegram proactive notifications are **default ON per authorized user**. Preferences persist independently per user and survive service restarts.

Canonical commands: `/notify on`, `/notify off`. Compatibility aliases include `/notification on|off`, `/notifications on|off`, `/notion/on`, `/notion/off`.

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
- graph-derived deterministic routing after scoped identity reset

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
- successful action-completion proactive push implementation deployed

### P2.2 — Browse the Sandbox

Status: IN PROGRESS

Goal: move from command-driven status checks to hierarchical Creator observation.

1. **Observer Home Menu + inline navigation — IMPLEMENTED / DEPLOYED**
   - `/start` opens a compact Observer Home dashboard.
   - inline buttons: Universe, Characters, Runtime, History.
   - callback routing uses stable ids/action keys.
   - reusable Back/Home navigation established.

2. **Location hierarchy / Thorne Estate**

   **P2.2.2A — Interior node foundation + clean spatial identity reset — COMPLETE / LIVE VERIFIED**
   - flat prototype Home model replaced by recursive mansion location graph;
   - scoped identity revision `thorne-estate-v3.0-scoped-ids`;
   - canonical root `world_observer_universe`, estate `loc_thorne_estate`;
   - rooms/objects use place-scoped ids such as `loc_thorne_estate_kitchen` and `obj_thorne_estate_kitchen_refrigerator`;
   - legacy spatial ids removed through a transactional migration;
   - Darian's current location is remapped while profile/physiology/AI/Telegram preferences remain durable;
   - stale pending/lease/retry state is safely cleared during the identity cutover;
   - exterior boundary remains locked/non-traversable;
   - query layer exposes parent, children, objects, occupants, residents, exits and metadata;
   - deterministic baseline routing now derives from `connected_to` graph relations.

   **P2.2.2B — Telegram Estate Browser — READY AFTER ARCHITECTURE-GATE DECISION**
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

Add Quasi after generic character selection/profile/navigation is already proven through P2.2 and after singleton-character runtime assumptions are removed.

## Current resume point

The clean spatial identity reset is complete and live. A one-time composable-runtime audit is now complete and proposes a bounded pre-expansion hardening gate. **Creator decision is next:** either approve that hardening pass before P2.2.2B, or deliberately defer it and continue Telegram Estate Browser first. Do not begin broader South Lake Tahoe/world expansion or a second autonomous character while singleton runtime assumptions remain. Preserve continuous 1x wake-on-demand cognition, scoped ids, the locked exterior boundary, Telegram presentation rules, and the shared per-user notification gate.
