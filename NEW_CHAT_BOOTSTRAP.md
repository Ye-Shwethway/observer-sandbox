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

The Estate-first sequence is complete/deployed through **Estate Campus Reachability v1**, **Spatial Familiarity Foundation v1**, and **Outdoor Spatial Affordance Cognition v1**. South Lake Tahoe remains intentionally paused.

A later architecture correction is also COMPLETE / DEPLOYED: **Universal Character Autonomy v1** removes the named Darian autonomy-policy layer. Character-specific behavioral hard-coding is now forbidden.

## Required world / cognition read order

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
11. `docs/UNIVERSAL_CHARACTER_AUTONOMY_CONTRACT_V1.md`

## Universal autonomy invariant

Character-specific authoring may seed represented facts/state, but must not command future behavior.

Forbidden:
- named-character autonomy prompts;
- bespoke daily routines or time-window activity preferences;
- named-character destination/activity preferences encoded as policy;
- anti-repetition or behavior-correction counter-prompts written for one character;
- character-specific behavior branches merely to make observation look better.

Autonomous behavior must emerge from universal systems consuming represented character profile/state, needs/physiology, time, environment, affordances, recent history, goals, relationships, memory/learning when available, and deterministic constraints.

`config/autonomy/universal.autonomy-policy.v1.json` is the shared cognition policy. `config/characters/darian.autonomy-policy.json` no longer exists and character registry entries no longer select an autonomy policy.

## Location semantic rule

A location is not a dimensionless point.

Canonical definition:
`location = identifiable nested spatial container with extent, contents, boundaries/interfaces, local state, control and explicit relationships to surrounding space`

The graph node is the stable identity/hierarchy/topology representation of that container.

## Spatial knowledge rule

Keep three layers distinct:
1. **World truth** — represented objective geography/topology.
2. **Character-known world** — the subset of geography an actor knows.
3. **Current actionable space** — exact deterministic moves/actions executable now.

Spatial familiarity vocabulary:
`unknown -> aware -> familiar -> intimate`.

Hidden/secret is orthogonal to familiarity. Known geography supports planning but never grants teleportation, permission or a non-local target. Exact movement authority remains current `action_options`.

### Temporary spatial-familiarity debt

`config/characters/darian.spatial_familiarity.v1.json` is retained only as a temporary factual bootstrap because the general Memory System / discovery-learning layer does not yet own initial and evolving spatial knowledge.

When the general Memory System is implemented:
1. migrate valid initial spatial knowledge into the generic memory/knowledge initialization model;
2. preserve world truth vs actor knowledge vs current action authority;
3. let discovery/familiarity reinforcement/forgetting evolve through universal systems where supported;
4. remove `darian.spatial_familiarity.v1.json` and any Darian-specific loader/path dependency;
5. do not replace it with another named-character cognition-policy file.

Until then this seed may contain factual initial knowledge only, never behavioral instructions.

## Outdoor-lived-space rule

Reachability alone does not make an outdoor location behaviorally meaningful.

`world.spatial_container.affordances` is the deterministic source for ordinary location-level activity. V1 supports:
- `walk` — within the current container; does not change `located_at`;
- `relax` — quiet/decompression activity, weaker recovery than dedicated `rest`;
- `observe` — spend time taking in represented surroundings without inventing facts.

Current Estate lifestyle destinations are Mansion Exterior, Core Estate Grounds, Private Lake Access and Rear Forested Estate. These are generic world affordances; they must not be converted into Darian-specific outing instructions.

Outdoor attraction is soft and never a quota. Tactical Obstacle Course remains training-oriented; Main Estate Approach remains transit-oriented; Hidden Dock, Concealed Forest Passage and Main Security Gate are not lifestyle-attraction destinations.

## Completed Estate-first sequence

- **A0 Location Spatial Container Contract v1** — PR #196 / merge `d1167771ddb9c358a464c6efb863d9edf6800e18`.
- **A1 Existing Estate Location Refactor** — PR #197 / merge `886001a1d5d1cc62e5e9aab26a64fc08dedf08f1` / Deploy #244 SUCCESS.
- **A2 Gameplay Runtime Reconnection / Regression** — PR #198 / merge `3425315d2a3f564f0f3f5beb15084fda214c3036` / final CI #957 SUCCESS.
- **B Estate Campus Reachability v1** — PR #199 / merge `f0955a582e11394ec64387f2a3fc0bfb468350b4` / Deploy #245 run `31936858504` SUCCESS.
- **C Spatial Familiarity Foundation v1** — PR #201 / merge `4778eb3e5fc0877ad49e7c96570f00ee5de4e121` / Deploy #246 run `31937763776` SUCCESS.
- **D Outdoor Spatial Affordance Cognition v1** — PR #204 / merge `14c48908bfefaf7509249cddafe3eb30c5ef0623` / CI #963 SUCCESS / Strength #91 SUCCESS / Deploy #248 run `31940047281` SUCCESS.

## Universal Character Autonomy v1

COMPLETE / DEPLOYED through PR #206.

Key results:
- removed `config/characters/darian.autonomy-policy.json`;
- removed character-registry autonomy-policy binding;
- added one character-agnostic `config/autonomy/universal.autonomy-policy.v1.json`;
- existing policy-loading compatibility path now returns the universal policy and rejects character binding;
- removed Darian-specific morning-training acceptance behavior;
- removed Darian-specific lean/muscular nutrition-policy expectation;
- added `docs/UNIVERSAL_CHARACTER_AUTONOMY_CONTRACT_V1.md` and locked the invariant in `AGENTS.md`;
- explicitly recorded the Darian spatial-familiarity seed as temporary Memory System migration debt.

Validation history:
- initial full-CI failures were stale tests still expecting the removed Darian policy identity/nutrition goal, not runtime regressions;
- final PR head `ddc94714b6e78f1b6a3b640aa04f86116893920a`;
- CI #966 / run `31941715382` SUCCESS;
- Strength Live Cycle Validation #94 / run `31941715379` SUCCESS;
- merge `133b2cf987768ffbf2263abb2ac1c7b086ea7aed`;
- Deploy #249 / run `31941781006` SUCCESS;
- schema remains v5.

## Current world boundary

The represented world is the mansion plus bounded private Estate campus.

Outside continuation remains unavailable:
- Main Security Gate -> no public road edge;
- Concealed Forest Passage -> no Tahoe backcountry edge;
- Hidden Dock -> no water-travel edge;
- legacy Estate Exterior -> locked/non-traversable.

## South Lake Tahoe — PAUSED

Do not currently create or enable public South Lake Tahoe topology, road continuation, Tahoe-backcountry continuation, Hidden Dock water travel, or public venue/economy/population loops without separate Creator prioritization.

## Current verified runtime

Latest verified runtime deployment: **Deploy #249 / run `31941781006` SUCCESS**.

Runtime merge: `133b2cf987768ffbf2263abb2ac1c7b086ea7aed`.
Schema remains v5.

## Exact resume point

**Observe Darian naturally at the Creator-set 30x speed under Universal Character Autonomy v1. Do not tune him through named-character policy or counter-prompts. If Gym/Training Hall fixation or another behavioral imbalance persists, inspect universal inputs/signals/competition and fix only evidence-backed generic causes. Preserve the Estate world boundary and keep South Lake Tahoe/public/backcountry/water continuations paused. The Darian-specific spatial-familiarity seed remains temporary factual bootstrap debt and must be migrated/removed when the general Memory System lands.**
