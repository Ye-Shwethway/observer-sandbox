# World Foundation Expansion Plan v1

Status: PLANNING AUTHORITY — DOCUMENTATION FIRST

## Purpose

Observer Sandbox has reached a point where character-side minimum foundations are substantially ahead of the represented world. Character autonomy can reason and act inside the current Estate interior, but the simulation cannot safely expand into the Estate campus or South Lake Tahoe until the world substrate can represent places, traversal, access, environmental state, resources, services, population presence, and basic world processes without relying on prompt-only invention.

This plan establishes the next development phase: **World Foundation Expansion**.

The phase is intentionally documentation-first. No implementation slice is authorized merely by inclusion here. The goal is to settle the dependency order, contracts, boundaries, and minimum-runnable milestones before sustained coding begins, so later implementation can proceed in consecutive bounded slices with less architectural drift.

## Governing architecture

Preserve the existing composable runtime contract:

`Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`

Preserve the current world/location contract in `docs/WORLD_LOCATION_NODE_MODEL.md`:
- locations are recursively nestable graph nodes;
- `contains` expresses structural containment;
- `connected_to` expresses legal traversable topology;
- `located_at` expresses dynamic physical presence;
- `owned_by`, carriage, and equipment stay distinct from structural location;
- locked or unimplemented boundaries have no traversable edge;
- routing is derived from authored relations rather than hard-coded room pairs.

The LLM may propose intentions and structured actions. It must not invent authoritative world topology, opening state, route legality, ownership, prices, inventory, weather, or other mutable world facts. Those belong to deterministic/runtime state.

## Core diagnosis

The immediate blocker is not lack of character cognition depth. It is lack of usable world substrate.

Today, the Estate exterior boundary exists canonically but is locked and has no legal traversal edge. This is correct behavior: the engine refuses movement into an unrepresented world instead of allowing prompt-only travel.

The next phase therefore expands the world in the same evidence-preserving manner already used for the Estate interior.

## Design principle: representation before simulation depth

World work is split into two classes.

### A. Representation foundations

These make the world structurally representable and traversable:
- spatial hierarchy and topology;
- place classification;
- access and ownership;
- route/travel representation;
- place state and facilities;
- object/resource location;
- environmental context.

### B. Living-world processes

These make the represented world change and operate over time:
- venue schedules;
- resource depletion and replenishment;
- ambient population/presence;
- service availability;
- economic transactions;
- weather evolution;
- transportation operations;
- recurring local/world events.

Representation foundations must precede broad living-world processes. Do not build economy, traffic, weather depth, or large NPC populations on top of an incomplete spatial/access model.

## Target world hierarchy

The current recursive model remains authoritative and is expanded rather than replaced.

Illustrative hierarchy:

`world_observer_universe`
`└─ loc_south_lake_tahoe`
`   ├─ loc_thorne_estate`
`   │  ├─ mansion/interior nodes`
`   │  ├─ estate grounds / campus zones`
`   │  ├─ driveway`
`   │  └─ security gate / boundary`
`   ├─ roads / public connectors`
`   ├─ public venues / services`
`   ├─ residences`
`   ├─ outdoor / wilderness locations`
`   └─ later civic / institutional nodes`

Hierarchy expresses containment, not movement. Traversal remains explicit through `connected_to` relations or a future compatible route relation built on the same graph contract.

## Program milestones

### WF-1 — World Spatial Hierarchy & Topology v1

Goal: make the world graph capable of representing Estate-campus and regional expansion without changing identity rules or hard-coding travel.

Minimum scope:
- confirm/extend location kinds required for outdoor zones, roads, boundaries, properties, and public places;
- preserve globally scoped stable IDs;
- preserve recursive parent/child containment;
- preserve explicit traversability independent from containment;
- support authored distance/travel-cost metadata where needed without turning coordinates into a mandatory global simulation;
- expose only legal adjacent/reachable movement targets to cognition.

First exemplar: Thorne Estate interior -> Estate campus boundary path.

Not yet:
- full GIS coordinates;
- street-by-street Tahoe reproduction;
- pathfinding over unbounded map data;
- vehicle simulation;
- traffic.

