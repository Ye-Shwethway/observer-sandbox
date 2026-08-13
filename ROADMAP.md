# Observer Sandbox Roadmap

Status: ACTIVE

## Global product principles

- Python/SQLite runtime/world state is authoritative.
- AI proposes structured cognition; it never directly mutates arbitrary world state.
- Telegram is a Creator-facing observer/control adapter, not a simulation engine.
- Cognition remains wake-on-demand; no periodic LLM heartbeat by default.
- Core simulation follows `docs/ARCHITECTURE.md` and the LEGO rule:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- World identity/topology follows `docs/WORLD_LOCATION_NODE_MODEL.md`.
- Physiology/effects follow `docs/PHYSIOLOGY_AND_ITEM_EFFECTS.md`.
- Telegram presentation follows `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`.

## Core composition / schema v4 — PRE-EXPANSION GATE COMPLETE

Canonical audit: `docs/COMPOSABLE_RUNTIME_ARCHITECTURE_AUDIT.md`.

Implemented foundation:
- SQLite schema v4;
- actor-scoped autonomy/pending/lease/retry/cognition in `actor_runtime`;
- universe-global pause/speed/time/world kept separate;
- data-driven `action_definitions`;
- first-class `action_instances` with actor/place/target/participants/resources/conditions/modifiers/time/status/outcome;
- concurrent actions do not double-advance the one universe clock;
- richer event linkage with action/location/state changes/participants/causal socket;
- reusable `entity_definitions` -> concrete `entities` instance path;
- immediate effect operations add/multiply/set/clamp;
- `active_modifiers` persistence socket with timing/source/stack policy;
- generic dynamic `located_at` contract plus distinct ownership/possession semantics;
- service enumerates active actor runtimes instead of assuming Darian-only scheduling;
- action notifications resolve actual actor identity rather than hard-coding Darian.

Deferred intentionally until their feature slices: inventory quantity/depletion/durability, full active-modifier evaluation across domains, rich relationship/memory/environment engines, complex multi-party synchronization/combat.

Acceptance evidence:
- multi-actor/concurrency/definition-instance/modifier/event tests included in CI;
- bounded schema-v4 accelerated production-copy recovery acceptance run #5 succeeded with `needs_acceptable=true` without mutating production;
- production readback showed schema 4, autonomy ON/normal, 1x and a valid actor-scoped pending action.

## World / location graph

Current root: `world_observer_universe`; estate: `loc_thorne_estate`.
Spatial/resource ids are globally scoped and path-independent. `contains` is structural hierarchy, `connected_to` traversal, `located_at` dynamic presence. Future `loc_south_lake_tahoe` can be inserted above the estate; future `loc_quasi_home` can be a sibling. Estate exterior remains locked/non-traversable.

## P0 — Foundation & Remote Control

Status: COMPLETE / LIVE VERIFIED

## P0.5 — AI Provider Layer

Status: FOUNDATION COMPLETE

Dynamic provider/model catalogs and bindings are established; current Darian cognition uses the configured Gemini binding.

## P1 — Living Darian Minimum

Status: CONTINUOUS AUTONOMY LIVE / ENGINE HARDENING PASSED

Includes wake-on-demand scheduler, validated actions, persistent state, five-stat recovery, authored item/resource effects, graph routing, accelerated disposable acceptance and schema-v4 composable runtime foundation.

## P2 — Telegram Observer

Status: ACTIVE

### P2.1 — Mobile Observer MVP

Status: LIVE

Private role-aware bot, status/watch/history/character/home/control commands, polished presentation, persistent default-ON notification preferences and successful action-completion push implementation.

### P2.2 — Browse the Sandbox

Status: IN PROGRESS

1. **P2.2.1 Observer Home + inline navigation — COMPLETE / DEPLOYED**

2. **P2.2.2 Location hierarchy / Thorne Estate**
   - **P2.2.2A Interior node foundation + scoped identity reset — COMPLETE / LIVE VERIFIED**
   - **P2.2.2B Telegram Estate Browser — NEXT**
     - Universe -> Thorne Estate -> floor/zone -> room
     - room detail: occupants, objects, exits, current activity
     - Back follows actual parent-node data
     - locked exterior visible as unavailable, never a movement affordance

3. **P2.2.3 Item browsing — AFTER ESTATE BROWSER**
   - room contents -> item detail
   - capabilities + authored effects
   - definition/instance-aware presentation
   - quantity/durability only after inventory mechanics exist

4. **Character selection**
   - generic list/select flow
   - no Telegram handler assumes Darian forever

5. **Profile section browsing**
   - identity/appearance/body/traits/skills/preferences/physiology/etc.
   - section/paginate large profiles

P2.2 acceptance: Creator can navigate Universe -> location -> sublocation -> room -> contents/item and character/profile surfaces without internal ids or raw dumps.

### P2.3 — Creator Control Expansion

Status: LATER

Owner user management, provider/model browsing/rebinding, richer runtime/history controls and notification categories.

## P3 — Rich State & Memory

Status: LATER

## P4 — First Richer Simulation Module

Status: LATER

## P5 — Second Character

Status: LATER

Quasi becomes the second full autonomous character after P2.2 navigation/selection is proven. The schema/runtime no longer requires a Darian-only scheduler rewrite when that slice arrives.

## Current resume point

**Pre-expansion composable runtime hardening is complete. Resume P2.2.2B Telegram Estate Browser on schema v4.** Do not broaden into South Lake Tahoe yet; first prove recursive estate observation cleanly. Preserve 1x wake-on-demand production autonomy, globally scoped ids, locked unfinished boundaries, actor-scoped scheduler state, Telegram presentation rules and per-user notification preferences.