# Telegram Observer Architecture

Status: ACTIVE DESIGN
Scope: P2 Telegram Observer and future Creator-facing universe observation/control surface.

## Product intent

Telegram is not a Darian-status bot. It is the first mobile shell for the Creator's long-term goal: **observe and control the universe through a progressively richer interface**.

P2 starts deliberately small, but its internal contracts must support later expansion without rebuilding the runtime or coupling Telegram handlers directly to SQLite.

## Architectural rule

Telegram is an adapter/UI layer only.

Handlers MUST call reusable application/query/control services. They MUST NOT encode world rules, mutate SQLite directly, duplicate model-binding logic, or invent Telegram-specific representations of core entities.

Target flow:

`Telegram update -> command/callback router -> Observer Query / Runtime Control services -> world/profile/event/provider backends -> formatted Telegram view`

The same service layer must remain usable by future web/mobile/CLI observer surfaces.

## Generic observer resource model

The observer layer should navigate canonical runtime resources by stable ids rather than by hard-coded Darian/Home assumptions.

Primary resource classes:

- Universe / world
- Location
- Sublocation / room
- Item / object
- Character
- Character profile section / field
- Runtime state
- Event / history entry
- Provider
- Model
- Binding
- Control state

Each resource should expose a reusable summary representation and, where appropriate, a detail representation. Telegram should format these resources but not own their semantics.

## Navigation model

The long-term UI should behave like hierarchical browsing rather than a flat command dump.

Conceptual hierarchy:

`Universe -> Location -> Sublocation -> Contents`

Contents may include characters, items/objects, exits/relations, active events, and state summaries.

Character browsing:

`Characters -> selected character -> current state | profile | recent history | relationships | inventory | physiology | skills | preferences | other future sections`

Model control browsing:

`AI -> providers -> provider catalog -> model -> binding target`

The initial single-character/single-home implementation may default to Darian and Home, but service interfaces must accept ids so later character/location selection does not require architectural replacement.

## P2 MVP surface

The first live Telegram slice should stay minimal and immediately useful:

- `/start` or home menu — compact observer entry point.
- `/status` — world runtime + autonomy + current selected/default character summary.
- `/watch` — human-readable "what is happening now" view with current action and recent event context.
- `/history` — recent action/event timeline with bounded pagination.
- `/darian` — Darian summary view; implemented internally through generic character lookup, not a Darian-only backend.
- `/home` — Home summary view; implemented internally through generic location lookup.
- autonomy controls: pause, resume, speed, status. Continuous enable remains separately gated until explicitly approved.

Use Telegram inline buttons where they materially reduce command typing, but callback payloads must carry stable resource/action ids rather than display names.

## Near-term expansion already reserved by the architecture

These do not all belong in the first MVP, but the service/API design must allow them:

### Location observation

- list locations
- select a location
- list sublocations/rooms
- open a room
- show room state, occupants, objects/items, exits/relations, and recent events
- navigate parent/back without hard-coded room names

### Item observation

- list items in a selected location/room or character inventory
- open item details
- show capabilities, static definition, mutable state, ownership/location, and relevant history

### Character observation

- list/select characters
- current location/action/needs/state
- full detailed canonical profile
- profile section browsing instead of dumping an enormous message
- skills, traits, preferences, habits, measurements, physiology and later relationship/memory/inventory views
- recent event history scoped to the selected character

### Multi-character future

No Telegram session should assume `char_darian` forever. Maintain a per-chat/session selected-character id with a project default fallback while the world still has only one character.

When Quasi or later characters exist, the same menus and queries must operate without duplicated handlers.

### AI/model control

- list providers
- refresh provider catalog
- list currently fetched models
- show current binding
- change provider/model binding through existing backend resolution/binding APIs
- never hard-code model ids in Telegram

### Runtime/world controls

Future controls may include pause/resume/speed, bounded canary, continuous autonomy activation after explicit policy approval, and other safe runtime controls. Telegram must invoke the same control service used by CLI/Actions rather than reimplementing scheduler state mutation.

