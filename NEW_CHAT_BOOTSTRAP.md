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

**Human Memory Dynamics v1 is COMPLETE / DEPLOYED.**

Latest runtime evidence:
- PR #212 — `Add Human Memory Dynamics v1`
- final tested head: `1cad8d9188e49f42f9c00b8026eccd917a9fc073`
- CI #980 / run `31950039890`: SUCCESS
- Strength Live Cycle Validation #102: SUCCESS
- Inventory Foundation Acceptance #65: SUCCESS
- Skill Evidence Semantics Acceptance #51: SUCCESS
- Skill Progression Foundation Acceptance #68: SUCCESS
- Technology Diagnostic Task Runtime Acceptance #42: SUCCESS
- Attribute Grading Batch 1 Acceptance #50: SUCCESS
- Read-Only Grading Proof Acceptance #51: SUCCESS
- Solo Regulation Naturalism v2 Acceptance #49: SUCCESS
- merge: `b8343d12b5204a0f3a049cbfb7632b617df77495`
- Deploy #253 / run `31950111179`: SUCCESS
- deployment verification (`sync -> install/configure cognition -> restart -> verify`): SUCCESS
- schema: **v7**

`main` and `test` are synchronized at the runtime merge before this docs-only continuity checkpoint.

## Required cognition / memory / world read order

1. `docs/HUMAN_MEMORY_DYNAMICS_V1.md`
2. `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
3. `docs/UNIVERSAL_CHARACTER_AUTONOMY_CONTRACT_V1.md`
4. `docs/WORLD_SPATIAL_FAMILIARITY_CONTRACT_V1.md`
5. `docs/WORLD_OUTDOOR_SPATIAL_AFFORDANCE_CONTRACT_V1.md`
6. task-relevant canonical docs/source only.

## Universal autonomy invariant

Character-specific authoring may seed represented facts/state, but must not command future behavior.

Forbidden:
- named-character autonomy prompts/policies;
- bespoke daily routines or time-window activity preferences;
- named-character destination/activity steering;
- anti-repetition or behavior-correction counter-prompts written for one character;
- identity-keyed behavior branches.

Autonomous behavior must emerge from universal systems consuming represented profile/state, needs/physiology, time, environment, affordances, goals, relationships, currently recallable memories/learning, recent history and deterministic constraints.

## Character Memory architecture

Preserve four distinct layers:
1. **World/event truth** — objective represented facts and completed events.
2. **Character memory trace** — what an actor encoded or is initialized to know, plus its current strength/detail/lifecycle.
3. **Retrieved cognition context** — bounded memories that are currently recallable/relevant.
4. **Current action authority** — exact deterministic actions/targets executable now.

Canonical rule:
`stored memory != currently recallable memory != world truth != action authority`.

### Foundation / spatial migration status

Character Memory Foundation v1 and Semantic Spatial Memory Migration are both deployed.

Spatial knowledge now lives in generic semantic Character Memory. `config/characters/darian.spatial_familiarity.v1.json` has been removed. Familiarity remains `unknown -> aware -> familiar -> intimate`; hidden/secret status remains orthogonal.

Known-world cognition is separately projected from semantic spatial memory. Generic relevant-memory retrieval surfaces spatial familiarity rows only when the current represented location directly cues them, preventing map knowledge from crowding episodic recall.

## Human Memory Dynamics v1

Canonical contract:
`docs/HUMAN_MEMORY_DYNAMICS_V1.md`

Lifecycle:
`experience -> recent -> consolidation -> consolidated/remote -> possible fading -> cue-driven recall/reinforcement`

Dynamic state:
- `memory_strength` — gist/accessibility strength;
- `detail_strength` — contextual-detail strength;
- `emotional_arousal`;
- `personal_relevance`;
- `consolidated_sim_time`;
- `last_dynamics_sim_time`.

Important rules:
- forgetting weakens accessibility/precision; it does not delete event truth;
- represented sleep acts as a chronological consolidation boundary;
- emotional significance may preserve gist better than exact details;
- faded traces remain stored and can be reactivated by strong represented cues;
- successful recall provides bounded reinforcement;
- retrieval is deterministic in v1;
- false memories, clinical psychiatric simulation, dreams, detailed sleep-stage modeling and vector memory are not implemented.

## Memory Ability profile

Character Profile now contains `🧩 Memory Ability` with four independent 0..100 traits:
- Working Memory
- Encoding
- Retention
- Recall

These are character facts, not Skills or behavioral scripts, and are not directly derived from IQ.

Current Darian factual seed:
- Working Memory 86
- Encoding 89
- Retention 84
- Recall 91

Runtime uses one character-generic profile contract. Do not create identity-keyed memory formulas.

## Telegram observability

Current Character surfaces include:
- `📖 Profile`
- `🗃️ Memory`
- owner-only `🧠 Cognition Context`

Memory view is live/read-only and shows Active/Episodic/Knowledge plus Recent/Long-term/Faded counts, lifecycle stage, Strength, Detail, salience, confidence, recall count and represented entity associations.

Observability distinction:
- **Memory** — stored actor-owned traces and knowledge with current dynamic state.
- **Cognition Context** — what was actually injected for a particular model decision.

Telegram never mutates, restores, deletes or force-recalls memories.

## Estate / simulation boundary

Estate-first foundation remains the active world scope. South Lake Tahoe/public/backcountry/water expansion is still intentionally paused.

Outside continuation remains unavailable:
- Main Security Gate -> no public road edge;
- Concealed Forest Passage -> no Tahoe backcountry edge;
- Hidden Dock -> no water-travel edge;
- legacy Estate Exterior -> locked/non-traversable.

## Behavioral observation context

The unresolved higher-level observations remain:
- local indoor actions can win repeatedly over purposeful use of known outdoor Estate destinations;
- training can recur daily because no true multi-day intention/planning layer exists yet.

Do **not** fix these with Darian-specific rules, fixed rest days, outdoor quotas or scripted schedules.

Human Memory Dynamics now provides a more realistic substrate for future planning, but it is not itself a planner.

## Exact resume point

**STOP before implementing Minimal Mind / Planning. The Creator explicitly wants further architecture discussion after Human Memory Dynamics deployment. Reconcile the live deployed M3 state first, discuss remaining memory/mind/planning questions, and only implement P0 after explicit direction. Preserve universal behavior and the current Estate boundary.**
