# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-16

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema, and verified live production outrank remembered chat context.
- AI proposes structured cognition; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Preserve: `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Prefer vertical completeness before local depth.
- Never manipulate production merely to manufacture evidence.
- Code/runtime PRs get one final full CI checkpoint by default; docs-only changes do not need the Python suite.

## Character-side checkpoint

All Character Profile sections are minimum-unlocked v1. Skills remains CLOSED v1. Adaptive Character Disposition Foundation is COMPLETE v1. Overall Workflow/Foundation Review v1 is COMPLETE / CLOSED.

Character-side depth is not the immediate priority.

## Active phase — Estate-first World Foundation

Status: **LOCATION ONTOLOGY DOCUMENTATION FIRST; IMPLEMENTATION NEXT**.

The immediate goal is not South Lake Tahoe expansion. The private Thorne Estate must first become a semantically coherent, runtime-safe spatial world.

### Canonical world-planning read order

1. `docs/WORLD_FOUNDATION_EXPANSION_PLAN_V1.md`
2. `docs/WORLD_LOCATION_NODE_MODEL.md`
3. `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`
4. `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`
5. `docs/WORLD_GEOGRAPHY_EXPANSION_CONTRACT_V1.md`
6. `docs/THORNE_ESTATE_CAMPUS_CANON_MAP_V1.md`
7. `docs/WORLD_FOUNDATION_IMPLEMENTATION_SEQUENCE_V1.md`
8. later task-relevant environment/venue/resource/population/economy contracts only when their phase becomes active.

## Location ontology lock

A location is **not a point**.

Canonical semantic rule:

> `location = identifiable nested spatial container with extent, contents, boundaries/interfaces, local state, control and explicit relationships to surrounding space`

A graph node is the stable identity/topology representation of that spatial container.

The location contract now distinguishes:
- spatial containment;
- extent/area metadata;
- boundary;
- entrances/exits/spatial interfaces;
- adjacency/proximity versus legal traversability;
- ownership/control/access;
- operating and environmental state;
- facilities/affordances;
- occupants/resources/contained elements;
- temporal state changes.

No GIS/polygon precision or doorway-per-node model is required for v1.

## Current Estate source/canon

The original mansion source establishes approximately 50 acres of private land in the forested outskirts of South Lake Tahoe, with the Main Mansion, Garage & Workshop, Tactical Obstacle Course, Private Lake Access, Hidden Dock, Underground Bunker and tactical escape capability.

Creator-established storyline continuity adds the rear/western Estate forest/backcountry connection and Concealed Forest Passage.

`THORNE_ESTATE_CAMPUS_CANON_MAP_V1.md` separates `source_confirmed`, `story_established`, `structurally_inferred/provisional`, and `planned_unapproved` geography.

Garden, swimming pool and tennis court are not automatic canon from the supplied mansion source.

## Active near-term implementation sequence

The sequence is now Estate-first and must be executed in order.

### A0 — Location Spatial Container Contract v1

Current docs task. Define what a real represented location means without replacing the existing graph/node identity model.

### A1 — Existing Estate Location Refactor

After A0 is canonical:
- audit current Estate floors/rooms/objects against the new container semantics;
- preserve stable location IDs wherever possible;
- classify parent/kind/exposure/access/source confidence;
- make contained elements and entrances/exits/interfaces coherent;
- align facilities/affordances with machine-readable contained capabilities/resources;
- avoid inventing uncertain layout.

No campus traversal or Tahoe traversal should be added in A1.

### A2 — Gameplay Runtime Reconnection / Regression

Before campus expansion, reconnect the refactored Estate to current runtime and verify/fix:
- `located_at` and compatibility location handling;
- movement/routing;
- action targets and place-dependent validation;
- inventory/resource/object location consumers;
- training/physiology and other place-context consumers;
- cognition projection;
- scheduler/pending action references;
- event/history location linkage;
- Telegram/generic location browsing.

A2 must be green before adding new campus reachability.

### B — Estate Campus Reachability

Only after A1/A2:
- author source-confirmed/story-established Estate-side containers;
- add only minimal provisional grounds/approach/path connectors needed for coherent space;
- add ordinary mansion exterior interface and Estate-private walking routes;
- make Garage/Workshop, Tactical Obstacle Course, Private Lake Access, Hidden Dock, Rear Forested Estate, Main Security Gate and Concealed Forest Passage coherently reachable where supported;
- expand facilities/affordances and **choosable model options** from generic action/target/resource rules;
- prove Darian can leave the mansion, use multiple private campus locations and return through ordinary gameplay/runtime.

Main Security Gate, Concealed Forest Passage and Hidden Dock may be reachable Estate-side endpoints, but their outward public/backcountry/water continuations remain locked.

### B acceptance — Estate Campus Runtime Acceptance

Required proof includes:
- mansion -> campus -> mansion traversal;
- multiple meaningful campus destinations/actions;
- correct simulation-time/location/event/history continuity;
- no regressions to indoor gameplay;
- no illegal outside-world options in cognition;
- generic engine/data behavior, not Darian-specific runtime branches.

## South Lake Tahoe — intentionally paused

WF-5 regional/public expansion is not the current target.

Do not yet:
- connect the Main Security Gate to public roads;
- connect the Concealed Forest Passage to Tahoe backcountry;
- enable water travel from Hidden Dock;
- author public Tahoe destinations merely to advance the old roadmap;
- implement public economy/population/venue loops ahead of the Estate milestone.

Outside-world work resumes only after Estate Campus Runtime Acceptance and separate Creator prioritization.

## World-scale cognition rule

World growth must not make cognition context scale with world size.

Preferred projection:
`current container -> relevant local facilities/interfaces -> legal nearby/reachable options -> compact decision context`

Never serialize the whole Estate/world merely to let the model discover relevance.

## Current verified deployment

Latest verified runtime deployment remains **Deploy #243 / run `31931381264` SUCCESS**, schema v5.

All world work through the current ontology checkpoint is documentation-only; production runtime/world state has not been changed.

## Deferred depth / non-goals

Do not build merely for completeness: full GIS/polygon geometry, exact room dimensions, every doorway as a node, acoustic/visibility propagation, collision physics, detailed utilities, South Lake Tahoe public graph, vehicles/boats, climate simulation, macroeconomy, city-scale LLM population, law/crime, universal permission/hazard engines, or synthetic production events.

## Exact resume point

**Current task is A0 Location Spatial Container Contract v1. The repo must treat a location as a nested real spatial container, with the graph node serving only as stable identity/topology representation. Once A0 is canonical, proceed to A1 Existing Estate Location Refactor, then A2 Gameplay Runtime Reconnection/Regression, then Estate Campus Reachability and Campus Runtime Acceptance. South Lake Tahoe/public-world expansion is explicitly paused until that Estate-first milestone is green and separately prioritized by the Creator. Latest runtime remains Deploy #243 at schema v5.**