### WF-2 — Property, Place Classification & Access v1

Goal: prevent a graph of places from becoming a world where every actor can enter every node.

Minimum scope:
- place categories such as private property, public place, residence, business/service, outdoor/wilderness, road/connector;
- ownership/residency distinct from physical location;
- access modes such as public, resident/owner, invited/authorized, restricted, locked/closed;
- opening/access state read deterministically by movement/action validation;
- no inference that being near a place grants entry.

First exemplar: Thorne Estate private property and security gate.

Not yet:
- legal system;
- trespass/crime simulation;
- keys/cards taxonomy;
- universal permission scripting language.

### WF-3 — Local Travel & Route Runtime v1

Goal: represent movement beyond one adjacent room as a deterministic world process.

Minimum scope:
- origin, destination, route/connection sequence, travel mode, and represented duration;
- walking/property traversal as first travel mode;
- route legality derived from topology and access;
- bounded route cost/duration;
- movement remains an action/runtime process, not teleportation;
- route completion updates authoritative `located_at` / mirrored actor location through existing location runtime boundaries.

First exemplar: Mansion -> Estate grounds -> Estate gate.

Not yet:
- automobiles;
- fuel;
- traffic;
- public transit;
- route optimization beyond the bounded represented graph.

### WF-4 — Thorne Estate Campus Expansion v1

Goal: make the known property usable outside the mansion before opening the public world.

Candidate authored campus nodes:
- front grounds;
- rear grounds;
- garden;
- pool area;
- tennis court;
- driveway;
- garage exterior / vehicle access zone;
- security gate;
- perimeter/path zones where source support exists.

Rules:
- only source-supported or explicitly Creator-approved geography becomes canonical;
- unsourced exact placement remains provisional rather than silently promoted;
- campus nodes must have meaningful traversal/access/facility semantics rather than being decorative labels.

Exit criterion: Darian can autonomously and deterministically move from an interior room to multiple Estate-campus locations and return, without unlocking South Lake Tahoe yet.

### WF-5 — South Lake Tahoe Regional Anchor v1

Goal: insert the regional node already anticipated by the canonical world model and create the first legal world boundary beyond the Estate.

Minimum scope:
- `loc_south_lake_tahoe` as regional parent for the Estate and future local locations;
- one or more bounded road/public connector nodes immediately outside the Estate;
- explicit Estate gate -> public-world edge;
- regional identity without requiring exhaustive city content;
- only represented destinations become cognition-visible.

Exit criterion: the Estate is no longer a sealed world island, but the region still exposes only authored reachable places.

### WF-6 — Environment / Daylight / Weather Foundation v1

Goal: make outdoor world state consequential rather than cosmetic.

Minimum scope:
- local simulation date/time;
- daylight/daypart derived from time;
- ambient temperature;
- one bounded weather-state representation;
- precipitation/visibility only if represented by the chosen weather state;
- indoor/outdoor exposure distinction;
- compact cognition projection of only locally relevant environmental state;
- deterministic effect hooks may influence action desirability or legality without granting the LLM mutation authority.

Not yet:
- meteorological forecasting engine;
- climate model;
- detailed storm physics;
- broad injury/hazard engine.

### WF-7 — Venue & Service Foundation v1

Goal: make outside destinations useful rather than empty map nodes.

Minimum venue contract:
- category;
- location;
- access/opening state;
- operating hours where applicable;
- represented services/capabilities;
- represented resources/facilities.

Candidate venue categories:
- grocery/store;
- restaurant/cafe;
- clinic/hospital/pharmacy;
- fuel/service station;
- park/trail;
- hotel;
- general public/service building.

Use one or a small bounded set of Tahoe exemplars first. Do not author an exhaustive city directory.

### WF-8 — World Resource Distribution v1

Goal: allow resources to exist, be consumed, and create reasons for travel.

Minimum scope:
- object/resource authoritative location;
- ownership independent from location;
- quantity/availability where meaningful;
- portable vs fixture distinction;
- depletion from deterministic actions;
- bounded replenishment producer or authored restock where justified;
- existing inventory/effect contracts reused rather than duplicated.

