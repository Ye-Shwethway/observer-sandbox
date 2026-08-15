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

Latest runtime deployment: **Deploy #221 / run `31889659349` SUCCESS**, Bladed Weapons Simulation-Safe Runtime v1, PR #152 merge `ce77b0a9a78684283c69daa3357df1dcd4d9aeb6`.

Final tested PR head: `44f70f8f9768665851858a16bc198c962d9b512a`.

Validation:
- **CI #902 / run `31889534085` SUCCESS**;
- full suite: **513 passed in 42.24s**;
- fresh DB init/status succeeded;
- schema remains v5;
- Skill Definition, Skill Application Requirements, Actor Skill Capability, Represented Skill Task, Cognition Capability Awareness, Technology, and Strength acceptance lanes passed.

Verified production readback after Deploy #221:
- service active/healthy; production init succeeded; schema v5;
- autonomy enabled, normal mode, **10x**, retry null, pending action present;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram bot/API/owner/allowed-user configuration healthy;
- live sim time was `2025-05-06T14:18:00+00:00`;
- Darian was naturally reading in the Living Room;
- Bladed Weapons remained 87/A, Firearms 87/A, Weapon Mastery 87/A, overall Skills A / 85.167;
- no production `blade_drill` or other weapon proof action was fabricated.

Exact application/outcome/evidence/no-XP behavior is CI/fresh-fixture evidence. Production deployment proves safe loading and runtime continuity only.

## Skill authority / ontology

- learned leaf/component `character_skills.score` = authoritative learned proficiency;
- `character_skills.experience` = legitimate accumulated learning evidence;
- derived parent Skills summarize components and are not independent learning/task authority;
- persisted `tier` = compatibility only;
- grade = read-time `skill-proficiency-100-v1`.

Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated reliability. Runtime application/consequence/lifecycle evidence is not automatically learning evidence.

### Weapon Mastery hierarchy

`Weapon Mastery` — derived parent
- `Bladed Weapons` — learned component
- `Firearms` — learned component

Rules:
- parent score = equal-weight mean of current component scores;
- parent has no direct progression and cannot authorize represented tasks;
- parent is excluded from overall Skills aggregation to prevent double-counting;
- historical `weapons = 87` initialized both components only as a compatibility baseline, not proof of distinct historical specialization measurements;
- existing component score/experience/learning state survives initialization;
- legacy `weapons` remains temporarily as hidden compatibility projection while old paths are retired;
- no deep knife/sword/handgun/rifle tree until simulation actually needs it.

### Bladed Weapons — represented application now active

`employ_familiar_melee_weapon` executable authority now belongs to `bladed_weapons`, not the hidden legacy `weapons` projection.

First represented task:
- `bladed_weapons_safe_handling_sim_v1`;
- action `blade_drill`;
- exact target `represented_task:bladed_weapons_safe_handling_simulator_v1`;
- Training Hall simulator requires exact capability `usable_bladed_training_weapon`;
- simulation-safe, low risk, solo-compatible;
- deterministic application evidence only;
- no separate cognitive/Attribute modifier contract is invented;
- no automatic XP or world-state harm mutation.

## Current Skills coverage

### Hand-to-Hand Combat
- represented controlled striking/grapple applications exist;
- progression exists through structured Training Method evidence;
- represented sparring requires a second distinct consenting colocated character;
- no injury/casualty production from controlled H2H;
- no H2H hierarchy rewrite during the current Weapon Mastery pass.

### Weapon Mastery / Bladed / Firearms
- hierarchy foundation complete;
- Bladed Weapons now has one simulation-safe represented application runtime;
- Bladed progression producer is still missing;
- Firearms represented runtime and progression remain missing;
- Weapon Mastery parent remains derived/non-executable;
- hostile use, lethality, injury, casualty generation, and automatic XP remain deferred.

### Survival
- represented field navigation/sustainment runtimes exist;
- explicit solo progression exists through `field_navigation_practice` and `field_sustainment_practice`;
- ordinary application does not automatically grant Survival XP.

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

1. **Bladed Weapons Progression Producer v1 — REVIEW NEXT / not yet implemented.**
2. Add one explicit simulation-safe Bladed practice/learning producer using the existing structured Skill progression machinery where possible.
3. Learning evidence must be explicit and whitelisted; ordinary `blade_drill` application evidence remains non-learning evidence.
4. Parent `weapon_mastery` must never receive direct XP; component learning re-derives the parent.
5. Preserve exact safe resource/target semantics and no harm/consumption side effects.
6. After Bladed application + progression is complete, apply the proven pattern to **Firearms Simulation-Safe Runtime v1** rather than creating another bespoke architecture.

## Deferred boundaries

No relationship system expansion, casualty handoff consumer, hostile/non-consensual Combat Engine, weapon lethality, broad casualty simulator, universal Hazard/Injury Engine, bleeding/wound taxonomy, definitive-treatment engine, random-accident scheduler, full Knowledge Engine, H2H hierarchy rewrite, deep weapon taxonomy, economy/jobs/quests, real-world weapon instructions, or synthetic production actors/actions solely for proof.

## Exact resume point

**Bladed Weapons Simulation-Safe Runtime v1 is complete through PR #152 final tested head `44f70f8f9768665851858a16bc198c962d9b512a`, merge `ce77b0a9a78684283c69daa3357df1dcd4d9aeb6`, CI #902 / run `31889534085` with 513 passing tests plus fresh-DB init/status and all relevant Skill/Cognition/Strength gates green, and Deploy #221 / run `31889659349` SUCCESS. `bladed_weapons` now owns executable `employ_familiar_melee_weapon` authority in an exact simulation-safe `blade_drill` task requiring `usable_bladed_training_weapon`; Weapon Mastery remains derived/non-executable, Firearms remains inactive, application evidence is non-learning, no XP or harm semantics were added, and no production proof action was forced. Review Bladed Weapons Progression Producer v1 next.**
