# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-16

## Operating principles

- Current Creator instruction, canonical repo contracts/config/schema, and verified live production outrank remembered chat context.
- AI proposes structured cognition; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Preserve: `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Prefer **vertical completeness before local depth**.
- Never manipulate production merely to manufacture evidence.
- Verification is focused-first. Code/runtime PRs get one final full CI checkpoint by default; docs-only changes do not need the Python suite.

## Character-side checkpoint

All Character Profile sections are minimum-unlocked v1. Skills remains CLOSED v1.

Adaptive Character Disposition Foundation is COMPLETE v1:
`Habit Formation/Extinction -> Hobby/Interest Lifecycle -> Preference Adaptation -> Slow Personality Plasticity`.

The Overall Workflow/Foundation Review v1 is COMPLETE / CLOSED. Four evidence-selected cross-system gaps were closed:
1. Autonomy Intent Continuity v1 — PR #178 / Deploy #236.
2. Active Modifier Runtime Foundation v1 — PR #180 / Deploy #237.
3. Action Condition Runtime Foundation v1 — PR #182 / Deploy #238.
4. Participant-Aware Recent Event Context v1 — PR #184 / Deploy #239.

Character-side foundation depth is no longer the immediate expansion priority. Do not reopen psychology, Skills, relationships, memory, planning, modifiers, or action-condition depth merely because more detail is possible.

## Skills — CLOSED v1

Frozen learned Skill surface:
- Hand-to-Hand Combat
- Bladed Weapons
- Firearms
- Survival
- Tactical Planning
- Technology
- Field Medicine

`Weapon Mastery` is derived/non-executable; hidden legacy `weapons` is compatibility only.

## World model baseline

`docs/WORLD_LOCATION_NODE_MODEL.md` remains the active world/location contract.

Current minimum facts:
- locations are recursively nestable graph nodes;
- technical IDs are stable and globally scoped;
- `contains`, `connected_to`, `located_at`, ownership and possession semantics remain distinct;
- routing derives from authored topology rather than hard-coded room pairs;
- the Thorne Estate interior is represented;
- `loc_thorne_estate_exterior_boundary` exists but is intentionally locked and has no legal traversal edge;
- future South Lake Tahoe insertion is already compatible with existing identities.

This means the present outside-world limitation is a world-content/runtime expansion boundary, not a reason to replace the current spatial model.

## Active phase — World Foundation Expansion

Status: **DOCUMENTATION FIRST / IMPLEMENTATION NOT YET STARTED**.

Canonical planning authority:
- `docs/WORLD_FOUNDATION_EXPANSION_PLAN_V1.md`
- `docs/WORLD_LOCATION_NODE_MODEL.md`

### Why this phase exists

Observer Sandbox now has enough character-side capability that further progress is increasingly constrained by the represented world. Darian can reason and act within the current Estate interior, but Estate-campus and South Lake Tahoe autonomy cannot be safely opened while topology, access, route/travel semantics, environment, venues, distributed resources, population presence and basic world processes remain too thin.

The next priority is therefore world substrate rather than additional character depth.

### Documentation-first policy

Before sustained coding:
- settle world-system dependency order;
- document minimum-runnable contracts and explicit non-goals;
- refine Estate-campus geography and public-world source policy;
- define cognition projections so world growth does not cause prompt growth proportional to world size;
- keep the existing deterministic/LLM authority boundary explicit.

Inclusion in the plan does **not** authorize implementation by itself. No Estate exterior edge, outside-world travel, weather/economy runtime or production world mutation is authorized during planning-only work.

### Planned foundation sequence

1. **WF-1 — World Spatial Hierarchy & Topology v1**
   - extend the existing recursive graph for outdoor/property/road/public nodes;
   - retain stable IDs and explicit legal traversal;
   - first structural exemplar: Mansion -> Estate campus boundary path.

2. **WF-2 — Property, Place Classification & Access v1**
   - private/public/residential/business/outdoor/connector place semantics;
   - ownership/residency distinct from current location;
   - deterministic access/open/locked/restricted state.

3. **WF-3 — Local Travel & Route Runtime v1**
   - origin, route, destination, travel mode and represented duration;
   - walking/property traversal first;
   - no teleportation or prompt-only route authority.

4. **WF-4 — Thorne Estate Campus Expansion v1**
   - source-supported/Creator-approved outdoor property nodes;
   - candidate grounds, garden, pool, tennis court, driveway, security gate and justified paths;
   - exit goal: autonomous mansion <-> campus movement without opening Tahoe yet.

5. **WF-5 — South Lake Tahoe Regional Anchor v1**
   - add the anticipated regional parent and first bounded public connectors;
   - create an explicit Estate gate -> represented public-world boundary only when implementation is authorized.

6. **WF-6 — Environment / Daylight / Weather Foundation v1**
   - local time/daylight, ambient temperature, bounded weather state, outdoor exposure;
   - consequential deterministic hooks, not decorative prompt prose.

7. **WF-7 — Venue & Service Foundation v1**
   - category, location, access/opening state, hours, services/resources;
   - bounded Tahoe exemplars rather than exhaustive city authoring.

8. **WF-8 — World Resource Distribution v1**
   - authoritative location/ownership/quantity/availability;
   - depletion/replenishment hooks;
   - reuse existing inventory/item-effect foundations.

9. **WF-9 — Ambient Population / Presence v1**
   - persistent named characters remain full agents;
   - lightweight staff/patron/pedestrian/crowd presence avoids one-LLM-agent-per-person scaling.

10. **WF-10 — Basic World Economy v1**
    - balances/prices/payment/resource transfer and auditable transaction consequences;
    - no macroeconomic simulation in the minimum pass.

### Representation before living-world depth

Representation foundations come first:
`space/topology -> access -> travel -> campus/region -> environment/place/resource representation`.

Living-world processes follow:
`schedules -> services -> replenishment/depletion -> ambient presence -> transactions -> later weather/transport/economic depth`.

Do not jump directly to weather, vehicles, economy, city-scale NPCs, jobs, law, traffic or institutions before the spatial/access/travel substrate is settled.

### World-scale cognition rule

World growth must not make every cognition prompt contain the whole world.

Cognition should receive only a bounded decision-relevant projection such as:
- current location and immediate parent context;
- legal adjacent/reachable destinations relevant now;
- local access/opening/environment state;
- task-relevant resources/services;
- active travel context when in transit.

Full regional graphs, venue catalogs, resource registries and ambient population state remain deterministic/query-layer data and are retrieved only when relevant.

## Recently completed Creator features

### Telegram Cognition Context Inspector v1

COMPLETE / DEPLOYED through PR #187, CI #950 with 605 passing tests, merge `c1ee61ad335ea3fd37509e868c8b406e20d714b7`, Deploy #240 SUCCESS.

### Cognition Context Efficiency v1

COMPLETE / DEPLOYED / CLOSED through PR #191, final tested head `b4febc29ad7ba37d67547346abd5bb9fff73b772`, CI #954 with 613 passing tests, merge `25d709ddc0cc36d7d7ba30a3e0f7357ce1348dd6`, Deploy #243 SUCCESS.

Measured pre-compaction production baseline: 66,952 full-prompt characters and 64,575 runtime-context characters. The compaction targeted duplicate capability/training metadata while preserving deterministic/runtime semantics. Do not resume speculative context trimming without new measured evidence.

## Current verified deployment

Latest runtime deployment: **Deploy #243 / run `31931381264` SUCCESS**, Cognition Context Efficiency v1.

Verified deployment evidence:
- runtime merge `25d709ddc0cc36d7d7ba30a3e0f7357ce1348dd6` deployed;
- install/configure/restart/verify completed successfully;
- production cognition-context audit execution succeeded;
- schema remains v5;
- no schema migration or synthetic production cognition call was required for that slice.

The World Foundation Expansion planning phase is docs-only and does not supersede this runtime deployment until implementation is separately authorized, merged and deployed.

## Deferred depth / non-goals for the minimum world pass

Do not build merely for completeness:
- giant planner/task graph;
- universal episodic memory or witness engine;
- city-scale population of LLM agents;
- full GIS or street-by-street Tahoe reproduction;
- detailed traffic/public-transit simulation;
- vehicle/fuel/maintenance depth before travel foundations;
- meteorological/climate simulation;
- macroeconomics, taxes, banking or labor-market simulation;
- crime/law/trespass engine;
- broad institutional simulation;
- universal permissions/expression language;
- universal hazard/injury engine;
- synthetic production travel/world events solely for proof.

These remain later features if concrete user-visible goals justify them.

## Exact resume point

**World Foundation Expansion is now the active strategic phase, documentation-first. Character-side minimum foundations remain closed enough for the current purpose; the immediate bottleneck is represented world substrate. `docs/WORLD_FOUNDATION_EXPANSION_PLAN_V1.md` defines the planned WF-1 -> WF-10 sequence, beginning with spatial hierarchy/topology, property/access and local travel before Estate-campus and South Lake Tahoe expansion. No world implementation or production unlock is authorized yet. Continue logical discussion/documentation and refine the world contracts/roadmap before beginning sustained coding. Latest verified runtime remains Deploy #243 at schema v5.**