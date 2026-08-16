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

The Estate-first foundation milestone is **COMPLETE / DEPLOYED v1** through Estate Campus Reachability, Spatial Familiarity Foundation v1 and Outdoor Spatial Affordance Cognition v1. South Lake Tahoe remains intentionally paused.

Canonical world/cognition docs:
1. `docs/WORLD_FOUNDATION_EXPANSION_PLAN_V1.md`
2. `docs/WORLD_LOCATION_NODE_MODEL.md`
3. `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`
4. `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`
5. `docs/WORLD_GEOGRAPHY_EXPANSION_CONTRACT_V1.md`
6. `docs/THORNE_ESTATE_CAMPUS_CANON_MAP_V1.md`
7. `docs/WORLD_FOUNDATION_IMPLEMENTATION_SEQUENCE_V1.md`
8. `docs/ESTATE_CAMPUS_REACHABILITY_V1.md`
9. `docs/WORLD_SPATIAL_FAMILIARITY_CONTRACT_V1.md`
10. `docs/WORLD_OUTDOOR_SPATIAL_AFFORDANCE_CONTRACT_V1.md`

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

## Spatial knowledge semantic lock

World geography and character knowledge are separate authoritative layers.

Canonical separation:
1. **World truth** — what represented locations/topology objectively exist.
2. **Character-known world** — what represented geography this actor is authored to know.
3. **Current actionable space** — exact actions/moves the deterministic runtime permits now.

Spatial familiarity levels are:
`unknown -> aware -> familiar -> intimate`.

Hidden/secret status is orthogonal to familiarity. Known geography is planning knowledge only. It never grants teleportation, access permission, or a non-local target. Exact executable moves remain authoritative only when present in current `action_options`.

## Outdoor-lived-space semantic lock

A reachable outdoor node is not automatically a meaningful lived destination.

`world.spatial_container.affordances` now authors ordinary location-level activity. V1 generic activities are `walk`, `relax` and `observe`.

Preserve:
- `walk` is activity within the current container, not inter-location travel;
- `move` remains authoritative for changing `located_at`;
- outdoor attraction is a soft positive choice signal, never a quota;
- dedicated indoor `rest` remains a stronger recovery option than ordinary outdoor `relax`;
- known outdoor lifestyle destinations may appear in planning cognition while exact execution stays local;
- security/egress/utility nodes must not become recreation defaults merely because they are outdoors;
- no weather/daylight/safety facts may be invented before environment runtime represents them.

Current Estate lifestyle destinations are Mansion Exterior, Core Estate Grounds, Private Lake Access and Rear Forested Estate. Tactical Obstacle Course remains training-oriented; Main Estate Approach remains transit-oriented; Hidden Dock, Concealed Forest Passage and Main Security Gate are not lifestyle-attraction destinations.

## Estate-first implementation checkpoint

### A0 — Location Spatial Container Contract v1 — COMPLETE

PR #196 / merge `d1167771ddb9c358a464c6efb863d9edf6800e18`.

### A1 — Existing Estate Location Refactor — COMPLETE / DEPLOYED

PR #197 added generic `world.spatial_container` metadata while preserving IDs/topology and keeping the legacy exterior boundary locked.

CI #955 SUCCESS; Strength Live Cycle Validation #86 SUCCESS.
Merge `886001a1d5d1cc62e5e9aab26a64fc08dedf08f1`.
Deploy #244 SUCCESS.

### A2 — Gameplay Runtime Reconnection / Regression — COMPLETE

PR #198 verified location, movement/options, move settlement, event/history linkage, object/location queries, training consumers and exterior lock after the refactor.

Final CI #957 SUCCESS.
Merge `3425315d2a3f564f0f3f5beb15084fda214c3036`.

### B — Estate Campus Reachability v1 — COMPLETE / DEPLOYED

PR #199 established the bounded private Estate campus through generic world/runtime data.

Current campus locations include Mansion Exterior, Core Estate Grounds, Tactical Obstacle Course, Private Lake Access, Hidden Dock, Rear Forested Estate, Concealed Forest Passage, Main Estate Approach and Main Security Gate.

Ordinary traversal begins:
`Master Suite -> Grand Foyer -> Mansion Exterior -> Core Estate Grounds`.

Final evidence:
- CI #959 SUCCESS;
- merge `f0955a582e11394ec64387f2a3fc0bfb468350b4`;
- Deploy #245 / run `31936858504` SUCCESS.

### C — Spatial Familiarity Foundation v1 — COMPLETE / DEPLOYED

