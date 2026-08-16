# World Location Spatial Container Contract v1

Status: PLANNING AUTHORITY — IMPLEMENTATION NOT YET AUTHORIZED

## Purpose

This contract defines what a `location` means in Observer Sandbox.

A location is represented as a graph node for identity, hierarchy and routing, but it is **not conceptually a dimensionless point**. A real simulation location is a bounded or conceptually bounded **spatial container** that may contain smaller places, objects, resources and occupants; expose entrances/exits and other spatial interfaces; carry ownership/access/environment/facility state; and relate to surrounding locations through explicit spatial relations.

This document extends `WORLD_LOCATION_NODE_MODEL.md` and `WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`. It does not replace their stable ID, containment, topology or movement rules.

## Core definition

Canonical semantic definition:

> **Location = an identifiable spatial container with extent, contents, boundary/interface semantics, local state and explicit relationships to surrounding space.**

The graph node is the storage/query identity of that container. `Node` does not mean `point`.

Examples:
- South Lake Tahoe is a regional spatial container.
- Thorne Estate is a property spatial container, canonically about 50 acres.
- Main Mansion is a building spatial container.
- Ground Floor is a nested zone container.
- Living Room is a room container.
- Rear Forested Estate is an outdoor/wilderness-like property container.
- Hidden Dock is a bounded facility/location at the Estate's private lake access.

## Recursive-space invariant

Locations may contain locations recursively:

`region -> property -> building/outdoor zone -> floor/area -> room/sub-area`

Containment describes **spatial membership**, not traversal.

A child location exists inside the spatial extent or conceptual boundary of its parent. A location may have one canonical structural parent in v1.

The hierarchy must remain acyclic.

## Minimum semantic dimensions

A location does not need every optional field populated to exist, but the model must support the following dimensions without changing the meaning of `location` later.

### 1. Identity and classification

Minimum conceptual fields:
- stable technical ID;
- display name;
- `kind` / spatial role;
- functional classification where useful;
- canon/source status where authored geography may be uncertain.

Examples of `kind` include region, property, building, floor, room, outdoor_zone, boundary, path, road, venue, wilderness and service_area.

Classification never grants access or traversal by itself.

### 2. Spatial extent

A location represents an area or volume, even when exact geometry is unknown.

Supported metadata may include:
- known area/size;
- dimensions where meaningful;
- indoor / covered-outdoor / outdoor exposure;
- terrain/surface type;
- optional elevation;
- optional coarse geographic position or bounds;
- optional human-readable orientation/layout metadata.

Exact dimensions, coordinates or polygon geometry are **not required** for v1. Unknown geometry remains unknown rather than fabricated.

Area metadata is descriptive unless a deterministic feature explicitly consumes it.

### 3. Structural contents

A location may contain:
- child locations;
- fixtures;
- non-movable structural objects;
- stored or distributed resources;
- facilities;
- currently present movable objects;
- current occupants/characters;
- ambient population state where later supported.

These are not all represented by the same relation.

Preserve the existing distinction:
- `contains` = authored structural/static containment;
- `located_at` = current dynamic presence;
- future storage/container relation = physical storage inside a movable/static container where required;
- ownership/possession relations remain independent.

Never infer ownership from containment or current location.

### 4. Boundary

Every location has a conceptual boundary separating `inside this location` from `outside this location`, even when the boundary is not a wall.

Examples:
- room walls/doorways;
- building envelope;
- Estate property perimeter;
- edge of an authored forest zone;
- shoreline/lake-access transition;
- conceptual boundary of a public park or regional node.

Boundary geometry may be implicit in v1. The important invariant is that crossing between spatial containers happens through represented topology/interfaces rather than prompt invention.

A boundary may have policy/state associated with it, such as private access, locked state or future operating restrictions.

### 5. Spatial interfaces: entrances, exits and portals

A location may expose one or more spatial interfaces through which traversal occurs.

Examples:
- main entrance;
- rear door;
- garage entrance;
- security gate;
- concealed forest passage;
- dock/water departure point;
- staircase/elevator between floors;
- tunnel endpoint.

Conceptual model:

`Location A -> spatial interface -> Location B`

