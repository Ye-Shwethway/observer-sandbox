# Estate Campus & South Lake Tahoe Geography Expansion Contract v1

Status: PLANNING AUTHORITY — IMPLEMENTATION NOT YET AUTHORIZED

## Purpose

This document refines WF-4 and WF-5. It defines how Observer Sandbox expands from the current Thorne Estate interior into the Estate campus and then into a bounded South Lake Tahoe regional world without pretending to model the full real city.

For exact Estate-campus canon/provisional classification, read `docs/THORNE_ESTATE_CAMPUS_CANON_MAP_V1.md` as the authoritative content map.

## Expansion rule

Open geography in concentric, usable rings:

1. mansion interior;
2. Estate campus;
3. Estate boundary connectors;
4. bounded South Lake Tahoe destinations;
5. later town/wilderness/institutional expansion.

A ring is not opened merely because its parent region exists. It opens only when meaningful nodes, legal routes, access state, and at least minimal use semantics are represented.

## Canon versus provisional layout

Geography/content may be classified as:
- `source_confirmed` / canonical — directly supported by the original Estate source;
- `story_established` / canonical — explicitly reaffirmed Creator-approved storyline continuity;
- `structurally_inferred` / `provisional_layout` — needed for traversal but not directly sourced;
- `planned_unapproved` — discussed but not canonical and not represented.

Technical IDs must remain stable where possible even if provisional layout metadata later improves. Do not silently convert inferred geometry or old memory into canon.

## Estate campus v1

The campus content baseline is defined by `THORNE_ESTATE_CAMPUS_CANON_MAP_V1.md`.

Source/story-backed anchors include:
- Main Mansion and Garage & Workshop;
- Tactical Obstacle Course;
- Private Lake Access;
- Hidden Dock;
- rear forested Estate zone;
- concealed forest passage;
- underground escape capability.

Structurally inferred connectors may include:
- Mansion Exterior / Primary Entrance;
- Core Estate Grounds;
- Main Approach;
- Main Security Gate;
- minimal internal connector paths/edges.

Garden, swimming pool and tennis court are not supported by the supplied mansion source and remain `planned_unapproved` unless the Creator explicitly adopts them later.

The exact graph should favor meaningful navigation over architectural micromapping.

## Estate mobility directions

The Estate canon map establishes three conceptually distinct mobility directions:

1. **Road / ordinary access** — through the formal main security gate to a future public-road connector.
2. **Forest / backcountry access** — through the rear forested Estate and concealed forest passage to a future bounded Tahoe backcountry connector.
3. **Water / covert access** — through Private Lake Access and Hidden Dock; water travel remains later explicit work.

Main security gate, concealed forest passage and tactical escape tunnels are separate semantics and must not collapse into one generic exit.

## Estate boundary semantics

Before WF-5:
- Estate-side main gate may exist and be reachable;
- Estate-side concealed forest passage may exist and be reachable;
- Hidden Dock may exist as a campus destination;
- outward public-road, backcountry and water routes remain absent/locked.

After WF-5:
- road and forest outside-world edges may be opened independently after their destination graph is represented;
- only authored regional destinations become reachable;
- water travel remains a separate later slice unless explicitly authorized.

## Regional parent insertion

`loc_south_lake_tahoe` becomes the structural regional parent of `loc_thorne_estate` and future Tahoe locations.

This insertion must not require renaming existing Estate IDs or invalidate actor/object identity.

## Bounded regional representation

South Lake Tahoe v1 is a simulation region, not a complete geographic database.

Initially represent only locations needed for meaningful loops:
- the Estate;
- immediate road/public connector network;
- a bounded rear-forest/backcountry connector when authorized;
- a small set of public/service destinations;
- selected outdoor/recreation destinations later.

Unrepresented real places remain unavailable to simulation until authored. The LLM may not fabricate them into authoritative topology.

## Real-world source policy

For public real-world geography:
- use current reputable official/map/business sources when exact existence/location matters;
- store only the precision needed by the simulation;
- distinguish durable place identity from volatile facts such as opening hours;
- do not assume a business remains open or unchanged without current verification at authoring/update time;
- avoid unnecessary copying of external datasets.

Official Tahoe geography may establish plausibility of forest/backcountry context, but it does not establish the fictional Estate's exact parcel, legal boundary, named adjacent trail, or precise shoreline/road geometry.

Creator-authored fictional/private locations may coexist with real public geography and should be clearly classified as fictional/private world content.

## Address and coordinates

V1 may keep human-readable locality/address metadata and optional coordinates for orientation. Coordinates are not routing authority unless a later routing implementation explicitly adopts them.

The authored relation graph remains authoritative for legal simulation traversal.

## Road and backcountry representation

Do not model every street or trail segment.

Use coarse connector nodes/edges sufficient to represent:
- leaving the Estate;
- entering bounded public-road or backcountry space;
- reaching selected destinations;
- meaningful route duration;
- later insertion of additional destinations without redesign.

Do not claim a named public trail directly borders the Estate unless separately sourced/authored.

## Regional destination admission test

A new public destination should satisfy at least one simulation need:
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
2. traverses campus to one represented boundary connector;
3. legally crosses into represented public-road or backcountry topology;
4. can reach one bounded regional destination or waypoint;
5. travel duration advances simulation time;
6. ordinary return route remains valid;
7. no unrepresented Tahoe locations appear as legal cognition options.

## Deferred depth

Not required for Estate/Tahoe v1:
- full municipal map;
- parcel-accurate property boundaries;
- live traffic map;
- exhaustive business directory;
- turn-by-turn street navigation;
- exact named-trail adjacency to the fictional Estate;
- boat/water runtime;
- broad NPC population;
- civic/legal systems;
- region-wide event simulator.

## Unlock relationship

WF-4 completes when source/story-backed Estate campus locations and necessary provisional connectors are traversable and useful while all outside-world edges remain hard boundaries.

WF-5 completes when at least one Estate boundary connects to a bounded represented South Lake Tahoe graph. This then unlocks environment, venues/services, resources and later world-process work on genuinely reachable outside locations.