## Query-service boundary

P2 should introduce a reusable observer/query facade, tentatively `ObserverService` or equivalent, with id-oriented methods such as:

- `runtime_overview()`
- `list_locations()`
- `get_location(location_id)`
- `list_sublocations(location_id)`
- `list_location_contents(location_id)`
- `list_items(location_id=None, character_id=None)`
- `get_item(item_id)`
- `list_characters()`
- `get_character_summary(character_id)`
- `get_character_profile(character_id, section=None)`
- `recent_events(actor_id=None, location_id=None, limit=...)`
- `autonomy_status(character_id)`
- provider/model/binding list and mutation methods delegated to the existing AI backend

The exact Python API can evolve, but the separation is mandatory.

## Telegram session state

Persist only UI/navigation preferences that are genuinely Telegram-specific, such as:

- authorized Telegram user/chat id
- currently selected character id
- currently selected location/sublocation id
- pagination cursor/page

Do not copy world state into Telegram session storage. World state remains authoritative in the runtime DB.

## Security / authorization

The bot is a private Creator control surface, not a public chatbot.

Authorization has three explicit roles:

1. **Owner** — one privileged Telegram identity configured separately as `OBSERVER_TELEGRAM_OWNER_ID`. The owner is always authorized and does not need to be duplicated in the normal allowlist.
2. **Allowed user** — identities listed in `OBSERVER_TELEGRAM_ALLOWED_USER_IDS`. They may use the currently exposed observer/control surface but are not the root authority for future user-management changes.
3. **Unauthorized user** — receives no world data or control access; `/start` and `/whoami` may reveal only the caller's own Telegram id and authorization state for bootstrap.

The bot token, owner id, and allowed-user ids are secrets/config and are never committed or logged as values.

Future user-management commands should be owner-only. The intended direction is owner-controlled list/add/remove/role management backed by a persistent authorization store; the initial environment-backed allowlist remains the bootstrap source until that layer is implemented. No allowed user may remove/demote the owner or grant owner authority through ordinary commands.

Control callbacks and future user-management callbacks must re-check authorization server-side; hidden buttons alone are not authorization.

## Message design

Prefer concise layered views over giant raw dumps.

Examples:

- summary message -> inline buttons for Details / Profile / Location / History
- profile overview -> section buttons -> paginated fields
- location -> Rooms / Characters / Items / Events

Telegram message limits must never force the data model to become shallow. Large profiles are paginated/sectioned at the presentation layer.

## P2 implementation stages

### P2.1 — Mobile Observer MVP

- bot process/service foundation
- private authorization with separate owner and allowed-user roles
- generic observer/query service foundation
- `/start`, `/status`, `/watch`, `/history`
- generic character summary surfaced initially as `/darian`
- generic location summary surfaced initially as `/home`
- pause/resume/speed/status controls
- live VPS deployment and readback

### P2.2 — Browse the sandbox

- location list/selection
- room/sublocation navigation
- room contents
- item list/detail
- character list/selection
- profile section browsing

### P2.3 — Creator control expansion

- owner-only user management
- provider/model catalog browsing and refresh
- binding selection/change
- richer runtime controls
- scoped event/history filters
- future notification/watch preferences

Later phases may add relationships, inventory, physiology dashboards, memory views, world events, additional locations and multiple characters without replacing this architecture.

## Non-goals for P2 MVP

- full graphical universe UI
- duplicating the entire canonical profile in one Telegram message
- Telegram-owned simulation rules
- hard-coded provider/model ids
- Darian/Home-specific backend contracts
- public multi-user bot access

## Acceptance principle

P2 MVP passes when the Creator can independently open Telegram and inspect the live sandbox and basic runtime state without relying on ChatGPT narration, while the codebase remains ready for hierarchical universe browsing, multiple characters/resources, and owner-managed users later.
