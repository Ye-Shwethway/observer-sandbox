# Observer Sandbox Roadmap

Status: ACTIVE

This roadmap tracks the smallest useful vertical slices for the Observer Sandbox. Keep the project intentionally modular; deepen each phase only when it improves the Creator's ability to observe or operate the universe.

## Global product principles

- Runtime/world state remains authoritative in the Python/SQLite core.
- AI models propose structured cognition; they do not directly mutate world state.
- Telegram is a Creator-facing observer/control adapter, not a second simulation engine.
- Continuous cognition remains wake-on-demand: no periodic LLM heartbeat or background reflection loop by default.
- New features should prefer generic ids/query services over Darian/Home-specific backend contracts.
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
- The action options given to the LLM must not force a semantic contradiction where the reason says “recover/rest/eat/drink/clean up” but the deterministic action effect worsens or fails to restore the relevant need.
- Recovery math is regression-tested as before/after state, not only by checking that an action validates.
- Persistent pending actions must be considered during world/effect migrations; do not invalidate a live pending action without an explicit safe migration/revalidation path.
- Future physiology expansion must preserve these directional invariants before adding more detailed rates, temporary modifiers, consumable quantities, tolerance, or inventory depletion.

Current P1 physiology baseline:
- passive per hour: energy `-2.0`, hunger `+2.5`, thirst `+3.0`, sleepiness `+3.0`, cleanliness `-0.8`;
- one hour targetless rest is net about `+8 energy` and `-1 sleepiness`;
- one hour idle is net about `+1 energy`;
- authored Home recovery resources currently include Drinking Water, Sink water, Meal Ingredients, Pantry food source, Shower, Bed and Rest.

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

Compatibility aliases currently supported:
- `/notification on|off`
- `/notifications on|off`
- `/notion/on`
- `/notion/off`

The same preference gate should be reused by future proactive universe notifications rather than creating one-off notification toggles. Boot notification `Universe is alive!` obeys the Owner's notification preference.

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

Status: CONTINUOUS AUTONOMY LIVE / ENGINE HARDENING ACTIVE

- persistent character state and home graph
- validated action contract
- cognition context and policy
- scheduler / lease / crash recovery
- wake-on-demand LLM cognition
- cognition call telemetry
- 1x continuous production autonomy
- all five current basic physiology stats have authored restoration paths
- targetless `rest` recovery available in every room, while object-backed rest remains supported
- generic world-object `game.effects` contract for food/drink/shower and future item effects
- legal action options expose item effects to cognition
- restorative target actions require matching authored effects
- migration-safety rule for persisted pending actions

## P2 — Telegram Observer

Status: ACTIVE

### P2.1 — Mobile Observer MVP

Status: LIVE

- private bot transport
- Owner / Allowed User authorization split
- `/status`, `/watch`, `/history`, `/darian`, `/home`
- pause/resume/speed controls
- owner boot notification: `Universe is alive!`
- human-friendly Telegram presentation contract established and live
- persistent per-user notification preference, default ON

### P2.2 — Browse the Sandbox

Status: IN PROGRESS

Goal: move from command-driven status checks to hierarchical Creator observation.

1. **Observer Home Menu + inline navigation — IMPLEMENTED**
   - `/start` opens a compact Observer Home dashboard.
   - inline buttons: Universe, Characters, Runtime, History.
   - callback routing uses stable ids/action keys rather than display labels.
   - callback navigation edits the existing Telegram message to reduce chat clutter.
   - reusable Back/Home navigation is established.
   - notification status is visible from Observer Home.

2. **Location hierarchy — NEXT AFTER CURRENT ENGINE HARDENING**
   - list rooms/sublocations from the canonical world graph;
   - open a room;
   - show occupants, items/objects, exits/relations and current activity;
   - preserve Back -> Universe -> Observer Home navigation.

3. **Item browsing**
   - room contents -> item list -> item detail;
   - show capabilities plus authored effects using human-readable labels;
   - later expose quantity/temporary modifiers only after those systems exist.

4. **Character selection**
   - generic character list is already exposed by the callback framework;
   - next add selected-character session state so future views follow the selected character;
   - no Telegram handler may assume `char_darian` forever.

5. **Profile section browsing**
   - character -> Profile -> section menu;
   - identity/appearance/body/traits/skills/preferences/physiology and later additional sections;
   - paginate large sections.

P2.2 acceptance: the Creator can navigate from Universe/Home to a room, inspect its contents, open an item, select a character, and browse profile sections without typing internal ids or receiving raw dumps.

### P2.3 — Creator Control Expansion

Status: LATER

- owner-only user management
- provider/model catalog browsing and refresh
- live model binding changes
- richer runtime controls
- scoped history/event filters
- notification/watch-category preferences building on the global per-user notification gate

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

Verify the new **P1 full basic-physiology + item-effect recovery system** against live production recovery from the currently depleted state, then resume **P2.2.2: Location hierarchy and room detail browsing**. Preserve continuous 1x wake-on-demand cognition, Telegram presentation rules, and the shared per-user notification preference gate.
