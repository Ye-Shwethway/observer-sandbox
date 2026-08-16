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

**Character Memory Foundation v1 is COMPLETE / DEPLOYED.**

Evidence:
- PR #209
- final tested head `0a59bb2e24a30eca81144935e5631019e947c5bc`
- CI #972 / run `31948233699`: SUCCESS
- Inventory Foundation Acceptance #59: SUCCESS
- Attribute Grading Batch 1 Acceptance #44: SUCCESS
- Read-Only Grading Proof Acceptance #45: SUCCESS
- merge `516414a1a6b1d5471206145e11c30407515398cc`
- Deploy #251 / run `31948315106`: SUCCESS
- schema v6

## Completed foundation stack

The current minimum foundation is deployed through:
- Character Profile / Skills minimum foundations;
- adaptive dispositions/habits/preferences/personality foundations;
- Estate spatial-container and reachability foundation;
- Spatial Familiarity Foundation v1;
- Outdoor Spatial Affordance Cognition v1;
- Universal Character Autonomy v1;
- Universal action satiation / movement-cycle shaping;
- **Character Memory Foundation v1**.

South Lake Tahoe remains intentionally paused.

## Memory architecture lock

Canonical contract:
`docs/CHARACTER_MEMORY_FOUNDATION_V1.md`

Preserve:
`event/world truth != actor memory != retrieved cognition context != current action authority`

V1 memory provides:
- `episodic` and `semantic` actor-owned records;
- source-event provenance;
- associated represented entities/locations;
- automatic compact episodic encoding for new completed actions;
- bounded actor-scoped retrieval;
- recency + salience + local/action relevance ranking;
- dynamic recall metadata;
- live Telegram Character → Memory observability.

Current lifecycle:
`experience -> encode -> retrieve -> recall metadata`

Deferred until evidence justifies them:
- consolidation/reflection;
- reconsolidation;
- forgetting/fading/retirement policy;
- vector/embedding retrieval;
- full daily/weekly planning.

Do not simulate deferred capabilities with arbitrary timers or character-specific prompt instructions.

## Universal autonomy semantic lock

A character-specific source may define factual identity/profile, biography, initial skills, possessions, relationships, preferences/hobbies, factual goals or factual initial knowledge.

It may not define future behavior scripts such as:
- named autonomy prompts/policies;
- fixed daily routines or training schedules;
- named-character destination preferences;
- bespoke anti-repetition counter-prompts;
- identity-keyed code branches.

Generic cognition derives behavior from represented state:
`profile + needs/physiology + time + environment + affordances + goals + relationships + relevant memories/learning + recent context + deterministic constraints`.

## World / spatial lock

A location is an identifiable nested spatial container with extent, contents, boundaries/interfaces, local state, control and explicit relationships to surrounding space.

Preserve:
- `contains` = structural containment;
- `connected_to` = traversable topology;
- `located_at` = dynamic presence;
- known geography != executable movement;
- hidden/secret status is orthogonal to familiarity.

Spatial familiarity vocabulary remains:
`unknown -> aware -> familiar -> intimate`.

Current lifestyle destinations include Mansion Exterior, Core Estate Grounds, Private Lake Access and Rear Forested Estate. Outdoor attraction is soft, never a quota.

Current outside boundary remains closed:
- no public-road edge from Main Security Gate;
- no Tahoe-backcountry edge from Concealed Forest Passage;
- no water-travel edge from Hidden Dock;
- legacy Estate Exterior remains locked/non-traversable.

## Active phase — Memory integration → Minimal Mind / Planning

### M2 — Semantic Spatial Memory Migration — NEXT

Goal: remove the remaining named-character spatial-familiarity bootstrap debt now that generic Character Memory exists.

Required:
1. map valid existing spatial-familiarity facts into generic semantic memory/knowledge initialization;
2. preserve familiarity vocabulary and concealed/secret knowledge;
3. preserve world truth vs actor knowledge vs current action authority;
4. make the bootstrap path character-generic;
5. prove existing known-world cognition/reachability behavior remains equivalent;
6. remove `config/characters/darian.spatial_familiarity.v1.json`;
7. remove Darian-specific familiarity loader/path dependencies.

Not in scope:
- Tahoe expansion;
- automatic forgetting policy;
- full planner;
- character-specific behavior steering.

### P0 — Minimal Mind / Planning Foundation — AFTER M2

Create a small persistent intention/planning layer above local action selection.

Target flow:
`profile/state + physiology + environment/affordances + goals + relevant memories -> bounded intention/plan -> local authoritative action execution`

Planning must be adaptive, not a scripted calendar. It must remain interruptible by needs, safety and deterministic action constraints.

### P1 — First Planning Consumers

Use the shared planning foundation for two observed gaps:

**Multi-day training/recovery balance**
- consume recent training memories/history, recovery/readiness/adaptation and goals;
- allow recovery-oriented days to emerge naturally;
- do not encode fixed named rest days or athlete schedules.

**Purposeful destination + activity planning**
- allow cognition to form intentions such as destination plus activity across known Estate space;
- use represented affordances/resources only;
- do not force outdoor quotas or invent unavailable activities/resources.

Example distinction:
- `relax -> Private Lake Access` may be planned if represented and reachable;
- `read outdoors` requires an actual represented readable resource/affordance and must not be invented merely because an outdoor location exists.

## Telegram observability direction

Keep observability alongside each cognition subsystem rather than bolting it on later.

Current Character surfaces:
- `📖 Profile` — represented character data;
- `🧠 Memory` — live actor-owned memory/knowledge;
- Creator-only `🧠 Cognition Context` — actual model injection snapshots.

Future planning should receive a similarly read-only observer surface once the planning representation is stable enough to inspect.

## Current exact resume point

**Implement M2 — Semantic Spatial Memory Migration next. Do not yet build a large Mind System. Once named spatial-familiarity bootstrap debt is removed and generic semantic memory is proven, implement the smallest useful P0 planning foundation, then evaluate the two first planning consumers against live observation. Preserve universal behavior, schema/runtime/Telegram observability, and the current Estate boundary.**
