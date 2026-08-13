# World / Location Node Model

Status: ACTIVE CONTRACT

## Purpose

Observer Sandbox locations are graph nodes, not hard-coded screen names. The same location model must scale from a single interior to a regional universe without identity collisions or changes to Telegram/backend contracts.

## Identity contract

Entity ids are **global technical identities**, not display labels.

Spatial/resource ids must be:

- globally unique within the universe database;
- type-prefixed (`world_`, `loc_`, `obj_`);
- scoped by the stable owning/place identity where ambiguity can exist;
- human-debuggable but never exposed as normal UI labels;
- stable across ordinary containment/topology changes.

Examples:

- world root: `world_observer_universe`
- estate: `loc_thorne_estate`
- estate kitchen: `loc_thorne_estate_kitchen`
- estate gym: `loc_thorne_estate_home_gym`
- kitchen refrigerator: `obj_thorne_estate_kitchen_refrigerator`
- future regional node: `loc_south_lake_tahoe`
- future second residence: `loc_quasi_home`
- future second-residence kitchen: `loc_quasi_home_kitchen`

Two nodes may share the same display name, such as `Kitchen`, while their ids remain distinct.

### Path independence

Do **not** encode the full mutable parent path in a room/object identity merely to make it unique. For example prefer:

`loc_thorne_estate_kitchen`

over:
`loc_thorne_estate_ground_floor_kitchen`

Containment belongs in `contains` relations. If a room is later reclassified or moved to another floor, its stable identity should not need to change solely because its parent changed.

Objects use the same principle: scope them enough to avoid collision, but keep parent/topology facts in relations rather than treating a full path as identity.

Character ids such as `char_darian` are already globally person-specific and do not need residence scoping.

## Hierarchy

The current root is:

`world_observer_universe -> loc_thorne_estate -> Floor/Zone -> Room -> Object`

A later regional expansion may insert:

`world_observer_universe -> loc_south_lake_tahoe -> loc_thorne_estate`

and add sibling locations such as Quasi's home, businesses, wilderness areas, faction sites, or other residences without renaming existing estate/room identities.

## Node types

- `world` — top-level universe container.
- `location(kind=estate|region|floor|room|boundary|...)` — recursively nestable spatial node.
- `object` — contained usable/inspectable resource or item-like fixture.
- `character` — may have a runtime location that points to a traversable room node.

Containment uses `contains` relations. Physical movement uses `connected_to` relations. Hierarchical containment does **not** automatically imply traversability.

## Thorne Estate interior foundation

Canonical mansion source establishes a three-story estate with a reinforced underground level in South Lake Tahoe, with living quarters, training facilities, gym, intelligence/surveillance, armory/storage, garage/workshop, library/study, medical room, food supply storage, bunker/security infrastructure, and related features.

World seed revision: `thorne-estate-v3.0-scoped-ids`.

Current hierarchy begins with:

- `loc_thorne_estate` — Thorne Estate
  - `loc_thorne_estate_ground_floor` — Ground Floor
  - `loc_thorne_estate_second_floor` — Second Floor
  - `loc_thorne_estate_third_floor` — Third Floor
  - `loc_thorne_estate_underground` — Underground Level
  - `loc_thorne_estate_exterior_boundary` — Estate Exterior boundary (locked)

Current room nodes include Grand Foyer, Living Room, Kitchen, Dining Area, Library & Study, Garage & Workshop, Darian's Master Suite, Master Bathroom, Quasi's Room, Guest Rooms, Surveillance & Intelligence Hub, Secure Communications Room, Training Hall, Top-Class Home Gym, Medical Bay, Armory & Storage, Food Supply Storage, and Underground Bunker.

The source establishes the estate's three stories, underground level, and major areas, but does not assign every named area to an exact floor. Therefore floor placements not directly established by source are marked `provisional_layout`. Do not silently promote provisional placement to canon.

## Exterior boundary

The canonical estate has extensive private grounds and outdoor/escape features, but the outer environment is not implemented yet.

`loc_thorne_estate_exterior_boundary` exists so the graph records that an exterior boundary exists, but:

- access is `locked`;
- it has no `connected_to` relation;
- it must not appear in legal movement action options;
- cognition cannot leave the mansion through prompt choice alone.

When the Tahoe exterior is implemented, unlock traversal through explicit graph migration rather than prompt-only permission.

## Clean identity reset / migration rule

The early prototype ids `home`, `observer_universe`, `zone_*`, `room_*`, and generic `obj_*` ids are obsolete and must not be reused for new world state.

The scoped-id migration deliberately performs a clean spatial reset while preserving non-spatial durable state:

- character/profile data, physiology values, AI bindings, Telegram preferences and event history remain;
- Darian's old runtime location is mapped to the equivalent scoped node;
- stale pending/lease/retry scheduler state is cleared because it may contain obsolete ids;
- runtime is paused transactionally before legacy spatial deletion and restored after the new service has initialized;
- legacy spatial entities are removed rather than retained as aliases that could create two identities for the same place.

This project is still early enough that clean identity architecture takes precedence over preserving prototype spatial ids.

## Routing contract

Do not maintain hard-coded room-pair routing tables. Deterministic baseline/dry-run routing must derive routes from authored `connected_to` relations (currently shortest-path BFS). Production cognition still receives only legal adjacent movement options through `action_options()`.

## Observer query contract

Generic location queries should expose:

- current node identity/name/kind/access metadata;
- parent node;
- child location nodes;
- contained objects and authored effects;
- occupants/residents;
- physical exits (`connected_to`).

Telegram must consume this generic query layer rather than encode mansion-specific hierarchy itself.

## Future expansion

Expected evolution:

1. Thorne Estate interior (current)
2. Telegram recursive estate browsing
3. Estate grounds / exterior features
4. South Lake Tahoe regional node
5. additional residences such as Quasi's home
6. town/wilderness/faction locations
7. broader universe graph

Each expansion adds/reparents nodes and relations. Shared names such as Bedroom, Kitchen or Bathroom are safe because identity is place-scoped and display names are independent of ids.
