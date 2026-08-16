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

## Current canonical checkpoint

**Character Memory Foundation v1 is COMPLETE / DEPLOYED.**

Runtime evidence:
- PR #209 — `Add Character Memory Foundation v1`
- final tested PR head: `0a59bb2e24a30eca81144935e5631019e947c5bc`
- CI #972 / run `31948233699`: SUCCESS
- Inventory Foundation Acceptance #59: SUCCESS
- Attribute Grading Batch 1 Acceptance #44: SUCCESS
- Read-Only Grading Proof Acceptance #45: SUCCESS
- merge: `516414a1a6b1d5471206145e11c30407515398cc`
- Deploy #251 / run `31948315106`: SUCCESS
- deployment verification (`sync -> install/configure cognition -> restart -> verify`): SUCCESS
- schema: **v6**

`main` and `test` are synchronized at the runtime merge before this docs-only continuity checkpoint.

## Required cognition / world read order

1. `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
2. `docs/UNIVERSAL_CHARACTER_AUTONOMY_CONTRACT_V1.md`
3. `docs/WORLD_SPATIAL_FAMILIARITY_CONTRACT_V1.md`
4. `docs/WORLD_OUTDOOR_SPATIAL_AFFORDANCE_CONTRACT_V1.md`
5. `docs/ESTATE_CAMPUS_REACHABILITY_V1.md`
6. `docs/THORNE_ESTATE_CAMPUS_CANON_MAP_V1.md`
7. other task-relevant canonical docs/source only.

## Universal autonomy invariant

Character-specific authoring may seed represented facts/state, but must not command future behavior.

Forbidden:
- named-character autonomy prompts/policies;
- bespoke daily routines or time-window activity preferences;
- named-character destination/activity steering;
- anti-repetition or behavior-correction counter-prompts written for one character;
- identity-keyed behavior branches.

Autonomous behavior must emerge from universal systems consuming represented profile/state, needs/physiology, time, environment, affordances, goals, relationships, memories/learning, recent history and deterministic constraints.

`config/autonomy/universal.autonomy-policy.v1.json` remains the shared policy. No character selects a bespoke autonomy policy.

## Character Memory Foundation v1

Canonical contract:
`docs/CHARACTER_MEMORY_FOUNDATION_V1.md`

Preserve four distinct layers:
1. **World / event truth** — objective represented facts and completed events.
2. **Character memory / knowledge** — what an actor has encoded or is initialized to know.
3. **Retrieved cognition context** — bounded memories relevant to a present decision.
4. **Current action authority** — exact deterministic actions/targets executable now.

Canonical rule:
`Events say what happened. Memory says what this actor retained or knows. Cognition retrieves only what is relevant. Action options remain execution authority.`

V1 runtime:
- actor-owned `episodic` and `semantic` memory schema;
- new completed actions automatically encode compact episodic memories exactly once;
- provenance links memory to its source event;
- memory/entity associations support location/target relevance;
- retrieval is character-scoped and bounded (default top 8 for cognition);
- initial ranking combines recency, salience, current-location association and available-action relevance;
- cognition receives `relevant_memories` but memories never grant action/topology/resource authority;
- only memories actually retrieved into normal captured cognition increment `recall_count` / `last_recalled_sim_time`;
- vector DB, consolidation, forgetting and full planning are intentionally deferred until evidence justifies them.

Dynamic lifecycle currently implemented:
`experience -> encode -> retrieve -> recall metadata`

Future lifecycle extension points:
`reinforcement -> consolidation -> reconsolidation -> fading/retirement`

Do not fake those future stages with arbitrary timers.

## Telegram Character Memory UX

Character view now includes a live read-only `🧠 Memory` surface alongside Profile; Creator-only Cognition Context remains separate.

Memory view provides:
- live active / episodic / semantic counts;
- latest encoded simulation time;
- All / Episodes / Knowledge filters;
- pagination;
- memory time, summary, salience, confidence, recall count and related represented entities.

Observability distinction:
- **Memory**: what this character currently remembers/knows.
- **Cognition Context**: what was actually injected for a specific model decision.

Use both when diagnosing behavior: first verify a memory exists, then verify retrieval selected it, then inspect the resulting decision.

## Spatial knowledge rule and remaining migration debt

Keep distinct:
1. world truth;
2. character-known world;
3. current actionable space.

Spatial familiarity vocabulary remains:
`unknown -> aware -> familiar -> intimate`.

`config/characters/darian.spatial_familiarity.v1.json` **still exists temporarily**. Character Memory Foundation v1 did not remove it yet.

Next bounded memory migration must:
1. migrate valid initial spatial knowledge into generic semantic-memory initialization;
2. preserve concealed/secret knowledge independently from familiarity;
3. preserve world truth vs actor knowledge vs action authority;
4. verify equivalent cognition/reachability behavior;
5. remove `darian.spatial_familiarity.v1.json` and any Darian-specific loader/path dependency;
6. never replace it with another named-character cognition/behavior file.

## Estate / simulation boundary

Estate-first foundation remains deployed through:
- Estate Campus Reachability v1;
- Spatial Familiarity Foundation v1;
- Outdoor Spatial Affordance Cognition v1;
- Universal Character Autonomy v1;
- Character Memory Foundation v1.

Current Estate lifestyle destinations include Mansion Exterior, Core Estate Grounds, Private Lake Access and Rear Forested Estate. `walk`, `relax` and `observe` are generic represented outdoor affordances; they are not quotas or Darian-specific outing instructions.

Outside continuation remains unavailable:
- Main Security Gate -> no public road edge;
- Concealed Forest Passage -> no Tahoe backcountry edge;
- Hidden Dock -> no water-travel edge;
- legacy Estate Exterior -> locked/non-traversable.

South Lake Tahoe/public/backcountry/water expansion remains intentionally paused.

## Behavioral observation context

Recent production observation exposed two longer-horizon gaps:
- local indoor actions often win over purposeful use of known Estate outdoor destinations;
- training can recur daily even though current load/readiness systems lack a true multi-day planning layer.

Do **not** fix either symptom with Darian-specific rules, fixed rest days, outdoor quotas or character schedules.

Memory Foundation is the substrate for later planning, not the planner itself.

## Exact resume point

**Next minimum bounded implementation: migrate the temporary spatial-familiarity bootstrap into generic semantic Character Memory and remove the named Darian familiarity file/path after equivalence is proven. Then design a Minimal Mind / Planning Foundation that consumes profile/state + physiology + environment/affordances + goals + relevant memories to form short/medium-term intentions. First planning consumers should be multi-day training/recovery balance and purposeful destination+activity selection. Keep all behavior character-agnostic and preserve the Estate boundary.**
