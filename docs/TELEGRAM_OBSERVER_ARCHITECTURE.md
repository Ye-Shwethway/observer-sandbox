# Telegram Observer Architecture

Status: ACTIVE
Scope: Creator-facing mobile observation/control adapter for the persistent universe.

## Product intent

Telegram is not a Darian-status bot and not a Thorne-Estate control panel. It is the first mobile shell for observing and controlling the universe through reusable query/control services.

Darian, `/darian`, Home and the Thorne Estate may remain convenience/exemplar presentation surfaces while production has one rich character/home. Backend contracts must remain entity-id driven so later characters, locations, containers and resources require no duplicate architecture.

## Adapter rule

Telegram is UI/transport only.

`Telegram update -> command/callback router -> reusable query/control service -> canonical runtime/world/profile/inventory/provider backend -> formatted Telegram view`

Handlers must not encode world rules, own stock/macro calculations, mutate SQLite directly, hard-code provider/model ids, or create Telegram-specific copies of canonical entities.

The same service layer must remain reusable by CLI/web/mobile surfaces.

## Generic observer resources

Primary resources include:
- universe/world;
- locations/sublocations;
- characters;
- item definitions + concrete item/stack instances;
- fixed/movable inventory containers;
- runtime state/actions/events;
- profile sections/fields;
- providers/models/bindings;
- typed Creator controls.

Stable ids are callback/query identities. Normal presentation prefers human-readable names.

## Navigation model

World:
`Universe -> Location -> Sublocation -> Contents`

Character:
`Characters -> Character -> State | Profile | History | Inventory | Physiology | Skills | ...`

Inventory:
`Inventory -> Locations | Characters | Containers | All Stocks -> Scope -> Stack`

AI:
`Creator Settings -> AI -> Provider -> Model -> Test -> Save`

Large resources use layered/paginated views rather than giant messages.

## Universal inventory observer invariant

Telegram Inventory is **universe-wide**, never implemented as `Darian's Estate inventory`.

The Creator/authorized observer can browse:
- inventory related to any location;
- inventory related to any character;
- any fixed or movable container;
- all current universe stock stacks.

A scope may legitimately contain zero inventory. New future characters, shops, warehouses, bags/backpacks or regions must work through the same handlers/query service by stable entity id.

Darian's Estate is only the first production content exemplar.

Current entry points:
- `/start -> 🎒 Inventory`;
- `/inventory`;
- Locations / Characters / Containers / All Stocks buttons;
- stack detail with quantity/unit, universal definition, owner, container and container mobility/kind.

Synthetic non-Estate location and non-Darian character + movable backpack tests guard against identity leakage.

## Inventory authorization/control

Read/write authority is separate:
- configured Owner may browse and apply typed inventory replenishment;
- Allowed users may browse but cannot replenish;
- Unauthorized users receive no world inventory data.

Owner stack detail may expose `➕ Replenish Stock`.

Button path:
`Stack -> Replenish -> amount -> explicit confirmation -> typed backend control -> audited result`

Owner direct command:
`/replenish <stack_id> <positive_quantity>`

Telegram never performs the SQL mutation itself. It calls the reusable Creator control service. Server-side role checks are mandatory even if mutation buttons are hidden.

## General character/location observation

The observer layer may expose:
- location list/detail/rooms/contents/exits/recent events;
- item/stack detail;
- character list/selection/current state/profile/history;
- inventory scoped through the universal inventory query contract.

No Telegram session should assume `char_darian` forever. Selected actor/location/session navigation remains a presentation concern; world state remains canonical in runtime storage.

## AI/model control

Creator AI control remains owner-only and preserves these invariants:
- fetch catalogs without mutating the active cognition binding;
- never display credential values;
- stage provider/model candidate server-side;
- require one minimal real inference probe before Save & Activate;
- classify bounded provider failures usefully;
- candidate/test/cancel/navigation never changes binding;
- only explicit successful Save activates the candidate;
- provider/model mutation uses reusable AI services, not Telegram SQL;
- no hard-coded model ids;
- runtime fallback is independent from the Telegram candidate workflow.

Current production primary/fallback remain runtime configuration, not Telegram-owned state.

## Authorization model

Roles:
1. **Owner** — `OBSERVER_TELEGRAM_OWNER_ID`; root Creator authority.
2. **Allowed user** — `OBSERVER_TELEGRAM_ALLOWED_USER_IDS`; authorized observer surface, but not root Creator mutation authority.
3. **Unauthorized** — no world data/control; `/whoami` may reveal only caller identity/bootstrap authorization state.

Bot token, IDs and provider credentials are secrets and are never displayed as values.

Every mutation/control callback rechecks authorization server-side.

## Presentation contract

Telegram is a human-readable mobile observer UI, not a raw runtime log.

- runtime timestamps remain canonical ISO internally; presentation formats them at the edge;
- prefer display names over internal ids in normal views;
- use compact headers/dividers/icons and concise labels;
- use readable Yes/No, ON/OFF/status language;
- default history suppresses control-plane noise unless materially useful;
- paginate profiles, histories, model catalogs and inventory lists;
- callback payloads carry stable ids/bounded selection data, not display identity;
- formatting helpers may transform presentation only, never business semantics.

Canonical simulated-time display:
`dd-mm-yyyy (Day) hh:mm AM/PM`

## Telegram Home lifecycle

`/start` Home is a transient mobile navigation surface with manual Close and bounded auto-delete lifecycle. Message deletion is presentation lifecycle only and never changes universe state.

## Query/control service direction

Reusable id-oriented services may include:
- runtime overview;
- list/get locations and contents;
- list/get characters/profile/history;
- inventory scopes + `inventory_for_entity(entity_id)` + stack detail;
- provider/model/binding queries;
- typed Creator controls such as restore basic stats and replenish an existing inventory stack.

The exact API may evolve; Telegram/backend separation is mandatory.

## Acceptance principles

Telegram observer work passes only when:
- the Creator can independently inspect live universe state on mobile;
- read-only navigation does not mutate simulation state;
- mutation paths are typed, authorized, confirmed where appropriate and audited;
- presentation remains mobile-scannable;
- backend semantics remain reusable beyond current Darian/Estate exemplars.

For Inventory Operations v1 specifically, acceptance requires the same Telegram/query path to represent arbitrary location, character and container inventories without Darian/Estate-specialized backend logic, while Owner-only replenishment uses the reusable Creator control service.
