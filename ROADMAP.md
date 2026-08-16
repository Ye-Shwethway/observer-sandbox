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

Character Profile minimum foundations, Skills v1, Adaptive Character Disposition Foundation and Overall Workflow/Foundation Review v1 remain closed enough for the current purpose. Character-side depth is not the immediate priority.

## Active strategic phase — Estate-first World Foundation

The Estate-first foundation milestone is now **COMPLETE / DEPLOYED v1** through Estate Campus Reachability.

Canonical docs:
1. `docs/WORLD_FOUNDATION_EXPANSION_PLAN_V1.md`
2. `docs/WORLD_LOCATION_NODE_MODEL.md`
3. `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`
4. `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`
5. `docs/WORLD_GEOGRAPHY_EXPANSION_CONTRACT_V1.md`
6. `docs/THORNE_ESTATE_CAMPUS_CANON_MAP_V1.md`
7. `docs/WORLD_FOUNDATION_IMPLEMENTATION_SEQUENCE_V1.md`
8. `docs/ESTATE_CAMPUS_REACHABILITY_V1.md`

## Location semantic lock

A location is not a point.

Canonical rule:

`location = identifiable nested spatial container with extent, contents, boundaries/interfaces, local state, control and explicit relationships to surrounding space`

The graph node is the stable identity/hierarchy/topology representation of that container.

Preserve:
- containment != dynamic presence;
- adjacency/proximity != traversability;
- topology != access;
- ownership/control != occupancy;
- access policy != operating/open state;
- entrances/exits/doors/gates/passages are spatial interfaces and do not all require independent location nodes.

No full GIS/polygon model is required for the current Estate implementation.

## Estate-first implementation checkpoint

### A0 — Location Spatial Container Contract v1 — COMPLETE

PR #196 / merge `d1167771ddb9c358a464c6efb863d9edf6800e18`.

The location ontology was completed before runtime mutation.

### A1 — Existing Estate Location Refactor — COMPLETE / DEPLOYED

PR #197:
- added `config/worlds/home.spatial.v1.json`;
- seeded `world.spatial_container` through generic field storage;
- preserved existing IDs and topology;
- separated source confidence from provisional layout confidence;
- kept the legacy exterior boundary locked/non-traversable.

CI #955 SUCCESS; Strength Live Cycle Validation #86 SUCCESS.
Merge `886001a1d5d1cc62e5e9aab26a64fc08dedf08f1`.
Deploy #244 SUCCESS.

### A2 — Gameplay Runtime Reconnection / Regression — COMPLETE

PR #198 verified the refactored Estate against current gameplay/runtime:
- actor/current location;
- movement/action options;
- move settlement;
- event/history linkage;
- object/location queries;
- training location consumers;
- locked exterior boundary.

The initial failure was only a test misconception about move-event completion location; runtime behavior matched the existing event contract.

Final CI #957 SUCCESS.
Merge `3425315d2a3f564f0f3f5beb15084fda214c3036`.

### B — Estate Campus Reachability v1 — COMPLETE / DEPLOYED

PR #199 added the bounded private Estate campus through an additive generic world seed.

Represented campus locations:
- Mansion Exterior;
- Core Estate Grounds;
- Tactical Obstacle Course;
- Private Lake Access;
- Hidden Dock;
- Rear Forested Estate;
- Concealed Forest Passage;
- Main Estate Approach;
- Main Security Gate.

Ordinary traversal spine:

`Master Suite -> Grand Foyer -> Mansion Exterior -> Core Estate Grounds`

From Core Estate Grounds the current graph reaches:
- Tactical Obstacle Course;
- Private Lake Access -> Hidden Dock;
- Rear Forested Estate -> Concealed Forest Passage;
- Main Estate Approach -> Main Security Gate;
- Garage & Workshop through an Estate-side connection.

Campus fixtures expose executable options through the existing generic action-option engine. The Tactical Obstacle Course exposes a real outdoor `train` option.

Acceptance proves Darian can leave the mansion, traverse/use the private campus, and return through ordinary movement/action runtime.

Final evidence:
- CI #959 SUCCESS;
- Strength Live Cycle Validation #88 SUCCESS;
- Inventory Foundation Acceptance #51 SUCCESS;
- Skill Evidence Semantics Acceptance #42 SUCCESS;
- Skill Progression Acceptance #59 SUCCESS;
- Technology Diagnostic Acceptance #33 SUCCESS;
- merge `f0955a582e11394ec64387f2a3fc0bfb468350b4`;
- Deploy #245 / run `31936858504` SUCCESS, including sync, install/configure, restart and verification.

No synthetic production Darian movement was performed solely for proof.

## Current simulation boundary

The project has moved from a mansion-interior-only world to a bounded **private Thorne Estate world**.

Estate-side endpoints are represented and reachable where appropriate, but all outside continuations remain absent:
- Main Security Gate has no public-road edge;
- Concealed Forest Passage has no Tahoe-backcountry edge;
- Hidden Dock has no water-travel edge;
- legacy Estate Exterior boundary remains locked/non-traversable.

## South Lake Tahoe — intentionally PAUSED

Do not infer authorization to open the public world from the Estate milestone.

Do not currently:
- add `loc_south_lake_tahoe` or public-road topology;
- connect the Main Security Gate outward;
- connect the Concealed Forest Passage outward;
- enable Hidden Dock water travel;
- add public venues/economy/population simply because later world contracts exist.

Outside-world expansion requires a separate Creator priority decision.

## World-scale cognition rule

World growth must not make cognition context scale with world size.

Preferred projection:
`current container -> relevant local facilities/interfaces -> legal nearby/reachable options -> compact decision context`

Do not serialize the whole Estate/world into each model call.

## Current verified deployment

Latest verified runtime deployment: **Deploy #245 / run `31936858504` SUCCESS**, runtime merge `f0955a582e11394ec64387f2a3fc0bfb468350b4`.

Schema remains v5; the Estate campus implementation required no schema migration.

## Exact resume point

**A0 Location Spatial Container Contract, A1 Existing Estate Location Refactor, A2 Gameplay Runtime Reconnection/Regression, and B Estate Campus Reachability v1 are COMPLETE. Darian can now leave the mansion, use represented private Estate campus locations/actions, and return through generic runtime. South Lake Tahoe/public/backcountry/water expansion remains explicitly paused. Resume with observation/refinement of the Estate campus or the next Creator-prioritized Estate-local feature, not automatic outside-world expansion.**
