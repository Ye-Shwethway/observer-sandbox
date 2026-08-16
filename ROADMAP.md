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
- **Character-specific behavioral hard-coding is forbidden.** Character-specific authoring may seed represented facts/state; autonomous behavior must emerge from universal systems.

## Character-side checkpoint

Character Profile minimum foundations, Skills v1, Adaptive Character Disposition Foundation and Overall Workflow/Foundation Review v1 remain closed enough for the current purpose. Character-side depth is not the immediate priority.

**Universal Character Autonomy v1 is COMPLETE / DEPLOYED.** The former Darian-specific autonomy-policy layer has been removed. A new character must not require a new autonomy prompt, bespoke daily routine, destination preference policy, or character-specific behavior branch.

Canonical autonomy contract:
`docs/UNIVERSAL_CHARACTER_AUTONOMY_CONTRACT_V1.md`

Canonical direction:
`character seed/state + needs/physiology + time + environment + affordances + recent history + goals + relationships + memory/learning + deterministic constraints -> universal cognition -> proposed action -> deterministic validation/mutation`

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
11. `docs/UNIVERSAL_CHARACTER_AUTONOMY_CONTRACT_V1.md`

## Universal autonomy semantic lock

Character-specific files may define facts such as identity, body/profile, personality traits, biography, initial Skills, relationships, possessions, preferences/hobbies, initial habits, or factual initial knowledge. They must not tell the runtime what that named character should do next.

Forbidden patterns include:
- named-character autonomy policies/prompts;
- fixed character-specific morning/evening activity schedules;
- named-character destination/activity preference instructions;
- behavior-specific counter-prompts added because observation is undesirable;
- bespoke code branches that steer a named character toward or away from an activity.

Generic world affordances and universal soft signals are valid. Their effect on a particular character must be derived from represented character/world state rather than identity-specific policy prose.

Current universal policy:
`config/autonomy/universal.autonomy-policy.v1.json`

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

World geography and character knowledge are separate authoritative layers:
1. **World truth** — what represented locations/topology objectively exist.
2. **Character-known world** — what represented geography this actor knows.
3. **Current actionable space** — exact actions/moves the deterministic runtime permits now.

Spatial familiarity levels are:
`unknown -> aware -> familiar -> intimate`.

Hidden/secret status is orthogonal to familiarity. Known geography is planning knowledge only. It never grants teleportation, access permission, or a non-local target. Exact executable moves remain authoritative only when present in current `action_options`.

### Memory migration debt

`config/characters/darian.spatial_familiarity.v1.json` is explicitly temporary. It exists only because the general Memory System / discovery-learning layer does not yet own initial and evolving spatial knowledge.

When that system lands:
- migrate valid initial spatial knowledge into the generic memory/knowledge initialization model;
- preserve world truth vs actor-known world vs current action authority;
- make discovery/familiarity reinforcement/forgetting universal where supported;
- remove `darian.spatial_familiarity.v1.json` and Darian-specific loader/path dependencies;
- do not replace it with another named-character cognition-policy file.

Until migration, this seed is factual initial knowledge only and must contain no behavioral instructions.

## Outdoor-lived-space semantic lock

A reachable outdoor node is not automatically a meaningful lived destination.

`world.spatial_container.affordances` authors ordinary location-level activity. V1 generic activities are `walk`, `relax` and `observe`.

Preserve:
- `walk` is activity within the current container, not inter-location travel;
- `move` remains authoritative for changing `located_at`;
- outdoor attraction is a soft choice signal, never a quota;
- dedicated indoor `rest` remains a stronger recovery option than ordinary outdoor `relax`;
- known outdoor lifestyle destinations may appear in planning cognition while exact execution stays local;
- security/egress/utility nodes must not become recreation defaults merely because they are outdoors;
- no weather/daylight/safety facts may be invented before environment runtime represents them;
- outdoor affordances must not be converted into Darian-specific behavior instructions.

Current Estate lifestyle destinations are Mansion Exterior, Core Estate Grounds, Private Lake Access and Rear Forested Estate. Tactical Obstacle Course remains training-oriented; Main Estate Approach remains transit-oriented; Hidden Dock, Concealed Forest Passage and Main Security Gate are not lifestyle-attraction destinations.

