# Thorne Estate Campus Canon Map v1

Status: PLANNING AUTHORITY — GEOGRAPHY/CANON MAP — IMPLEMENTATION NOT YET AUTHORIZED

## Purpose

This document defines the first canonical/provisional campus map for the Thorne Estate before WF-4 implementation. It reconciles:

1. the original Darian's Mansion / Thorne Estate source supplied by the Creator;
2. Creator-established storyline continuity that the rear side of the Estate adjoins a forested Tahoe backcountry corridor and includes a concealed passage into the forest;
3. real Lake Tahoe Basin geography only as plausibility/context support, not as proof of the fictional Estate's exact parcel;
4. the existing Observer Sandbox graph/location contracts.

The goal is to make Estate-campus implementation low-drift while preserving uncertainty honestly.

## Source confidence classes

Every campus fact belongs to one of four classes.

### `source_confirmed`
Directly supported by the original mansion source.

### `story_established`
Explicitly established by prior Creator-approved storyline continuity, even where the original mansion source does not spell out the detail.

### `structurally_inferred`
Needed to make already-established geography physically traversable, but exact placement/name is not directly sourced. These nodes remain `provisional_layout` until explicitly approved as canon.

### `planned_unapproved`
Discussed candidate content that is neither source-confirmed nor story-established. It must not silently enter the canonical Estate seed.

## Source-confirmed Estate facts

The original mansion source establishes:
- South Lake Tahoe, California;
- a secluded forested-outskirts setting;
- approximately 50 acres of private land;
- an approximately 15,000 sq. ft. three-story estate with reinforced underground level;
- Garage & Workshop;
- Private Lake Access;
- Hidden Dock for covert departures/escape routes;
- private water purification system;
- Tactical Obstacle Course with wall climbs, barbed-wire crawl zones and sprinting tracks;
- Underground Bunker;
- tactical escape tunnels leading to safe exit points;
- advanced surveillance/defensive infrastructure and biometric access restrictions.

These are canonical content anchors. Exact exterior placement is not supplied by the source and must not be invented as canonical geometry.

## Creator-established rear-forest continuity

The Creator has reaffirmed prior storyline continuity that:
- the rear/western side of the Estate adjoins a forested South Lake Tahoe/backcountry corridor;
- the Estate includes a low-visibility passage allowing movement from private Estate forest into the adjoining forest;
- this arrangement fits Elias Thorne's intent for the Estate to function as a hidden stronghold.

This is `story_established` canon for Observer Sandbox planning.

The simulation should not claim that the fictional parcel specifically borders a named National Forest parcel, trail, or federal cadastral boundary unless separately authored and sourced later.

## Real-world plausibility boundary

Official Lake Tahoe sources establish a large National Forest/backcountry context around the basin and real trail/backcountry access near South Lake Tahoe. Tahoe also contains wildland-urban-interface areas where neighborhoods meet forested/open-space land.

This supports the plausibility of a fictional secluded estate adjoining a forest corridor.

It does **not** establish the Estate's exact real parcel, west/east orientation, legal boundary, lakefront parcel geometry, road, or connection to any named public trail.

## Campus topology principles

The Estate is modeled as a private property graph, not a decorative map.

A node exists when it has at least one of:
- traversal significance;
- access/boundary significance;
- facility/resource significance;
- activity significance;
- environmental significance.

Containment does not imply traversability. Traversal uses explicit legal graph edges.

## Canonical campus nodes

### Estate root

`loc_thorne_estate`
- class: `source_confirmed`
- kind: `estate/private_property`
- canonical scale: approximately 50 acres
- structural parent after WF-5: `loc_south_lake_tahoe`

### Main Mansion

Existing mansion/interior subtree.
- class: `source_confirmed`
- remains the current inhabited core.

### Garage & Workshop

Existing represented facility inside/attached to the Estate complex.
- class: `source_confirmed`
- later campus graph should expose a meaningful exterior/vehicle approach without changing the canonical garage identity.

