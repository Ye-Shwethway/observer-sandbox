# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-16

## Startup / authority

Read and reconcile in order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical docs/source
5. verified production before runtime implementation decisions.

Authority:
`current Creator instruction > current repo contracts/config/schema > verified live runtime/DB > CI/deploy evidence > bootstrap > remembered chat`.

Default workflow:
`branch -> focused tests + final PR CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`

Docs-only planning work does not require the Python suite or runtime deploy.

## Strategic checkpoint

Character-side foundations are closed enough for the current purpose. The immediate priority is making the Thorne Estate a coherent spatial world before opening South Lake Tahoe.

## Active phase — Estate-first World Foundation

Status: **LOCATION ONTOLOGY DOCUMENTATION FIRST; IMPLEMENTATION NEXT**.

### Required read order

1. `docs/WORLD_FOUNDATION_EXPANSION_PLAN_V1.md`
2. `docs/WORLD_LOCATION_NODE_MODEL.md`
3. `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`
4. `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`
5. `docs/WORLD_GEOGRAPHY_EXPANSION_CONTRACT_V1.md`
6. `docs/THORNE_ESTATE_CAMPUS_CANON_MAP_V1.md`
7. `docs/WORLD_FOUNDATION_IMPLEMENTATION_SEQUENCE_V1.md`

Read later environment/venue/resource/population/economy contracts only when their phase becomes active.

## Location semantic rule

A location is **not a dimensionless point**.

Canonical definition:

`location = identifiable nested spatial container with extent, contents, boundaries/interfaces, local state, control and explicit relationships to surrounding space`

The graph node is the stable identity/hierarchy/topology representation of that container.

Key distinctions:
- `contains` = structural spatial membership;
- `located_at` = dynamic presence;
- `connected_to` = legal traversable topology;
- adjacency/proximity != traversability;
- ownership/control != containment/presence;
- access policy != operating/open state;
- entrance/exit/door/gate/passage = spatial interface concept, not automatically a location node.

GIS polygons, exact dimensions and doorway-per-node modeling are not required for v1.

## Current Estate canon/source checkpoint

Original mansion source supports:
- approximately 50 acres private land in the forested outskirts of South Lake Tahoe;
- Main Mansion;
- Garage & Workshop;
- Tactical Obstacle Course;
- Private Lake Access;
- Hidden Dock;
- Underground Bunker;
- tactical escape tunnels/safe exit capability.

Creator-reaffirmed storyline canon adds:
- rear/western Estate forest/backcountry continuity;
- Concealed Forest Passage as a distinct low-visibility Estate boundary/egress concept.

The Main Security Gate, Concealed Forest Passage and tactical escape tunnels are distinct semantics. Garden, swimming pool and tennis court are not automatic canon from the supplied mansion source.

## Active near-term sequence

### A0 — Location Spatial Container Contract v1

Current documentation checkpoint. Complete and canonicalize the ontology before runtime mutation.

### A1 — Existing Estate Location Refactor

Next implementation slice after A0:
- audit current Estate locations against container semantics;
- preserve stable IDs wherever possible;
- confirm parent/kind/exposure/access/source confidence;
- align contained children/fixtures/resources;
- make entrances/exits/interfaces coherent with topology;
- align facilities/affordances with machine-readable capabilities;
- avoid inventing unsourced layout.

No new campus/public traversal in A1.

### A2 — Gameplay Runtime Reconnection / Regression

Then verify/fix current location consumers:
- actor `located_at` and compatibility location;
- movement/routing;
- action-target/place validation;
- inventory/resource/object location queries;
- training/physiology/place-context consumers;
- cognition compact projection;
- scheduler/pending action location references;
- event/history location linkage;
- Telegram/generic location browsing.

A2 must be green before campus reachability.

### B — Estate Campus Reachability

After A1/A2:
- author Estate-side source-confirmed/story-established containers plus minimal provisional connector spaces;
- create coherent ordinary mansion exterior and Estate-private walking topology;
- make meaningful campus facilities/affordances usable;
- expand cognition-visible **choosable options** only from generic executable action/target/resource/facility rules;
- prove Darian can leave the mansion, use multiple campus locations and return through normal gameplay/runtime.

Estate-side Main Gate, Concealed Forest Passage and Hidden Dock may be reachable, but all outward public/backcountry/water continuations remain locked.

## South Lake Tahoe — PAUSED

Do not currently:
- connect Main Security Gate to public roads;
- connect Concealed Forest Passage to Tahoe backcountry nodes;
- enable Hidden Dock water travel;
- author arbitrary public Tahoe destinations;
- implement public venue/economy/population loops ahead of Estate acceptance.

Outside-world expansion resumes only after Estate Campus Runtime Acceptance and separate Creator prioritization.

## Current verified runtime

Latest verified runtime deployment remains **Deploy #243 / run `31931381264` SUCCESS**, schema v5.

The current ontology work is docs-only and has made no runtime/schema/production world change.

## Exact resume point

**Complete A0 Location Spatial Container Contract v1 first. Then proceed in order: A1 Existing Estate Location Refactor -> A2 Gameplay Runtime Reconnection/Regression -> B Estate Campus Reachability -> Estate Campus Runtime Acceptance. The goal is to make the current Estate a complete, coherent spatial simulation boundary and allow Darian to use the private campus before any South Lake Tahoe expansion. Public/backcountry/water outside edges remain locked. Latest runtime remains Deploy #243 at schema v5.**