PR #201 adds deterministic character-owned geographic knowledge without introducing a general episodic memory system.

Darian's normal represented home/interior and ordinary private Estate campus are authored as known geography. Rear Forested Estate is `familiar`; Hidden Dock and Concealed Forest Passage are explicitly known concealed Estate facilities at `familiar` under current story continuity.

Evidence:
- CI #960 / run `31937649311` SUCCESS;
- merge `4778eb3e5fc0877ad49e7c96570f00ee5de4e121`;
- Deploy #246 / run `31937763776` SUCCESS.

### D — Outdoor Spatial Affordance Cognition v1 — COMPLETE / DEPLOYED

PR #204 turns selected familiar campus outdoor locations into ordinary lived spaces rather than traversal-only nodes.

Runtime changes:
- generic `walk`, `relax`, `observe` actions;
- deterministic location-authored affordance validation;
- lifestyle-destination metadata and atmosphere tags;
- one-hop previews now explain location-level activities available after arrival;
- broader known-map cognition projects familiar outdoor lifestyle destinations even when distant;
- Darian autonomy guidance gives outdoor walking, lakeside quiet time, forest walking, outdoor observation and decompression positive consideration without creating a quota;
- training repetition pressure may make these non-training alternatives more attractive but does not force them.

Current authoring:
- Mansion Exterior: `observe`, `relax`;
- Core Estate Grounds: `walk`, `relax`, `observe`;
- Private Lake Access: `relax`, `observe`;
- Rear Forested Estate: `walk`, `relax`, `observe`.

Tactical Obstacle Course stays training-oriented. Main Estate Approach is transit-oriented. Main Security Gate, Concealed Forest Passage and Hidden Dock are deliberately excluded from lifestyle attraction.

Validation:
- first CI run exposed only a stale policy-revision assertion: 642 passed / 1 failed;
- corrected final head `71f0ad934c34bcc31ad16928a2cad9ce459234fc`;
- CI #963 / run `31939974004` SUCCESS including pytest, init and status;
- Strength Live Cycle Validation #91 SUCCESS;
- merge `14c48908bfefaf7509249cddafe3eb30c5ef0623`;
- Deploy #248 / run `31940047281` SUCCESS including application sync, cognition configuration, restart and verification.

No synthetic Darian production action was created for proof.

## Current simulation boundary

The represented world is the mansion plus bounded private Thorne Estate campus.

Outside continuations remain absent:
- Main Security Gate has no public-road edge;
- Concealed Forest Passage has no Tahoe-backcountry edge;
- Hidden Dock has no water-travel edge;
- legacy Estate Exterior remains locked/non-traversable.

## Memory/discovery boundary

Spatial Familiarity v1 is not the future character memory system.

Deferred:
- episodic memories;
- automatic discovery/revelation transitions;
- familiarity learning/decay from lived experience;
- forgetting;
- map-item or teaching mechanics.

## South Lake Tahoe — intentionally PAUSED

Do not infer authorization to open the public world from the Estate milestones.

Do not currently:
- add `loc_south_lake_tahoe` or public-road topology;
- connect the Main Security Gate outward;
- connect the Concealed Forest Passage outward;
- enable Hidden Dock water travel;
- add public venues/economy/population merely because later contracts exist.

Outside-world expansion requires a separate Creator priority decision.

## World-scale cognition rule

World growth must not make cognition context scale blindly with world size.

Use a compact actor-relative projection:
`current executable space + relevant local previews + compact known geography + task-relevant context`.

Do not serialize the entire objective world into each model call.

## Current verified deployment

Latest verified runtime deployment: **Deploy #248 / run `31940047281` SUCCESS**, runtime merge `14c48908bfefaf7509249cddafe3eb30c5ef0623`.

Schema remains v5. Outdoor Spatial Affordance Cognition v1 required no schema migration.

## Exact resume point

**Estate Campus Reachability, Spatial Familiarity Foundation v1 and Outdoor Spatial Affordance Cognition v1 are COMPLETE / DEPLOYED. Keep South Lake Tahoe/public/backcountry/water expansion paused. Resume by naturally observing Darian at the Creator-set 30x speed: specifically whether he now chooses Mansion Exterior/Core Grounds/Lake Access/Rear Forest for walking, quiet relaxation or observation at plausible times; whether indoor rest remains natural rather than disappearing; whether multi-step movement toward distant known outdoor destinations is coherent; and whether security/egress nodes remain non-attractive. Refine only evidence-backed Estate-local behavior gaps.**
