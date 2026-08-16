# Estate Campus & South Lake Tahoe Geography Expansion Contract v1

Status: PLANNING AUTHORITY — IMPLEMENTATION NOT YET AUTHORIZED

## Purpose

This document refines WF-4 and WF-5. It defines how Observer Sandbox expands from the current Thorne Estate interior into the Estate campus and then into a bounded South Lake Tahoe regional world without pretending to model the full real city.

## Expansion rule

Open geography in concentric, usable rings:

1. mansion interior;
2. Estate campus;
3. Estate gate/public connector;
4. bounded South Lake Tahoe destinations;
5. later town/wilderness/institutional expansion.

A ring is not opened merely because its parent region exists. It opens only when meaningful nodes, legal routes, access state, and at least minimal use semantics are represented.

## Canon versus provisional layout

Three geography states are permitted:
- `canonical`: source-supported or explicitly Creator-approved;
- `provisional_layout`: necessary spatial arrangement not established by source;
- `planned`: discussed but not yet represented.

Technical IDs must remain stable where possible even if provisional layout metadata later improves.

Do not silently convert inferred geometry into canon.

## Estate campus v1

Candidate campus surface:
- Main Mansion exterior / primary entrance;
- front grounds;
- rear grounds;
- garden;
- pool area;
- tennis court;
- driveway;
- garage exterior / vehicle approach;
- security gate;
- bounded perimeter/path nodes only where useful.

The exact graph should favor meaningful navigation over architectural micromapping. A lawn does not need ten nodes unless distinct gameplay/runtime semantics justify them.

## Estate campus functional requirement

Each authored campus node should provide at least one of:
- traversal significance;
- facility/resource significance;
- environmental significance;
- activity affordance;
- access/boundary significance.

Decorative labels alone are insufficient reason for a node.

## Estate gate semantics

The gate is both a physical transition and an access boundary.

Before WF-5:
- Estate-side gate node may exist;
- actor may reach it from inside the Estate;
- outward public-world route remains absent/locked.

After WF-5:
- a represented public connector exists outside the gate;
- the gate transition composes private-property access with public-road topology;
- only authored regional destinations become reachable.

## Regional parent insertion

`loc_south_lake_tahoe` becomes the structural regional parent of `loc_thorne_estate` and future Tahoe locations.

This parent insertion must not require renaming existing Estate IDs or invalidate actor/object identity. Structural hierarchy can evolve while stable entity IDs remain path-independent.

## Bounded regional representation

South Lake Tahoe v1 is a simulation region, not a complete geographic database.

The region should initially contain only locations needed for meaningful loops, such as:
- the Estate;
- immediate road/public connector network;
- a small set of public/service destinations;
- selected outdoor/recreation destinations later;
- other residences only when required.

Unrepresented real places are simply unavailable to simulation until authored. The LLM may not fabricate them into authoritative topology.

## Real-world source policy

For public real-world geography:
- use current reputable map/official/business sources when exact existence/location matters;
- store only the precision needed by the simulation;
- distinguish durable place identity from volatile facts such as opening hours;
- do not assume a business remains open or unchanged without current verification at authoring/update time;
- avoid unnecessary copying of full external datasets.

Creator-authored fictional/private locations may coexist with real public geography and should be clearly classifiable as fictional/private world content.

## Address and coordinates

V1 may keep human-readable locality/address metadata and optional coordinates for orientation. Coordinates are not the routing authority unless a later routing implementation explicitly adopts them.

The authored relation graph remains authoritative for legal simulation traversal.

## Road representation

Do not model every street segment.

Use coarse connector nodes/edges sufficient to represent:
- leaving the Estate;
- reaching first selected destinations;
- meaningful route duration;
- later insertion of additional destinations without redesign.

Road/connector topology should be expandable and not destination-specific hard-coded travel tables.

## Regional destination admission test

A new public destination should not be added merely because it exists in real life. It should satisfy at least one simulation need:
- service/resource loop;
- social/character destination;
- recreation/activity;
- healthcare/safety;
- transportation support;
- meaningful world event or story relevance.

This keeps world growth useful rather than encyclopedic.

## First regional unlock proof

WF-5 is ready only after Estate Campus is usable.

First public-world proof should demonstrate:
1. actor begins inside Estate;
2. traverses campus to security gate;
3. legally crosses into a represented public connector;
4. can reach one bounded regional destination or public waypoint;
5. travel duration advances simulation time;
6. ordinary return route remains valid;
7. no unrepresented Tahoe locations appear as legal cognition options.

## Telegram/observer expectation

World browsing should eventually show recursive geography with friendly names and access/reachability state, but geography authority remains in generic world queries rather than Telegram-specific structures.

## Deferred depth

Not required for Estate/Tahoe v1:
- full municipal map;
- parcel-accurate property boundaries;
- live traffic map;
- exhaustive business directory;
- turn-by-turn street navigation;
- broad NPC population;
- civic/legal systems;
- region-wide event simulator.

## Unlock relationship

WF-4 completes when Estate campus is traversable and usable while the gate remains a hard world edge.

WF-5 completes when the gate connects to a bounded represented South Lake Tahoe graph. This then unlocks environment, venues/services, resources and later world-process planning on genuinely reachable outside locations.