V1 implementation does not require every doorway to become its own location entity. A spatial interface may initially be represented as metadata attached to a traversable connection or boundary. The ontology must nevertheless preserve the interface concept so later door/gate/lock state can be added without redefining what connectivity means.

Minimum interface semantics when represented:
- source location;
- destination location;
- friendly name/type where useful;
- directionality;
- enabled/disabled state;
- access/boundary state reference where applicable;
- supported traversal mode(s);
- optional traversal cost/duration metadata.

Do not create doorway micro-nodes unless they have independent simulation significance.

### 6. Adjacency versus traversability

Spatial adjacency and legal traversability are distinct concepts.

Two locations may be physically adjacent yet have no traversable interface, for example two rooms separated by a wall with no door.

Therefore:
- adjacency/proximity may be represented later when needed for perception, sound, hazards or geometric reasoning;
- `connected_to` remains the authoritative traversable topology relation;
- containment does not imply adjacency;
- adjacency does not imply `connected_to`;
- `connected_to` does not imply current permission to enter.

V1 does not require a new adjacency relation unless a concrete runtime consumer needs it. The semantic distinction is reserved now to avoid overloading `connected_to` later.

### 7. Ownership, control, residency and jurisdiction

A location may have authoritative control relationships independent from physical occupancy.

Supported concepts include:
- owner;
- resident;
- operator/manager where later useful;
- public/private/institutional/unowned classification;
- authorization/access policy;
- jurisdiction/administrative parent only when a feature requires it.

Existing `owned_by` semantics remain distinct from `contains` and `located_at`.

Presence in a place never grants ownership, residency or authorization automatically.

### 8. Access and operating state

A spatial connection may exist while entry is unavailable.

Location/access semantics must support:
- public;
- owner/resident;
- authorized;
- restricted;
- closed;
- locked;
- temporarily inaccessible/blocked where later required.

Operating state is distinct from access policy. A business can be public but closed; a private Estate gate can be physically open but still restricted.

Option shaping and committed action validation must ultimately use the same deterministic authority.

### 9. Local physical and environmental state

A location is the host for local environmental conditions.

Potential state includes:
- indoor/outdoor exposure;
- daylight/lighting;
- ambient temperature;
- weather exposure;
- precipitation/visibility where relevant;
- noise;
- cleanliness;
- power/water/utilities;
- local hazards or temporary conditions only when separately implemented.

Not all of these are required in the first implementation. The contract establishes that such state belongs to the spatial container or a world/environment layer scoped to it, not to free-form prompt prose.

Nested locations may inherit parent environmental state when an explicit deterministic inheritance rule exists. Do not assume inheritance ad hoc.

### 10. Facilities and affordances

A represented place should be able to explain what activities it physically supports.

Affordances may derive from:
- contained fixtures/equipment;
- venue/service capabilities;
- terrain/environment;
- authored place capabilities;
- available resources.

Examples:
- Home Gym supports strength training because relevant equipment/facilities exist.
- Kitchen supports food preparation because cooking/water/refrigeration facilities exist.
- Tactical Obstacle Course supports obstacle/agility training.
- Hidden Dock may later support water departure/boarding when a water-travel system exists.

Location labels alone should not magically grant executable actions. Where deterministic validation matters, affordances must resolve to machine-readable facilities/resources/capabilities.

### 11. Occupancy and capacity

A location may expose:
- current named occupants;
- ambient presence/crowd state later;
- optional intended or safe capacity where a concrete feature needs it.

Exact capacity is not required for ordinary rooms/areas in v1. Do not fabricate numbers solely for completeness.

Occupancy is dynamic state and must not be encoded as structural containment.

### 12. Temporal state

A location can change over simulation time without changing identity or topology.

Examples:
- venue opens/closes;
- entrance becomes locked/unlocked;
- path becomes temporarily blocked;
- lighting changes;
- occupancy changes;
- facility becomes unavailable.

Stable location identity must survive these state changes.

## Required versus optional data

The ontology distinguishes **semantic capability** from **mandatory populated metadata**.

