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

Docs-only planning work does not require the Python suite or runtime deploy. Use exemplar-first only for genuinely new invariants, then batch structurally equivalent follow-ons.

## Strategic checkpoint

All Character Profile sections are minimum-unlocked v1. Skills remains CLOSED v1.

Adaptive Character Disposition Foundation is COMPLETE v1:
`Habit Formation/Extinction -> Hobby/Interest Lifecycle -> Preference Adaptation -> Slow Personality Plasticity`.

Overall Workflow/Foundation Review v1 remains COMPLETE / CLOSED. Its four evidence-selected closures remain:
1. Autonomy Intent Continuity v1 — PR #178 / Deploy #236.
2. Active Modifier Runtime Foundation v1 — PR #180 / Deploy #237.
3. Action Condition Runtime Foundation v1 — PR #182 / Deploy #238.
4. Participant-Aware Recent Event Context v1 — PR #184 / Deploy #239.

Character-side foundation depth is no longer the immediate priority. The current bottleneck is world substrate: the represented world remains largely limited to the Thorne Estate interior, while the canonical Estate exterior boundary is intentionally locked because no sufficiently represented outside world exists yet.

## Active phase — World Foundation Expansion

Status: **DOCUMENTATION FIRST / IMPLEMENTATION NOT YET STARTED**.

Read:
- `docs/WORLD_FOUNDATION_EXPANSION_PLAN_V1.md`
- `docs/WORLD_LOCATION_NODE_MODEL.md`
- task-relevant world/action/resource source only when implementation is later authorized.

### Phase intent

Build the world foundations required to expand autonomous life from the mansion into the Estate campus and eventually a bounded South Lake Tahoe region, without falling back to prompt-only geography or world-state invention.

Preserve:
- recursively nestable location graph;
- stable globally scoped entity IDs;
- `contains` != `connected_to` != `located_at` != ownership/possession;
- deterministic route/access/world-state authority;
- LLM proposes actions but cannot invent legal topology, access, weather, prices, resources or other authoritative world facts;
- cognition receives only a decision-relevant local world projection, never the entire regional graph/catalog.

### Planned documentation/implementation sequence

1. WF-1 — World Spatial Hierarchy & Topology v1
2. WF-2 — Property, Place Classification & Access v1
3. WF-3 — Local Travel & Route Runtime v1
4. WF-4 — Thorne Estate Campus Expansion v1
5. WF-5 — South Lake Tahoe Regional Anchor v1
6. WF-6 — Environment / Daylight / Weather Foundation v1
7. WF-7 — Venue & Service Foundation v1
8. WF-8 — World Resource Distribution v1
9. WF-9 — Ambient Population / Presence v1
10. WF-10 — Basic World Economy v1

Representation foundations precede living-world depth. Do not jump to vehicles, traffic, economy depth, city-scale agents, law, jobs or institutions before spatial/access/travel foundations are settled.

### Planning-only boundary

Current documentation does not authorize runtime implementation or production mutation.

Until explicit implementation authorization:
- keep `loc_thorne_estate_exterior_boundary` locked;
- create no traversable Estate-exterior/public edge;
- do not fabricate production travel for proof;
- do not implement weather/economy/vehicles/population out of sequence;
- continue refining milestone contracts, Estate-campus geography, regional source policy and cognition/query boundaries.

## World baseline already present

`docs/WORLD_LOCATION_NODE_MODEL.md` is an ACTIVE CONTRACT and already supports the expansion direction:
- locations are graph nodes rather than hard-coded screen names;
- the model can insert `loc_south_lake_tahoe` above `loc_thorne_estate` without renaming existing Estate identities;
- `src/observer_sandbox/location_runtime.py` is the generic dynamic-location boundary;
- routing derives from authored `connected_to` relations;
- current Estate interior nodes and objects use scoped identities;
- Estate exterior is recorded as a locked boundary with no legal movement edge.

The new World Foundation Expansion plan extends this model rather than replacing it.

## Recently completed Creator features

### Telegram Cognition Context Inspector v1

COMPLETE / DEPLOYED through PR #187, CI #950 with 605 passing tests, merge `c1ee61ad335ea3fd37509e868c8b406e20d714b7`, Deploy #240 SUCCESS.

### Cognition Context Efficiency v1

COMPLETE / DEPLOYED / CLOSED through PR #191:
- final tested head `b4febc29ad7ba37d67547346abd5bb9fff73b772`;
- CI #954 SUCCESS, 613 passed;
- merge `25d709ddc0cc36d7d7ba30a3e0f7357ce1348dd6`;
- Deploy #243 / run `31931381264` SUCCESS.

Measured pre-compaction baseline was 66,952 full-prompt characters / 64,575 runtime-context characters. Do not continue speculative context trimming without new measured evidence.

## Current verified deployment

Latest runtime deployment remains **Deploy #243 / run `31931381264` SUCCESS**.

Verified evidence:
- runtime merge `25d709ddc0cc36d7d7ba30a3e0f7357ce1348dd6` deployed;
- install/configure/restart/verify succeeded;
- production cognition-context audit execution succeeded;
- schema v5;
- World Foundation Expansion planning has made no runtime/schema/production change.

## Development boundaries

- LLM proposes; deterministic runtime validates/mutates.
- Do not reopen closed character/profile/psychology foundations merely for depth.
- Do not infer that a future world system must be built deeply just because it appears in the planning map.
- Prefer representation before simulation depth.
- Reuse existing generic entity/relation/location/action/resource contracts before adding schema.
- Do not create mansion-only runtime shortcuts that block regional expansion.
- No full GIS, city-scale LLM NPC population, detailed traffic/transit, climate simulation, macroeconomy, law/crime, universal permission language, universal injury/hazard engine, or synthetic production world events merely for completeness.

## Exact resume point

**The active phase is World Foundation Expansion, documentation-first. `docs/WORLD_FOUNDATION_EXPANSION_PLAN_V1.md` is the planning authority and defines WF-1 through WF-10, beginning with spatial hierarchy/topology, property/access and local travel before Estate-campus and South Lake Tahoe unlock. `docs/WORLD_LOCATION_NODE_MODEL.md` remains the active spatial contract. No implementation or production world unlock has started. Continue logical discussion/documentation until the near-term world roadmap is sufficiently explicit for a consecutive coding phase with low architectural drift. Latest verified runtime remains Deploy #243 at schema v5.**