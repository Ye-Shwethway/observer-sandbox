# World / Location Node Model

Status: ACTIVE CONTRACT

## Purpose

Locations are graph nodes, not hard-coded screen names. The same model must scale from one mansion to regional/world expansion without identity collisions or UI/backend redesign.

## Identity contract

Entity ids are global technical identities, not display labels. Spatial/resource ids are globally unique, type-prefixed (`world_`, `loc_`, `obj_`), place-scoped where ambiguity exists, and path-independent across ordinary topology changes.

Examples:
- `world_observer_universe`
- `loc_thorne_estate`
- `loc_thorne_estate_kitchen`
- `loc_thorne_estate_home_gym`
- `obj_thorne_estate_kitchen_refrigerator`
- future `loc_south_lake_tahoe`
- future `loc_quasi_home` / `loc_quasi_home_kitchen`

Two nodes may share display name `Kitchen`; their ids may not collide. Prefer `loc_thorne_estate_kitchen` over encoding mutable floor paths into the id.

## Hierarchy

Current:

`world_observer_universe -> loc_thorne_estate -> Floor/Zone -> Room -> Object`

Future regional insertion:

`world_observer_universe -> loc_south_lake_tahoe -> loc_thorne_estate`

Other residences/businesses/wilderness/faction sites can become siblings without renaming existing estate identities.

## Relation semantics

Spatial/ownership relations are deliberately distinct:

- `contains` — structural/static containment or authored hierarchy (world->location, floor->room, room->fixture)
- `connected_to` — legal physical traversal edge
- `located_at` — current dynamic physical presence of a movable entity
- `owned_by` — ownership, independent of current position
- `carried_by` — current possession/carriage
- `equipped_by` — currently equipped state
- future container/storage relation — physical containment inside a movable container.

Never infer ownership from location or overload `contains` to mean every kind of possession.

`src/observer_sandbox/location_runtime.py` is the generic dynamic-location boundary. It resolves `located_at` first, retains character `runtime.location` as a mirrored compatibility/cache path, and may fall back to structural containment for static fixtures. New movable entity systems should use this boundary rather than create their own location convention.

## Node types

- `world` — universe/container root
- `location(kind=estate|region|floor|room|boundary|...)` — recursively nestable spatial node
- `object` — fixture/resource/item instance
- `character` — movable actor with dynamic location.

Containment does not imply traversability.

## Thorne Estate interior

Canonical source establishes a South Lake Tahoe three-story estate with reinforced underground level and major living/training/security/intelligence/garage/library/medical/food-storage/bunker areas.

World seed revision: `thorne-estate-v3.0-scoped-ids`.

Current child zones:
- Ground Floor
- Second Floor
- Third Floor
- Underground Level
- Estate Exterior boundary (locked)

Current room nodes include Grand Foyer, Living Room, Kitchen, Dining Area, Library & Study, Garage & Workshop, Darian's Master Suite, Master Bathroom, Quasi's Room, Guest Rooms, Surveillance & Intelligence Hub, Secure Communications Room, Training Hall, Top-Class Home Gym, Medical Bay, Armory & Storage, Food Supply Storage and Underground Bunker.

The source does not assign every area to an exact floor. Unsourced placements remain `provisional_layout`; do not silently promote them to canon.

## Exterior boundary

`loc_thorne_estate_exterior_boundary` records the known exterior boundary but remains `locked`, has no traversable `connected_to` edge, and must not appear as a legal movement target. Tahoe exterior traversal requires explicit future graph expansion/unlock, never prompt-only permission.

## Scoped identity reset

Prototype ids `home`, `observer_universe`, `zone_*`, `room_*` and generic estate `obj_*` ids are retired. The migration preserved character/profile/physiology/AI/Telegram/history data while remapping Darian's location and clearing stale scheduler plans that referenced obsolete identities.

## Routing contract

Deterministic routing derives from authored `connected_to` relations (currently shortest-path BFS), never a hard-coded room-pair table. Production cognition receives only legal adjacent movement options.

## Observer query contract

Generic location queries expose node identity/name/kind/access, parent, child locations, contained objects/effects, occupants/residents and physical exits. Telegram consumes this query layer rather than mansion-specific topology.

## Future expansion order

1. Thorne Estate interior
2. Telegram recursive estate browser
3. Estate grounds/exterior
4. South Lake Tahoe regional node
5. additional residences such as Quasi's home
6. town/wilderness/faction locations
7. broader universe graph

Shared room names remain safe because technical identity is globally scoped and independent from display labels.