Minimum representation for an ordinary location should normally provide:
- stable ID;
- display name;
- kind/classification;
- canonical structural parent where applicable;
- exposure classification where relevant;
- authoritative access classification where entry restrictions matter;
- enough topology/interfaces to explain actual legal entrances/exits;
- source/canon status for authored geography where uncertainty matters.

Populate area, dimensions, coordinates, capacity, terrain, utilities, detailed interfaces and other metadata only when known or useful.

Never invent precision merely to satisfy a schema.

## Location completeness levels

To support incremental world authoring without pretending every place is equally detailed, use conceptual completeness levels.

### L0 — Identity placeholder

Known identity only. Not sufficient as an autonomous travel/action destination.

### L1 — Structural container

Has parent/classification and basic containment semantics. May organize the world but lacks enough interfaces/affordances for meaningful runtime use.

### L2 — Traversable place

Has sufficient entrances/exits/topology and access semantics for deterministic movement into/out of the place.

### L3 — Usable place

L2 plus at least one meaningful facility/resource/environment/activity/service affordance.

### L4 — Living place

L3 plus changing operational/environment/resource/population/economic state as later systems apply.

These are planning/query concepts, not necessarily a required stored enum. They prevent an authored label from being mistaken for a fully simulated place.

## Container versus interface versus object

Do not confuse these primitives:

- **location/container**: spatial area/volume within which entities can exist;
- **spatial interface**: crossing point/path/portal between locations;
- **object/fixture**: physical entity contained in a location;
- **route/connection**: traversable relationship that may use an interface;
- **boundary**: separation/control surface around or between spatial containers.

A door is usually an interface/fixture, not a room. A gate is usually an interface/boundary fixture, but may justify a location node when it is a meaningful waiting/security/control area. A road is a location/container when actors can occupy/travel within it, not merely an edge label.

## Example: Thorne Estate

Source-backed conceptual container:

`Thorne Estate [property container, ~50 acres]`
- `Main Mansion [building container]`
- `Garage & Workshop [facility/building-area container as authored]`
- `Tactical Obstacle Course [outdoor activity container]`
- `Private Lake Access [outdoor/water-edge container]`
  - `Hidden Dock [facility/location]`
- `Rear Forested Estate [story-established outdoor container]`
- structural/provisional grounds, approach and connecting zones only as needed for coherent traversal.

Important interfaces/boundaries include:
- ordinary mansion exterior entrance(s);
- Main Security Gate for road-side property transition;
- Concealed Forest Passage for forest-side transition;
- tactical escape tunnel endpoint(s), distinct from ordinary surface access;
- Hidden Dock as future water-side egress interface/facility.

The original mansion source confirms a three-story Estate with reinforced underground level on about 50 acres of private land in the forested outskirts of South Lake Tahoe, plus Private Lake Access, Hidden Dock, Tactical Obstacle Course, Garage & Workshop, Underground Bunker and tactical escape tunnels. It does not support automatic canonization of garden/pool/tennis-court locations.

## Query contract

Generic location queries should eventually be able to expose, as relevant:
- identity/name/kind/classification;
- parent and child locations;
- extent/area metadata where known;
- exposure/terrain where known;
- entrances/exits/interfaces;
- legal connected destinations;
- ownership/residency/access/operating state;
- contained fixtures/resources;
- current occupants;
- facility/affordance summaries;
- local environment state;
- canon/source confidence when appropriate for Creator-facing tools.

Normal cognition must receive only a compact decision-relevant subset, not this full representation.

## Cognition boundary

The LLM may reason about represented place facts but may not author authoritative space.

Cognition may see:
- current location identity and useful local description;
- contained/nearby facilities relevant to the decision;
- legal exits/reachable destinations;
- access/open-state summaries;
- relevant local environment/resources.

It must not infer nonexistent doors, passages, neighboring rooms, public destinations or resources from narrative plausibility.

## Existing Estate refactor requirement

Before broad campus expansion, the already represented Estate locations should be audited/refactored against this contract.