### Tactical Obstacle Course

Proposed technical id: `loc_thorne_estate_tactical_obstacle_course`
- class: `source_confirmed`
- outdoor/training area
- supports agility/endurance/tactical physical training
- should be reachable through ordinary Estate-ground traversal.

### Private Lake Access

Proposed technical id: `loc_thorne_estate_private_lake_access`
- class: `source_confirmed`
- waterfront/access zone
- includes water-access significance and water-purification infrastructure context.

The source establishes private lake access but does not establish the exact shoreline shape or its orientation relative to the mansion.

### Hidden Dock

Proposed technical id: `loc_thorne_estate_hidden_dock`
- class: `source_confirmed`
- child/adjacent functional node of Private Lake Access
- covert departure/escape significance
- water-route runtime remains later work; the dock may exist as a campus node before water travel is implemented.

### Underground Bunker

Existing/established underground node.
- class: `source_confirmed`
- retained as part of the underground Estate topology.

### Tactical Escape Route Endpoint(s)

The source confirms escape tunnels leading to safe exit points, but not exact endpoint count or location.

Planning representation:
- class: `source_confirmed` for the existence of tunnel exit capability;
- exact endpoint node placement: `structurally_inferred` until separately approved.

Do not force every escape tunnel endpoint into WF-4 if ordinary campus traversal can be completed without it.

## Story-established forest nodes

### Rear Forested Estate Zone

Proposed id: `loc_thorne_estate_rear_forest`
- class: `story_established`
- private wooded zone inside the Estate boundary
- represents transition from managed/core Estate space into dense private forest.

This is the primary Estate-side anchor for backcountry access.

### Concealed Forest Passage

Proposed id: `loc_thorne_estate_concealed_forest_passage`
- class: `story_established`
- boundary/access node
- purpose: low-visibility pedestrian/backcountry egress associated with the stronghold design
- distinct from the ordinary main gate
- distinct from underground tactical escape tunnels.

Before WF-5/backcountry expansion, this passage may exist on the Estate side while its outward forest edge remains locked/unrepresented.

### Tahoe Backcountry Forest Connector

Proposed id: `loc_south_lake_tahoe_backcountry_connector_01`
- class: `planned` until WF-5 regional authoring
- represents bounded adjoining forest/backcountry, not a named real trail by default.

The Estate-side passage must not expose this as a legal movement target until an outside-world node is actually represented.

## Structurally inferred campus nodes

The following are required to make a 50-acre private estate traversable but are not directly named in the original source.

### Mansion Exterior / Primary Entrance

Proposed id: `loc_thorne_estate_mansion_exterior`
- class: `structurally_inferred`
- bridges interior exits to campus traversal.

### Core Estate Grounds

Proposed id: `loc_thorne_estate_core_grounds`
- class: `structurally_inferred`
- coarse shared outdoor connector around the principal buildings/facilities.

Do not split into many lawns/yards unless distinct runtime meaning later requires it.

### Drive / Main Approach

Proposed id: `loc_thorne_estate_main_approach`
- class: `structurally_inferred`
- connects mansion/garage side to ordinary property entrance.

The exact shape, length and road name remain provisional.

### Main Security Gate

Proposed id: `loc_thorne_estate_main_gate`
- class: `structurally_inferred` from the private stronghold/security/vehicle-access context
- ordinary formal property boundary
- access-controlled
- distinct from concealed forest passage.

Before WF-5, actors may reach the Estate side of the gate but no public-road edge exists.

### Internal Estate Paths

Use only the minimum connector edges/nodes needed for meaningful traversal among:
- mansion exterior;
- garage approach;
- obstacle course;
- lake access;
- rear forest;
- main approach/gate.

Prefer graph edges over creating a named path node for every short connection.

## Planned/unapproved locations

The following have appeared in earlier discussion/memory but are **not supported by the supplied mansion source** and are not required by the current Creator reaffirmation:
- garden;
- swimming pool;
- tennis court.

