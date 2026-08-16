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

All Character Profile sections are minimum-unlocked v1. Skills remains CLOSED v1. Adaptive Character Disposition Foundation is COMPLETE v1. Overall Workflow/Foundation Review v1 is COMPLETE / CLOSED after Autonomy Intent Continuity, Active Modifier Runtime, Action Condition Runtime, and Participant-Aware Recent Event Context.

Character-side foundation depth is no longer the immediate expansion priority. Do not reopen psychology, Skills, relationships, memory, planning, modifiers, or action-condition depth merely because more detail is possible.

## World model baseline

`docs/WORLD_LOCATION_NODE_MODEL.md` remains the active spatial contract.

Current facts:
- locations are recursively nestable graph nodes;
- technical IDs are stable and globally scoped;
- `contains`, `connected_to`, `located_at`, ownership and possession remain distinct;
- routing derives from authored topology rather than hard-coded room pairs;
- the Thorne Estate interior is represented;
- `loc_thorne_estate_exterior_boundary` exists but is intentionally locked with no legal traversal edge;
- future South Lake Tahoe insertion is compatible with existing Estate identities.

The present outside-world limitation is therefore a world-content/runtime expansion boundary, not a reason to replace the spatial model.

## Active phase — World Foundation Expansion

Status: **DOCUMENTATION FIRST / IMPLEMENTATION NOT YET STARTED**.

### Canonical planning set

Read in this order for world-foundation work:
1. `docs/WORLD_FOUNDATION_EXPANSION_PLAN_V1.md` — program goals, WF-1 through WF-10 dependency order and global boundaries.
2. `docs/WORLD_LOCATION_NODE_MODEL.md` — existing active spatial identity/relation contract.
3. `docs/WORLD_SPATIAL_ACCESS_TRAVEL_CONTRACT_V1.md` — detailed WF-1/WF-2/WF-3 contract.
4. `docs/WORLD_GEOGRAPHY_EXPANSION_CONTRACT_V1.md` — detailed WF-4/WF-5 Estate/Tahoe geography contract.
5. `docs/WORLD_ENVIRONMENT_RUNTIME_CONTRACT_V1.md` — detailed WF-6 environment contract.
6. `docs/WORLD_VENUE_RESOURCE_CONTRACT_V1.md` — detailed WF-7/WF-8 venue/resource contract.
7. `docs/WORLD_POPULATION_ECONOMY_CONTRACT_V1.md` — detailed WF-9/WF-10 ambient population/economy contract.
8. `docs/WORLD_FOUNDATION_IMPLEMENTATION_SEQUENCE_V1.md` — future coding slices, acceptance milestones and coding-start gate.

These documents are planning authority. Their inclusion does not itself authorize runtime implementation or production mutation.

### Why this phase exists

Observer Sandbox now has enough character-side capability that further progress is constrained primarily by represented world substrate. Darian can reason and act within the current Estate interior, but Estate-campus and South Lake Tahoe autonomy cannot be safely opened while topology, access, route/travel semantics, environment, venues, distributed resources, population presence and basic world processes remain too thin.

### Planned foundation sequence

1. **WF-1 — World Spatial Hierarchy & Topology v1**
2. **WF-2 — Property, Place Classification & Access v1**
3. **WF-3 — Local Travel & Route Runtime v1**
4. **WF-4 — Thorne Estate Campus Expansion v1**
5. **WF-5 — South Lake Tahoe Regional Anchor v1**
6. **WF-6 — Environment / Daylight / Weather Foundation v1**
7. **WF-7 — Venue & Service Foundation v1**
8. **WF-8 — World Resource Distribution v1**
9. **WF-9 — Ambient Population / Presence v1**
10. **WF-10 — Basic World Economy v1**

Representation foundations precede living-world depth:
`space/topology -> access -> travel -> Estate campus -> regional opening -> environment -> venues/services -> resources -> ambient presence -> transactions`.

Do not jump directly to vehicles, traffic, deep economy, city-scale NPCs, jobs, law or institutions before the spatial/access/travel substrate is proven.

## Implementation milestones already planned

The detailed sequence defines five future phases:
- **Phase A — Representation Foundation:** WF-1 through WF-3.
- **Phase B — Usable Estate World:** WF-4; first milestone is Estate Campus Unlock while Tahoe remains locked.
- **Phase C — Regional Opening:** WF-5 plus the first bounded public destination; milestone is Outside World Unlock.
- **Phase D — Environment and Useful Places:** WF-6/WF-7.
- **Phase E — Resource and World-Process Loop:** WF-8/WF-9/WF-10.

Final minimum-program proof is an ordinary loop equivalent to:
`Estate resource shortage -> decide -> traverse Estate -> legally leave gate -> travel through bounded Tahoe -> reach open staffed venue -> obtain/purchase finite resource -> return -> persistent world consequences`.

Production does not need to be artificially manipulated to manufacture that proof.

## Key design locks

- Containment never implies traversal.
- Topology and access must both permit movement.
- Region existence does not make all real locations reachable.
- Real-world destinations enter the simulation only when authored for a concrete simulation use.
- First travel mode is walking; vehicles plug into the same route contract later.
- Estate campus should use meaningful nodes rather than architectural micromapping.
- South Lake Tahoe v1 is bounded, not an exhaustive real-city replica.
- Environment is authoritative world state, not prompt prose.
- Venue capabilities are machine-readable but do not themselves mutate state.
- Resource location, ownership, carriage and quantity remain distinct.
- Named characters and ambient population are separate tiers.
- Basic economy is authoritative balance/price/transaction state, not macroeconomics.

## World-scale cognition rule

World growth must not make cognition context scale linearly with world size.

Cognition receives only a bounded decision-relevant projection:
- current location and immediate parent context;
- legal adjacent/reachable destinations relevant now;
- local access/opening/environment state;
- task-relevant venue/resource facts;
- active travel context when in transit.

Full regional graphs, catalogs, inventories, population ledgers and transaction histories remain deterministic/query-layer data.

## Recently completed Creator features

Telegram Cognition Context Inspector v1: COMPLETE / DEPLOYED through PR #187 / Deploy #240.

Cognition Context Efficiency v1: COMPLETE / DEPLOYED / CLOSED through PR #191, CI #954 with 613 passing tests, merge `25d709ddc0cc36d7d7ba30a3e0f7357ce1348dd6`, Deploy #243 SUCCESS.

Do not resume speculative context trimming without new measured evidence.

## Current verified deployment

Latest runtime deployment remains **Deploy #243 / run `31931381264` SUCCESS**, schema v5.

World Foundation Expansion planning is docs-only and has made no runtime/schema/production world change.

## Deferred depth / non-goals for the minimum world pass

Do not build merely for completeness:
- full GIS or street-by-street Tahoe reproduction;
- detailed traffic/public transit;
- vehicle/fuel/maintenance depth before travel foundations;
- meteorological/climate simulation;
- macroeconomics, taxes, banking or labor markets;
- city-scale population of LLM agents;
- law/crime/trespass engine;
- broad institutional simulation;
- universal permission/expression language;
- universal hazard/injury engine;
- synthetic production world events solely for proof.

## Exact resume point

**World Foundation Expansion is the active strategic phase and remains documentation-first. The detailed contract set for WF-1 through WF-10 and the future implementation sequence are now defined. No world implementation or production unlock is authorized yet. The next discussion should refine concrete authored content that cannot be decided purely at engine-contract level—especially exact Estate campus geography, the first bounded South Lake Tahoe public destination/connector set, and the first environment/venue/resource loop—then obtain Creator approval before sustained coding. Latest verified runtime remains Deploy #243 at schema v5.**