Target loop:
`need/resource shortage -> choose destination -> travel -> obtain/use resource -> authoritative quantity/inventory/state change`.

### WF-9 — Ambient Population / Presence v1

Goal: prevent represented public places from feeling physically empty without requiring a full cognition agent for every person.

Two population tiers:
1. persistent named characters/agents with ordinary character runtime;
2. lightweight ambient presence representing staff, patrons, pedestrians, crowd level, or occupancy without individual LLM cognition.

Minimum scope:
- place-level presence/occupancy state;
- role/category summaries where useful;
- deterministic availability for service interactions where a named character is not required;
- no fake named histories for ambient entities.

Not yet:
- thousands of autonomous LLM NPCs;
- city-scale demographic simulation;
- universal social-network graph.

### WF-10 — Basic World Economy v1

Goal: complete the first practical outside-world resource loop.

Minimum scope:
- money/account balance authority;
- prices for represented goods/services;
- purchase/payment transaction;
- deterministic inventory/resource transfer;
- auditable transaction event/state change;
- one bounded income or replenishment source only when needed to keep the loop runnable.

Not yet:
- macroeconomics;
- dynamic market simulation;
- banking depth;
- taxes;
- employment/labor-market simulation;
- property market.

## Expected unlock progression

The program should expand observable world capability incrementally:

- after WF-1 to WF-3: legal multi-node Estate traversal becomes structurally reliable;
- after WF-4: the Estate campus becomes a usable simulated environment;
- after WF-5: the Estate can open into a bounded South Lake Tahoe world;
- after WF-6 and WF-7: outdoor/public destinations gain environmental and service meaning;
- after WF-8 to WF-10: outside trips can arise from resource needs and produce persistent world consequences.

This ordering is intentional. It avoids creating a large catalog of places that actors cannot meaningfully traverse or use.

## Cognition context rule

World expansion must not scale model context linearly with world size.

The model should receive only a compact, relevance-bounded world slice such as:
- current location and parent context;
- legal adjacent/reachable destinations needed for the current decision;
- local access/opening/environment state;
- task-relevant resources/services;
- active travel context if already in transit.

Do not inject the full South Lake Tahoe graph, full venue catalog, full resource registry, or all ambient population state into each cognition call.

World complexity belongs primarily in deterministic storage/query/runtime layers. Cognition receives a decision-relevant projection.

## Data and source discipline

- Real-world geography may be represented selectively; completeness is not required.
- Do not invent canonical real-world details when they matter to topology, access, or service behavior.
- Creator-authored fictional/private locations remain valid world content and must be clearly distinguished from externally sourced public-world facts where relevant.
- Exact coordinates are optional unless a later feature truly requires them.
- Technical identity remains stable even if display names/layout metadata later improve.

## Implementation cadence after planning closure

When coding begins:
- keep each milestone minimum-runnable and reversible;
- use one exemplar only for a genuinely new invariant;
- batch structurally equivalent follow-ons after the invariant is proven;
- reuse existing generic entity/relation/location/action/resource contracts before adding schema;
- avoid bespoke mansion-only runtime paths;
- code/runtime PRs receive focused tests and one final full CI checkpoint;
- runtime-affecting merges use the standard deploy and read-only production verification path.

## Planning phase boundaries

During the current documentation-first phase:
- no world runtime mutation is authorized solely by this document;
- no production world unlock is authorized;
- no Estate exterior edge should be created yet;
- no synthetic production travel is required;
- no weather/economy/vehicle/population implementation should jump ahead of the settled dependency order;
- additional planning documents may refine individual milestones before implementation begins.

## Next documentation work

Before starting sustained implementation, continue discussion and documentation for the highest-leverage milestones, especially:
1. spatial hierarchy/topology metadata and route semantics;
2. property/access model;
3. local travel lifecycle;
4. Estate campus canonical geography;
5. South Lake Tahoe regional expansion/source policy;
6. environment/world-state contract;
7. venue/service and resource loops.

The aim is not to predict every later feature. The aim is to make the next implementation sequence sufficiently explicit that consecutive coding can proceed with minimal architectural reinterpretation.