For each existing Estate location:
1. confirm stable identity and structural parent;
2. classify container kind and exposure;
3. preserve/repair contained children/fixtures;
4. document or derive meaningful entrances/exits from topology;
5. confirm ownership/access semantics where relevant;
6. attach only source-supported/provisional extent/layout metadata;
7. confirm facilities/affordances reflect actual contained resources/equipment;
8. preserve current runtime IDs wherever possible;
9. avoid layout invention disguised as migration cleanup.

The refactor should prefer additive fields/relations over identity churn.

## Runtime reconnection requirement

After existing Estate locations are refactored, reconnect and regression-test the gameplay/runtime before adding campus reachability.

Required checks include:
- existing actor `located_at` resolution;
- existing movement options and routing;
- action-target compatibility;
- place-dependent action validation;
- inventory/resource/object location queries;
- physiology/training/runtime consumers that depend on place context;
- cognition compact projection;
- Telegram/generic location browsing;
- history/event location linkage;
- scheduler/pending-action references to location IDs.

Any regression exposed by the richer location semantics should be corrected before campus unlock work begins.

## Estate-first expansion gate

After the existing Estate interior is green under this contract, the next bounded feature is **Estate Campus Reachability**, not South Lake Tahoe.

Campus unlock should add only the elements required for Darian to meaningfully leave the mansion and use the represented private Estate:
- source-confirmed/story-established campus containers;
- minimal provisional connector/grounds containers needed for coherent routes;
- ordinary mansion exterior interface;
- legal Estate-internal walking connections;
- private-property access semantics;
- meaningful campus facilities/affordances;
- cognition-visible legal movement/action options;
- route duration/simulation-time behavior as required by the travel contract;
- Creator/observer visibility of current campus location.

The Main Security Gate may become reachable from inside the Estate, but **no outward South Lake Tahoe edge is authorized in this stage**.

Likewise, the Concealed Forest Passage and Hidden Dock may exist as Estate-side locations/interfaces while their external forest/water continuations remain locked/unrepresented.

## Acceptance sequence

The approved near-term sequence is now:

1. **Location Spatial Container Contract v1** — settle ontology/documentation.
2. **Existing Estate Location Refactor** — bring current represented locations into the richer contract while preserving IDs/behavior where possible.
3. **Gameplay Runtime Regression/Reconnection** — verify and fix all location consumers before expanding reachability.
4. **Estate Campus Reachability Expansion** — add required Estate-side containers/interfaces/affordances/options so Darian can leave the mansion and use the private campus.
5. **Estate Campus Runtime Acceptance** — prove ordinary autonomous mansion <-> campus movement/actions and return while all outside-world edges remain locked.
6. Only after separate Creator prioritization: consider South Lake Tahoe/public-world expansion.

## Explicit pause on outside-world expansion

South Lake Tahoe regional/public expansion is **not the current target**.

Do not during the above sequence:
- connect Main Security Gate to public roads;
- connect Concealed Forest Passage to represented Tahoe backcountry;
- create arbitrary Tahoe destinations;
- implement public venues/economy merely because later roadmap phases mention them;
- enable water travel from Hidden Dock;
- broaden cognition to an unimplemented outside world.

The Estate itself is the next complete simulation boundary.

## Non-goals for v1

Do not require:
- polygon/GIS geometry for every location;
- exact room dimensions;
- every doorway as an entity;
- acoustic/visibility propagation engine;
- collision/physics simulation;
- universal geometric coordinate system;
- dynamic door destruction;
- universal utility/building-management simulation;
- exhaustive environmental fields;
- exhaustive capacity metadata.

This contract should make later depth possible without forcing it into the first refactor.

## Implementation discipline

When implementation begins:
- preserve stable IDs unless a concrete correctness issue requires migration;
- reuse generic entity/relation/field storage before adding schema;
- keep authored data separate from runtime code;
- use source-confirmed/story-established/provisional classifications explicitly;
- prove one genuinely new invariant before batching equivalent Estate locations;
- run focused regression while iterating and one final full CI checkpoint for runtime PRs;
- do not manufacture production movement solely for evidence.

## Completion criterion

This documentation slice is complete when the repository clearly treats locations as nested spatial containers rather than points, preserves the graph/node abstraction as implementation identity, and records the Estate-first refactor/runtime/campus sequence above as the active near-term plan.
