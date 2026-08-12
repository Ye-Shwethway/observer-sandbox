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

Status: CONTINUOUS AUTONOMY LIVE

- persistent character state and home graph
- validated action contract
- cognition context and policy
- scheduler / lease / crash recovery
- wake-on-demand LLM cognition
- cognition call telemetry
- 1x continuous production autonomy

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

### P2.2 — Browse the Sandbox

Status: NEXT

Goal: move from command-driven status checks to hierarchical Creator observation.

Recommended implementation order:

1. **Observer Home Menu + inline navigation**
   - `/start` becomes a compact dashboard with buttons such as Universe, Characters, Runtime, History.
   - establish reusable callback routing and Back/Home navigation.

2. **Location hierarchy**
   - list locations;
   - select Home;
   - list rooms/sublocations;
   - open a room;
   - show occupants, items/objects, exits/relations and current activity.

3. **Item browsing**
   - room contents -> item list -> item detail;
   - show capabilities and relevant state using human-readable labels.

4. **Character selection**
   - generic character list and selected-character session state;
   - current Darian remains the only initial character, but no Telegram handler assumes that forever.

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
- notification/watch preferences

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

Proceed with **P2.2.1: Observer Home Menu + reusable inline callback/navigation framework**, then use that framework for location -> room -> contents browsing. Preserve continuous 1x wake-on-demand autonomy while building the observer UI.
