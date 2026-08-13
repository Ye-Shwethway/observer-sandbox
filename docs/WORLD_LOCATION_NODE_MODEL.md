# World / Location Node Model

Status: ACTIVE CONTRACT

## Purpose

Observer Sandbox locations are graph nodes, not hard-coded screen names. The same location model must scale from a single interior to a regional universe without changing entity identity or Telegram/backend contracts.

## Hierarchy

The current root is:

`Observer Universe -> Thorne Estate -> Floor/Zone -> Room -> Object`

`Thorne Estate` uses the stable entity id `home`, but it is a **location node**, not the world root. This is intentional. A later regional expansion can insert a South Lake Tahoe node above the estate:

`Observer Universe -> South Lake Tahoe -> Thorne Estate`

Additional sibling locations such as Quasi's home, town locations, wilderness areas, businesses, or faction sites can then be added under the same regional node without changing the estate id.

## Node types

- `world` — top-level universe container.
- `location(kind=estate|region|floor|room|boundary|...)` — recursively nestable spatial node.
- `object` — contained usable/inspectable resource or item-like fixture.
- `character` — may have a runtime location that points to a traversable room node.

Containment uses `contains` relations. Physical movement uses `connected_to` relations. Hierarchical containment does **not** automatically imply traversability.

## Thorne Estate interior foundation

Canonical mansion source establishes a three-story estate with a reinforced underground level in South Lake Tahoe, with living quarters, training facilities, gym, intelligence/surveillance, armory/storage, garage/workshop, library/study, medical room, food supply storage, bunker/security infrastructure, and related features.

The current seed models:

- Thorne Estate
  - Ground Floor
  - Second Floor
  - Third Floor
  - Underground Level
  - Estate Exterior boundary (locked)

Current room nodes include:

- Grand Foyer
- Living Room
- Kitchen
- Dining Area
- Library & Study
- Garage & Workshop
- Darian's Master Suite
- Master Bathroom
- Quasi's Room
- Guest Rooms
- Surveillance & Intelligence Hub
- Secure Communications Room
- Training Hall
- Top-Class Home Gym
- Medical Bay
- Armory & Storage
- Food Supply Storage
- Underground Bunker

The source establishes the estate's three stories, underground level, and major areas, but does not assign every named area to an exact floor. Therefore floor placements not directly established by source are marked `provisional_layout`. Do not silently promote provisional placement to canon.

## Exterior boundary

The canonical estate has extensive private grounds and outdoor/escape features, but the outer environment is not implemented yet.

`boundary_exterior` exists so the world model knows an exterior boundary exists, but:

- access is `locked`;
- it has no `connected_to` relation;
- it must not appear in legal movement action options;
- cognition cannot leave the mansion through prompt choice alone.

When the Tahoe exterior is implemented, unlock traversal through explicit graph migration rather than prompt-only permission.

## Stable-id migration rule

Existing P1 ids remain stable where possible:

- `home` -> Thorne Estate location node
- `room_bedroom` -> Darian's Master Suite
- `room_bathroom` -> Master Bathroom
- `room_living` -> Living Room
- `room_kitchen` -> Kitchen
- `room_gym` -> Top-Class Home Gym

This preserves runtime locations, pending actions, history, notifications, and existing observer links.

Seed-owned containment and adjacency relations may be rebuilt during initialization, but entity ids and persisted character/runtime state must not be casually reset.

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
2. Estate grounds / exterior features
3. South Lake Tahoe regional node
4. additional residences such as Quasi's home
5. town/wilderness/faction locations
6. broader universe graph

Each expansion adds/reparents nodes and relations; it should not require redesigning the location abstraction.
