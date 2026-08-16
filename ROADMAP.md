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

## Current production checkpoint

**Human Memory Dynamics v1 is COMPLETE / DEPLOYED.**

Evidence:
- PR #212
- final tested head `1cad8d9188e49f42f9c00b8026eccd917a9fc073`
- CI #980 / run `31950039890`: SUCCESS
- all triggered acceptance gates on the final head: SUCCESS
- merge `b8343d12b5204a0f3a049cbfb7632b617df77495`
- Deploy #253 / run `31950111179`: SUCCESS
- final install/configure cognition/restart/verify: SUCCESS
- schema v7

## Completed foundation stack

The current minimum foundation is deployed through:
- Character Profile / Skills minimum foundations;
- adaptive dispositions/habits/preferences/personality foundations;
- Estate spatial-container and reachability foundation;
- Outdoor Spatial Affordance Cognition v1;
- Universal Character Autonomy v1;
- Universal action satiation / movement-cycle shaping;
- Character Memory Foundation v1;
- Semantic Spatial Memory Migration;
- **Human Memory Dynamics v1**.

South Lake Tahoe remains intentionally paused.

## Memory architecture lock

Canonical docs:
- `docs/CHARACTER_MEMORY_FOUNDATION_V1.md`
- `docs/HUMAN_MEMORY_DYNAMICS_V1.md`

Preserve:
`event/world truth != actor memory trace != currently recalled cognition context != current action authority`

### Memory Foundation

Provides:
- actor-owned episodic and semantic records;
- source-event provenance;
- represented entity/location associations;
- automatic compact episodic encoding for completed actions;
- bounded actor-scoped retrieval;
- Telegram Memory observability.

### Semantic spatial migration

Spatial familiarity is now generic semantic Character Memory. The old named Darian familiarity file/path has been removed.

Known-world projection remains separate from current executable movement. Generic recall does not flood cognition with all known-map rows; spatial semantic memories become generic recall candidates only under direct represented location cue.

### Human Memory Dynamics v1

Lifecycle:
`experience -> recent -> consolidation -> consolidated/remote -> fading possible -> cue recall/reinforcement`

Dynamic trace model includes:
- memory strength;
- detail strength;
- emotional arousal;
- personal relevance;
- consolidation time;
- last dynamics settlement time.

Forgetting is simulation-time based and weakens accessibility/precision rather than deleting event truth. Represented sleep provides a consolidation boundary. Emotion/significance may protect gist more strongly than exact detail. Strong represented cues may make a faded trace accessible again. Successful recall gives bounded reinforcement.

The v1 model is deterministic and intentionally small. It is not a literal neurological or clinical model.

## Memory Ability profile

Character Profile contains a separate `Memory Ability` domain:
- Working Memory
- Encoding
- Retention
- Recall

Memory ability is not directly derived from IQ and is not automatically a Skill.

Darian's current factual seed through the shared generic memory-profile contract:
- Working Memory 86
- Encoding 89
- Retention 84
- Recall 91

No memory runtime behavior may branch on character identity.

## Universal autonomy semantic lock

A character-specific source may define factual identity/profile, biography, initial skills, possessions, relationships, preferences/hobbies, factual goals or factual initial knowledge.

It may not define future behavior scripts such as:
- named autonomy prompts/policies;
- fixed daily routines or training schedules;
- named-character destination preferences;
- bespoke anti-repetition counter-prompts;
- identity-keyed code branches.

Generic cognition derives behavior from represented state:
`profile + needs/physiology + time + environment + affordances + goals + relationships + currently recallable memories/learning + recent context + deterministic constraints`.

## World / spatial lock

A location is an identifiable nested spatial container with extent, contents, boundaries/interfaces, local state, control and explicit relationships to surrounding space.

Preserve:
- `contains` = structural containment;
- `connected_to` = traversable topology;
- `located_at` = dynamic presence;
- known geography != executable movement;
- hidden/secret status is orthogonal to familiarity.

Current outside boundary remains closed:
- no public-road edge from Main Security Gate;
- no Tahoe-backcountry edge from Concealed Forest Passage;
- no water-travel edge from Hidden Dock;
- legacy Estate Exterior remains locked/non-traversable.

## Telegram observability

Current Character surfaces:
- `📖 Profile`
- `🗃️ Memory`
- owner-only `🧠 Cognition Context`

`🧩 Memory Ability` is available inside Profile.

Memory view dynamically exposes lifecycle/strength/detail state while Cognition Context remains the actual model-injection inspector. Telegram is read-only for memory state.

## Deferred memory depth

Do not silently add these while working on planning:
- false-memory fabrication;
- clinical trauma/PTSD simulation;
- dream generation or detailed sleep-stage modeling;
- semantic reflection/consolidation from repeated episodes;
- procedural memory;
- vector/embedding retrieval;
- stochastic recall unless deterministic behavior proves inadequate.

They require separate evidence and scope decisions.

## Candidate next phase — Minimal Mind / Planning

### P0 — Minimal Mind / Planning Foundation — DISCUSSION ONLY

Candidate flow:
`present state + profile/traits + physiology + environment/affordances + goals + currently recallable memories -> bounded intention/plan -> local authoritative action execution`

The planner must not receive perfect memory-database access. `stored != currently recallable` is now a hard prerequisite.

Potential first consumers remain:

**Multi-day training/recovery balance**
- recent recalled training experience/history + authoritative load/readiness/adaptation + goals;
- recovery-oriented days can emerge without fixed rest-day schedules.

**Purposeful destination + activity planning**
- represented destination plus represented activity/resource;
- no outdoor quota and no invented resource/action.

However, **P0 is not authorized yet**. The Creator explicitly wants further discussion after M3 deployment.

## Current exact resume point

**Human Memory Dynamics v1 is deployed. Stop implementation and discuss the remaining memory/mind/planning architecture with the Creator before starting P0. Do not solve outdoor use or daily training recurrence through character-specific rules. Preserve the current Estate boundary.**