## Completed Estate-first implementation

- **A0 — Location Spatial Container Contract v1** — PR #196 / merge `d1167771ddb9c358a464c6efb863d9edf6800e18`.
- **A1 — Existing Estate Location Refactor** — PR #197 / merge `886001a1d5d1cc62e5e9aab26a64fc08dedf08f1` / Deploy #244 SUCCESS.
- **A2 — Gameplay Runtime Reconnection / Regression** — PR #198 / merge `3425315d2a3f564f0f3f5beb15084fda214c3036` / CI #957 SUCCESS.
- **B — Estate Campus Reachability v1** — PR #199 / merge `f0955a582e11394ec64387f2a3fc0bfb468350b4` / Deploy #245 run `31936858504` SUCCESS.
- **C — Spatial Familiarity Foundation v1** — PR #201 / merge `4778eb3e5fc0877ad49e7c96570f00ee5de4e121` / Deploy #246 run `31937763776` SUCCESS.
- **D — Outdoor Spatial Affordance Cognition v1** — PR #204 / merge `14c48908bfefaf7509249cddafe3eb30c5ef0623` / CI #963 SUCCESS / Strength #91 SUCCESS / Deploy #248 run `31940047281` SUCCESS.

## Universal Character Autonomy v1 — COMPLETE / DEPLOYED

PR #206 corrected an architectural violation in the prior cognition layer.

Implemented:
- deleted `config/characters/darian.autonomy-policy.json`;
- removed the character-registry autonomy-policy selector;
- introduced shared `config/autonomy/universal.autonomy-policy.v1.json` with no character binding;
- compatibility policy loading now resolves to the shared universal policy;
- removed Darian-specific morning-training behavior acceptance;
- removed Darian-specific lean/muscular nutrition-policy expectation;
- added architecture contract and AGENTS invariant;
- recorded spatial-familiarity seed as future Memory System migration debt.

Validation:
- final PR head `ddc94714b6e78f1b6a3b640aa04f86116893920a`;
- CI #966 / run `31941715382` SUCCESS;
- Strength Live Cycle Validation #94 / run `31941715379` SUCCESS;
- merge `133b2cf987768ffbf2263abb2ac1c7b086ea7aed`;
- Deploy #249 / run `31941781006` SUCCESS;
- schema remains v5.

The earlier CI failures during PR #206 were stale test expectations still asserting the removed Darian policy identity and Darian-specific nutrition goal, not runtime defects.

## Current simulation boundary

The represented world is the mansion plus bounded private Thorne Estate campus.

Outside continuations remain absent:
- Main Security Gate has no public-road edge;
- Concealed Forest Passage has no Tahoe-backcountry edge;
- Hidden Dock has no water-travel edge;
- legacy Estate Exterior remains locked/non-traversable.

## South Lake Tahoe — intentionally PAUSED

Do not currently add or enable public South Lake Tahoe topology, outward Main Gate road connection, Tahoe-backcountry connection, Hidden Dock water travel, or public venue/economy/population loops without separate Creator prioritization.

## World-scale cognition rule

World growth must not make cognition context scale blindly with world size.

Use a compact actor-relative projection:
`current executable space + relevant local previews + compact known geography + task-relevant context`.

Do not serialize the entire objective world into each model call.

## Current verified deployment

Latest verified runtime deployment: **Deploy #249 / run `31941781006` SUCCESS**, runtime merge `133b2cf987768ffbf2263abb2ac1c7b086ea7aed`.

Schema remains v5.

## Exact resume point

**Observe Darian naturally at the Creator-set 30x speed under Universal Character Autonomy v1. Do not tune him through named-character prompts/policies. If Gym/Training Hall fixation or another behavioral imbalance remains, diagnose the universal competition inputs—profile/state, physiology, recent training/repetition pressure, world affordances, time/circadian context, history and future memory/learning—and fix only generic evidence-backed causes. Keep South Lake Tahoe/public/backcountry/water expansion paused. When the general Memory System is implemented, migrate and remove `darian.spatial_familiarity.v1.json`.**
