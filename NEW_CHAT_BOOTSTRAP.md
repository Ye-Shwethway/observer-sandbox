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

All Character Profile sections are minimum-unlocked v1. Skills remains CLOSED v1. Adaptive Character Disposition Foundation and Overall Workflow/Foundation Review v1 remain COMPLETE / CLOSED.

Character-side foundation depth is no longer the immediate priority. The current bottleneck is world substrate: the represented world remains largely limited to the Thorne Estate interior, while the canonical Estate exterior boundary is intentionally locked because no sufficiently represented outside world exists yet.

## Active phase — World Foundation Expansion

Status: **DOCUMENTATION FIRST / IMPLEMENTATION NOT YET STARTED**.

### Required world-planning read order

1. `docs/WORLD_FOUNDATION_EXPANSION_PLAN_V1.md`
2. `docs/WORLD_LOCATION_NODE_MODEL.md`
3. `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md`
4. `docs/WORLD_GEOGRAPHY_EXPANSION_CONTRACT_V1.md`
5. `docs/WORLD_ENVIRONMENT_RUNTIME_CONTRACT_V1.md`
6. `docs/WORLD_VENUE_RESOURCE_CONTRACT_V1.md`
7. `docs/WORLD_POPULATION_ECONOMY_CONTRACT_V1.md`
8. `docs/WORLD_FOUNDATION_IMPLEMENTATION_SEQUENCE_V1.md`

Task-relevant runtime/source should be read only when implementation is later authorized.

### Phase intent

Build the world foundations required to expand autonomous life from the mansion into the Estate campus and eventually a bounded South Lake Tahoe region, without prompt-only geography or world-state invention.

Preserve:
- recursively nestable location graph;
- stable globally scoped entity IDs;
- `contains` != `connected_to` != `located_at` != ownership/possession;
- deterministic route/access/world-state authority;
- LLM proposes actions but cannot invent legal topology, access, weather, prices, resources or authoritative world facts;
- cognition receives only a decision-relevant local world projection, never the entire regional graph/catalog.

### Planned WF sequence

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

Detailed implementation order is already planned as Phase A representation foundation, Phase B Estate Campus Unlock, Phase C Outside World Unlock, Phase D environment/useful places, and Phase E resource/population/economy loop.

### Key planning locks

- Containment does not imply traversal.
- Topology and access must both allow movement.
- First travel mode is walking.
- Estate campus unlock comes before Tahoe public-world unlock.
- South Lake Tahoe v1 is intentionally bounded, not a full map replica.
- Public destinations are admitted only for concrete simulation use.
- Environment is authoritative state, not decorative prompt prose.
- Venue/service/resource/population/economy systems reuse generic world contracts rather than parallel bespoke engines.
- Named agents and ambient population remain separate tiers.
- World growth must not make model context grow with total world size.

### Planning-only boundary

Current documentation does not authorize runtime implementation or production mutation.

Until explicit implementation authorization:
- keep `loc_thorne_estate_exterior_boundary` locked;
- create no traversable Estate-exterior/public edge;
- do not fabricate production travel for proof;
- do not implement weather/economy/vehicles/population out of sequence;
- continue refining concrete authored world content.

## Next discussion targets

Engine-level contracts for WF-1 through WF-10 are now sufficiently explicit for planning. Remaining high-value documentation questions are content decisions rather than generic engine architecture:
1. exact Thorne Estate campus nodes, adjacency and canon/provisional geography;
2. first bounded South Lake Tahoe public connector and destination set;
3. first environment-state representation and deterministic consumer hook;
4. first venue/service/resource loop, with grocery/resource acquisition as the leading candidate;
5. any real-world Tahoe source policy/detail required for those chosen destinations.

After these are settled, the Creator may decide whether documentation is complete enough to authorize the consecutive coding sequence.

## World baseline already present

`docs/WORLD_LOCATION_NODE_MODEL.md` remains an ACTIVE CONTRACT. It already supports recursive world expansion, scoped IDs, generic `location_runtime`, relation-derived routing and future insertion of `loc_south_lake_tahoe` above the Estate without renaming current identities.

The current Estate exterior remains a locked boundary with no legal movement edge.

## Recently completed Creator features

Telegram Cognition Context Inspector v1: COMPLETE / DEPLOYED through PR #187 / Deploy #240.

Cognition Context Efficiency v1: COMPLETE / DEPLOYED / CLOSED through PR #191, CI #954 with 613 passing tests, merge `25d709ddc0cc36d7d7ba30a3e0f7357ce1348dd6`, Deploy #243 SUCCESS.

Do not continue speculative cognition-context trimming without new measured evidence.

## Current verified deployment

Latest runtime deployment remains **Deploy #243 / run `31931381264` SUCCESS**, schema v5.

World Foundation Expansion planning has made no runtime/schema/production change.

## Development boundaries

- LLM proposes; deterministic runtime validates/mutates.
- Do not reopen closed character/profile/psychology foundations merely for depth.
- Prefer representation before simulation depth.
- Reuse existing generic entity/relation/location/action/resource contracts before adding schema.
- Do not create mansion-only runtime shortcuts that block regional expansion.
- No full GIS, city-scale LLM NPC population, detailed traffic/transit, climate simulation, macroeconomy, law/crime, universal permission language, universal injury/hazard engine, or synthetic production world events merely for completeness.

## Exact resume point

**The active phase is World Foundation Expansion, documentation-first. The canonical contract set now covers WF-1 through WF-10 plus a low-drift future implementation sequence. No implementation or production world unlock has started. Continue by settling concrete Estate-campus geography, the first bounded Tahoe connector/destination set, and the first environment/venue/resource loop. Only after those content decisions are sufficiently documented should sustained coding be authorized. Latest verified runtime remains Deploy #243 at schema v5.**