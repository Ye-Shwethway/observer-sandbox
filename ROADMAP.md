# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-15

## Operating principles

- Current Creator instruction, current canonical repo contracts/config/schema, and verified live production outrank remembered chat context.
- AI proposes structured cognition; deterministic runtime validates and mutates.
- Telegram is observer/control, never simulation authority.
- Preserve: `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Never manipulate production merely to manufacture evidence.

## Current development direction

The active roadmap is **profile-first**: make Character Profile sections meaningfully participate in simulation before expanding relationship or broader multi-character systems.

Current focus: **Skills**.

Relationship-oriented expansion and casualty handoff/lifecycle-end work remain deferred until additional represented-character work resumes.

## Current verified deployment

Latest runtime deployment: **Deploy #220 / run `31886986845` SUCCESS**, Weapon Mastery Skill Hierarchy Foundation v1, PR #150 merge `d2616db5cf08e496b66c3f939ae3b2dcbf1560c4`.

Final tested PR head: `d4c23e77e24d6a7f6c75146b78ecab81be34d662`.

Validation:
- **CI #894 / run `31886921670` SUCCESS**;
- full suite: **506 passed in 41.06s**;
- fresh DB init/status succeeded;
- schema remains v5;
- Cognition Capability Awareness, Skill Progression, Skill Evidence, Grading, Strength, Inventory, and Technology acceptance lanes passed.

Verified production readback after Deploy #220:
- service active/healthy; production init succeeded; schema v5;
- autonomy enabled, normal mode, 1x, retry null, pending action present;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram bot/API/owner/allowed-user configuration healthy;
- live sim time was `2025-05-06T10:48:00+00:00`;
- Darian was naturally eating in the Kitchen;
- no production weapon action, practice, target, casualty, or harm event was fabricated for proof.

Production `init` executed the hierarchy reconciliation safely. Exact parent/component migration, derivation, profile projection, cognition projection, and idempotency are CI/fresh-DB evidence; the deploy workflow did not separately dump the live `character_skills` hierarchy rows.

## Skill authority / ontology

- learned leaf/component `character_skills.score` = authoritative learned proficiency;
- `character_skills.experience` = legitimate accumulated learning evidence;
- derived parent Skills summarize their components and are not independent learning/task authority;
- persisted `tier` = compatibility only;
- grade = read-time `skill-proficiency-100-v1`.

Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated reliability. Runtime application/consequence/lifecycle evidence is not automatically learning evidence.

### Weapon Mastery hierarchy

The historical flat `Weapons` gameplay meaning is replaced by:

`Weapon Mastery` — derived parent
- `Bladed Weapons` — learned component
- `Firearms` — learned component

V1 rules:
- parent score = equal-weight mean of current component scores;
- parent has no direct progression and cannot authorize represented tasks;
- parent is excluded from overall Skills aggregation to prevent double-counting;
- historical `weapons = 87` initializes both components only as an explicit compatibility baseline, not proof of distinct historical specialization measurements;
- existing component score/experience/learning state is preserved across initialization;
- legacy `weapons` remains temporarily as a hidden compatibility projection while old definition paths are retired;
- profile and cognition expose the canonical hierarchy, not the hidden legacy projection;
- no weapon runtime or XP path was activated by the hierarchy foundation.

Do not create a giant knife/sword/handgun/rifle tree until simulation actually needs deeper disciplines.

## Current Skills coverage

### Hand-to-Hand Combat
- represented controlled striking/grapple applications exist;
- progression exists through structured Training Method evidence;
- represented sparring currently requires a second distinct consenting colocated character;
- no injury/casualty production from controlled H2H;
- do not refactor H2H into independently scored Striking/Grappling during the current Weapon Mastery pass.

### Weapon Mastery
- hierarchy foundation complete;
- Bladed Weapons and Firearms are learned component authorities;
- historical melee/ranged `weapons` applications remain compatibility definition semantics only until explicitly moved to the component Skills;
- represented weapon runtime is still missing;
- component progression producers are still missing;
- hostile use, lethality, injury, casualty generation, and automatic XP remain deferred.

### Survival
- represented field navigation/sustainment runtimes exist;
- explicit solo progression exists through `field_navigation_practice` and `field_sustainment_practice`;
- ordinary obstacle-course/application evidence does not automatically grant Survival XP.

### Tactical Planning
- represented assessment/maneuver-planning runtimes and structured progression exist.

### Technology
- represented known-fault diagnostic runtime and explicit `systems_diagnostic_practice` progression exist.

### Field Medicine
- read-only casualty assessment and bounded stabilization runtimes exist;
- both require represented casualty context;
- progression and casualty lifecycle-end continuation remain deferred.

## Preserved casualty foundation

`typed represented fall -> casualty lifecycle state -> read-only Field Medicine assessment -> optional bounded stabilization -> explicit lifecycle-end event required for clear`

Risk reaching zero does not auto-clear and does not assert healing. No Injury Engine, wound taxonomy, diagnosis engine, definitive treatment, death/incapacity, random accidents, or automatic Field Medicine XP is implied.

## Next development sequence

1. **Bladed Weapons Simulation-Safe Runtime v1 — REVIEW NEXT / not yet implemented.**
2. Reconcile the historical `employ_familiar_melee_weapon` application semantics and move represented application authority onto `bladed_weapons` rather than the hidden legacy umbrella.
3. Add the smallest solo-usable represented training/simulation context with an exact safe target and exact represented bladed-weapon resource capability.
4. Parent `weapon_mastery` must remain non-executable; capability resolution must use `bladed_weapons`.
5. Keep application evidence separate from learning evidence; safe application must not automatically award Bladed Weapons XP.
6. No hostile target, lethality, injury, casualty generation, non-consensual combat, or broad Combat/Injury Engine.
7. After one safe Bladed Weapons application invariant is proven, review **Bladed Weapons Progression Producer v1**.
8. Once the shared invariant is proven, apply the pattern to **Firearms** rather than creating a second bespoke architecture.

## Deferred boundaries

No relationship system expansion, casualty handoff consumer, hostile/non-consensual Combat Engine, weapon lethality, broad casualty simulator, universal Hazard/Injury Engine, bleeding/wound taxonomy, definitive-treatment engine, random-accident scheduler, full Knowledge Engine, H2H hierarchy rewrite, deep weapon taxonomy, economy/jobs/quests, or synthetic production actors/targets solely for proof.

## Exact resume point

**Weapon Mastery Skill Hierarchy Foundation v1 is complete through PR #150 final tested head `d4c23e77e24d6a7f6c75146b78ecab81be34d662`, merge `d2616db5cf08e496b66c3f939ae3b2dcbf1560c4`, CI #894 / run `31886921670` with 506 passing tests plus fresh-DB init/status and relevant acceptance lanes green, and Deploy #220 / run `31886986845` SUCCESS. `Weapon Mastery` is now a derived non-executable parent over learned `Bladed Weapons` and `Firearms`; legacy `weapons=87` is used only as a documented compatibility baseline/projection, existing child learning state is preserved, profile/cognition are hierarchy-aware, and no weapon runtime or XP was activated. Review Bladed Weapons Simulation-Safe Runtime v1 next.**
