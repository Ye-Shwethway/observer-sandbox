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

The Estate-first sequence is now complete/deployed through **Estate Campus Reachability v1** and **Spatial Familiarity Foundation v1**. South Lake Tahoe remains intentionally paused.

## Required world read order

1. `docs/WORLD_FOUNDATION_EXPANSION_PLAN_V1.md`
2. `docs/WORLD_LOCATION_NODE_MODEL.md`
3. `docs/WORLD_LOCATION_SPATIAL_CONTAINER_CONTRACT_V1.md`
4. `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`
5. `docs/WORLD_GEOGRAPHY_EXPANSION_CONTRACT_V1.md`
6. `docs/THORNE_ESTATE_CAMPUS_CANON_MAP_V1.md`
7. `docs/WORLD_FOUNDATION_IMPLEMENTATION_SEQUENCE_V1.md`
8. `docs/ESTATE_CAMPUS_REACHABILITY_V1.md`
9. `docs/WORLD_SPATIAL_FAMILIARITY_CONTRACT_V1.md`

## Location semantic rule

A location is not a dimensionless point.

Canonical definition:
`location = identifiable nested spatial container with extent, contents, boundaries/interfaces, local state, control and explicit relationships to surrounding space`

The graph node is the stable identity/hierarchy/topology representation of that container.

## Spatial knowledge rule

Keep three layers distinct:
1. **World truth** — represented objective geography/topology.
2. **Character-known world** — the subset of geography an actor is authored to know.
3. **Current actionable space** — exact deterministic moves/actions executable now.

Spatial familiarity vocabulary:
`unknown -> aware -> familiar -> intimate`.

Hidden/secret is orthogonal to familiarity. Known geography supports planning but never grants teleportation, permission or a non-local target. Exact movement authority remains current `action_options`.

## Completed Estate-first sequence

### A0 — Location Spatial Container Contract v1

COMPLETE through PR #196 / merge `d1167771ddb9c358a464c6efb863d9edf6800e18`.

### A1 — Existing Estate Location Refactor

COMPLETE / DEPLOYED through PR #197.

CI #955 SUCCESS; Strength #86 SUCCESS.
Merge `886001a1d5d1cc62e5e9aab26a64fc08dedf08f1`.
Deploy #244 SUCCESS.

### A2 — Gameplay Runtime Reconnection / Regression

COMPLETE through PR #198.
Final CI #957 SUCCESS.
Merge `3425315d2a3f564f0f3f5beb15084fda214c3036`.

### B — Estate Campus Reachability v1

COMPLETE / DEPLOYED through PR #199.

Current private campus includes Mansion Exterior, Core Estate Grounds, Tactical Obstacle Course, Private Lake Access, Hidden Dock, Rear Forested Estate, Concealed Forest Passage, Main Estate Approach and Main Security Gate.

Ordinary traversal begins:
`Master Suite -> Grand Foyer -> Mansion Exterior -> Core Estate Grounds`.

Campus locations/fixtures feed the existing generic movement/action runtime. Darian can leave the mansion, use campus places/actions and return normally.

Final CI #959 SUCCESS.
Merge `f0955a582e11394ec64387f2a3fc0bfb468350b4`.
Deploy #245 / run `31936858504` SUCCESS.

### C — Spatial Familiarity Foundation v1

COMPLETE / DEPLOYED through PR #201.

The foundation adds explicit character-owned geographic knowledge without creating a general memory system.

Darian currently knows:
- normal represented home/interior and ordinary campus areas at `intimate` familiarity;
- Rear Forested Estate at `familiar`;
- Hidden Dock and Concealed Forest Passage as explicitly known concealed Estate facilities at `familiar`.

Cognition receives a compact broader known Estate map regardless of current one-hop position. Darian therefore need not physically reach the Foyer before reasoning that familiar campus destinations exist.

Important boundaries:
- exact move targets remain local deterministic `action_options`;
- unknown authored destinations are filtered from autonomous cognition move choices;
- generic one-hop previews omit globally concealed destinations;
- an actor who explicitly knows a concealed adjacent destination may still receive the legal exact move;
- familiarity does not alter objective topology;
- no automatic discovery, memory inference or forgetting exists yet.

Evidence:
- PR head `a77f9ec109ad7a161e8b5ca77688e84be79d2327`;
- CI #960 / run `31937649311` SUCCESS;
- Strength Live Cycle Validation #89 SUCCESS;
- merge `4778eb3e5fc0877ad49e7c96570f00ee5de4e121`;
- Deploy #246 / run `31937763776` SUCCESS, including sync, cognition configuration, restart and verification;
- schema remains v5.

No synthetic production Darian action was created solely for proof.

## Current world boundary

The represented world is the mansion plus bounded private Estate campus.

Outside continuation remains unavailable:
- Main Security Gate -> no public road edge;
- Concealed Forest Passage -> no Tahoe backcountry edge;
- Hidden Dock -> no water-travel edge;
- legacy Estate Exterior -> locked/non-traversable.

## Memory/discovery boundary

Spatial Familiarity v1 is not episodic character memory.

Future work may add validated discovery/revelation, lived familiarity changes, forgetting, map/teaching mechanics or general memory. That future layer must preserve the distinction between world truth, character knowledge and current action authority.

## South Lake Tahoe — PAUSED

Do not currently create or enable:
- public South Lake Tahoe regional graph;
- public-road continuation from Main Security Gate;
- Tahoe-backcountry continuation from Concealed Forest Passage;
- Hidden Dock water travel;
- public venue/economy/population loops merely because future contracts exist.

Outside-world expansion resumes only on separate Creator prioritization.

## Current verified runtime

Latest verified runtime deployment: **Deploy #246 / run `31937763776` SUCCESS**.

Runtime merge: `4778eb3e5fc0877ad49e7c96570f00ee5de4e121`.
Schema remains v5.

## Exact resume point

**Estate Campus Reachability v1 and Spatial Familiarity Foundation v1 are COMPLETE / DEPLOYED. Darian now has compact cognition access to his broader familiar Estate map from any represented Estate location while exact moves remain local/deterministic and unknown hidden spaces do not automatically leak into cognition. Keep all Tahoe/public/backcountry/water continuations locked. Resume by naturally observing Darian at the Creator-set 30x speed and checking real cognition/destination/multi-step movement/campus-use quality; fix only evidence-backed Estate-local gaps before considering any outside-world expansion.**