They remain `planned_unapproved` for this project until the Creator explicitly adopts them into Observer Sandbox canon or supplies a source establishing them.

They must not be seeded merely because they appeared in older project memories.

## Recommended coarse adjacency graph

This graph intentionally describes logical connectivity, not precise architecture.

`Main Mansion Interior`
`  <-> Mansion Exterior / Primary Entrance`
`       <-> Core Estate Grounds`
`            <-> Garage / Workshop approach`
`            <-> Tactical Obstacle Course`
`            <-> Private Lake Access <-> Hidden Dock`
`            <-> Rear Forested Estate Zone <-> Concealed Forest Passage [OUTSIDE LOCKED]`
`            <-> Main Approach <-> Main Security Gate [PUBLIC OUTSIDE LOCKED]`

This establishes three conceptually distinct future mobility directions:

1. **Road / ordinary access**
   - mansion -> grounds -> main approach -> main security gate -> future public-road connector.

2. **Forest / backcountry access**
   - mansion -> grounds -> rear forest -> concealed forest passage -> future Tahoe backcountry connector.

3. **Water / covert access**
   - mansion -> grounds -> private lake access -> hidden dock -> future water-route runtime.

The three directions are world-topology concepts, not authorization to implement road, backcountry or water travel in the planning phase.

## Main Gate vs Concealed Forest Passage vs Escape Tunnel

These must remain distinct.

### Main Security Gate
- ordinary formal Estate entrance/exit;
- vehicle/visitor/property access role;
- future road-world transition.

### Concealed Forest Passage
- low-visibility Estate-boundary passage;
- pedestrian/backcountry role;
- story-established stronghold feature;
- future forest-world transition.

### Tactical Escape Tunnel
- underground emergency/covert escape infrastructure;
- source-confirmed existence;
- endpoint placement remains separately authored;
- may terminate within Estate forest, near another safe exit, or elsewhere only when specifically approved.

Do not merge these into one generic `exit` node.

## WF-4 Estate Campus implementation target

WF-4 should initially make only the private Estate campus runnable.

Minimum target nodes:
- Mansion Exterior / Primary Entrance;
- Core Estate Grounds;
- Tactical Obstacle Course;
- Private Lake Access;
- Hidden Dock;
- Rear Forested Estate Zone;
- Main Approach;
- Main Security Gate;
- Concealed Forest Passage;
- Garage exterior/approach if needed by the chosen graph.

Required behavior:
- Darian can leave the mansion and traverse meaningful Estate campus nodes;
- access remains private-property aware;
- ordinary return paths work;
- main gate outward edge remains locked;
- concealed forest passage outward edge remains locked;
- hidden dock does not imply implemented boat/water travel;
- cognition sees only legal local movement options.

## WF-5 dual outside-world unlock

When regional expansion is separately authorized, road and forest boundaries may be opened independently.

Recommended order:
1. ordinary main-gate -> public-road connector;
2. bounded rear-forest -> backcountry connector;
3. water travel only in a later explicit slice.

This allows outside-world expansion without requiring vehicles, boats or a complete wilderness simulation simultaneously.

## Canon map acceptance criteria

This planning map is ready when:
- every proposed Estate campus node has a confidence class;
- source-confirmed details are not mixed with inferred layout;
- older unsupported campus candidates are explicitly excluded from automatic canon;
- main gate, forest passage and escape tunnels have separate semantics;
- Estate road/forest/water mobility directions are represented without prematurely opening outside travel;
- no exact real-world parcel or named trail claim is invented.

## Implementation boundary

This document is planning authority only.

It does not authorize:
- database/schema mutation;
- creation of production campus nodes;
- unlocking the current Estate exterior boundary;
- real public-road/backcountry/water edges;
- synthetic production travel;
- vehicle or boat runtime.

Implementation begins only after explicit Creator authorization.