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

## Strategic checkpoint

Character-side minimum foundations remain closed enough for the current purpose.

The Estate-first world sequence has now reached **Estate Campus Reachability v1 COMPLETE / DEPLOYED**. South Lake Tahoe remains intentionally paused.

## Required world read order

1. `docs/WORLD_FOUNDATION_EXPANSION_PLAN_V1.md`
2. `docs/WORLD_LOCATION_NODE_MODEL.md`
3. `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`
4. `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`
5. `docs/WORLD_GEOGRAPHY_EXPANSION_CONTRACT_V1.md`
6. `docs/THORNE_ESTATE_CAMPUS_CANON_MAP_V1.md`
7. `docs/WORLD_FOUNDATION_IMPLEMENTATION_SEQUENCE_V1.md`
8. `docs/ESTATE_CAMPUS_REACHABILITY_V1.md`

## Location semantic rule

A location is not a dimensionless point.

Canonical definition:

`location = identifiable nested spatial container with extent, contents, boundaries/interfaces, local state, control and explicit relationships to surrounding space`

The graph node is the stable identity/hierarchy/topology representation of that container.

Preserve:
- `contains` = structural spatial membership;
- `located_at` = dynamic presence;
- `connected_to` = traversable topology;
- adjacency/proximity != traversability;
- ownership/control != containment/presence;
- access policy != operating/open state;
- entrances/exits/doors/gates/passages are spatial-interface semantics, not automatically independent nodes.

## Completed Estate-first sequence

### A0 — Location Spatial Container Contract v1

COMPLETE through PR #196 / merge `d1167771ddb9c358a464c6efb863d9edf6800e18`.

### A1 — Existing Estate Location Refactor

COMPLETE / DEPLOYED through PR #197:
- generic `world.spatial_container` metadata;
- stable IDs/topology preserved;
- source/layout confidence separated;
- Estate represented as approximately 50-acre private spatial container;
- legacy exterior boundary remains locked.

CI #955 SUCCESS; Strength Live Cycle Validation #86 SUCCESS.
Merge `886001a1d5d1cc62e5e9aab26a64fc08dedf08f1`.
Deploy #244 SUCCESS.

### A2 — Gameplay Runtime Reconnection / Regression

COMPLETE through PR #198.

Regression coverage proves current snapshot/location resolution, movement/options, move settlement, event/history linkage, object/location query behavior, training consumers and exterior lock remain coherent after the refactor.

Final CI #957 SUCCESS.
Merge `3425315d2a3f564f0f3f5beb15084fda214c3036`.

### B — Estate Campus Reachability v1

COMPLETE / DEPLOYED through PR #199.

Current campus locations:
- Mansion Exterior;
- Core Estate Grounds;
- Tactical Obstacle Course;
- Private Lake Access;
- Hidden Dock;
- Rear Forested Estate;
- Concealed Forest Passage;
- Main Estate Approach;
- Main Security Gate.

Ordinary traversal begins:

`Master Suite -> Grand Foyer -> Mansion Exterior -> Core Estate Grounds`

Campus branches then reach the obstacle course, lake/dock, rear forest/concealed passage, and main approach/security gate. Garage & Workshop also connects Estate-side into the grounds.

Machine-readable campus fixtures feed the existing generic action-option engine; the outdoor Tactical Obstacle Course exposes a real `train` option.

Acceptance tests prove Darian can leave the mansion, reach/use the campus and return through ordinary runtime.

Final evidence:
- CI #959 SUCCESS;
- Strength Live Cycle Validation #88 SUCCESS;
- Inventory Foundation Acceptance #51 SUCCESS;
- Skill Evidence Semantics Acceptance #42 SUCCESS;
- Skill Progression Acceptance #59 SUCCESS;
- Technology Diagnostic Acceptance #33 SUCCESS;
- merge `f0955a582e11394ec64387f2a3fc0bfb468350b4`;
- Deploy #245 / run `31936858504` SUCCESS, including sync, install/configure, restart and verification.

No synthetic production movement was performed solely for proof.

## Current world boundary

The represented world now includes the mansion plus the bounded private Estate campus.

Outside continuation remains unavailable:
- Main Security Gate -> no public road edge;
- Concealed Forest Passage -> no Tahoe backcountry edge;
- Hidden Dock -> no water-travel edge;
- legacy Estate Exterior -> locked/non-traversable.

## South Lake Tahoe — PAUSED

Do not currently create or enable:
- public South Lake Tahoe regional graph;
- public-road continuation from the Main Security Gate;
- Tahoe-backcountry continuation from Concealed Forest Passage;
- Hidden Dock water travel;
- public venue/economy/population loops merely because future contracts exist.

Outside-world expansion resumes only on separate Creator prioritization.

## Current verified deployment

Latest verified runtime deployment: **Deploy #245 / run `31936858504` SUCCESS**.

Runtime merge: `f0955a582e11394ec64387f2a3fc0bfb468350b4`.
Schema remains v5; no schema migration was needed for Estate campus reachability.

## Exact resume point

**A0 Location Spatial Container Contract v1, A1 Existing Estate Location Refactor, A2 Gameplay Runtime Reconnection/Regression, and B Estate Campus Reachability v1 are COMPLETE. Darian can now leave the mansion, use represented private Estate campus places/actions, and return through generic runtime. Keep all South Lake Tahoe/public/backcountry/water continuations locked. Resume with Estate-campus observation/refinement or the next Creator-prioritized Estate-local feature; do not automatically expand outside Tahoe.**
