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

The active roadmap is **profile-first**. Current Character Profile focus: **Skills**.

Relationship-oriented expansion and casualty handoff/lifecycle-end work remain deferred until additional represented-character work resumes.

## Current verified deployment

Latest runtime deployment: **Deploy #222 / run `31890490349` SUCCESS**, Bladed Weapons Progression Producer v1, PR #154 merge `11ee97f093c7bc5a7439742f3f691f87b6b915de`.

Final tested PR head: `148884966ded63559806101cffbeb891efbe96dd`.

Validation:
- **CI #908 / run `31890299802` SUCCESS**;
- full suite: **518 passed in 191.64s**;
- fresh DB init/status succeeded; schema remains v5;
- Skill Progression, Skill Evidence, Skill Definition, Tactical Planning, and Strength acceptance lanes passed;
- post-merge **CI #909 / run `31890490342` SUCCESS**.

Verified production readback after Deploy #222:
- service active/healthy; production init succeeded; schema v5;
- autonomy enabled, normal mode, **10x**, retry null, pending action present;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram bot/API/owner/allowed-user configuration healthy;
- live sim time was `2025-05-06T17:18:00+00:00`;
- Darian was naturally resting in Darian's Master Suite;
- Bladed Weapons remained 87/A, Firearms 87/A, Weapon Mastery 87/A, overall Skills A / 85.167;
- no production `practice`, `blade_drill`, or other weapon proof action was fabricated.

The unchanged production score is expected: initialization activates Bladed progression with a zero-gain bootstrap. Exact score gain, evidence consumption, hierarchy re-derivation, and no-application-XP behavior are CI/fresh-fixture evidence.

## Skill authority / ontology

- learned leaf/component `character_skills.score` = authoritative learned proficiency;
- `character_skills.experience` = legitimate accumulated learning evidence;
- derived parent Skills summarize components and are not independent learning/task authority;
- persisted `tier` = compatibility only;
- grade = read-time `skill-proficiency-100-v1`.

Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated reliability. Runtime application evidence is not automatically learning evidence.

### Weapon Mastery hierarchy

`Weapon Mastery` — derived parent
- `Bladed Weapons` — learned component
- `Firearms` — learned component

Rules:
- parent score = equal-weight mean of current component scores;
- parent has no direct progression and cannot authorize represented tasks;
- parent is excluded from overall Skills aggregation;
- historical `weapons = 87` initialized both components only as a compatibility baseline;
- legacy `weapons` remains a hidden compatibility projection;
- component learning immediately re-derives the parent and legacy projection without granting either direct XP;
- no deep knife/sword/handgun/rifle tree until simulation needs it.

### Bladed Weapons — application + progression complete

Represented application:
- executable authority `bladed_weapons.employ_familiar_melee_weapon`;
- task `bladed_weapons_safe_handling_sim_v1`;
- action `blade_drill`;
- exact target `represented_task:bladed_weapons_safe_handling_simulator_v1`;
- exact capability `usable_bladed_training_weapon`;
- simulation-safe, low risk, solo-compatible;
- application evidence only, no automatic XP or harm mutation.

Explicit learning producer:
- `bladed_weapons_handling_practice`;
- action `practice`;
- minimum 10 minutes;
- relevance `{ "bladed_weapons": 1.0 }`;
- dedicated Training Hall practice simulator distinct from the `blade_drill` application simulator;
- ordinary `blade_drill` never becomes learning evidence merely by succeeding.

See `docs/BLADED_WEAPONS_PROGRESSION_V1.md` for the canonical checkpoint.

## Current Skills coverage

### Hand-to-Hand Combat
- represented controlled striking/grapple applications + progression active;
- sparring requires a distinct consenting colocated character;
- no controlled-H2H injury/casualty production.

### Weapon Mastery / Bladed / Firearms
- hierarchy foundation complete;
- Bladed represented safe application complete;
- Bladed explicit progression complete;
- Firearms represented runtime and progression remain missing;
- Weapon Mastery parent remains derived/non-executable;
- hostile use, lethality, injury, casualty generation, and automatic use=>XP remain deferred.

### Survival
- represented field navigation/sustainment + explicit solo progression active.

### Tactical Planning
- represented assessment/maneuver planning + structured progression active.

### Technology
- represented known-fault diagnostic + explicit systems-diagnostic progression active.

### Field Medicine
- read-only casualty assessment + bounded stabilization active;
- both require represented casualty context;
- progression and casualty lifecycle-end continuation remain deferred.

## Preserved casualty foundation

`typed represented fall -> casualty lifecycle state -> read-only Field Medicine assessment -> optional bounded stabilization -> explicit lifecycle-end event required for clear`

Risk reaching zero does not auto-clear or assert healing. No Injury Engine, wound taxonomy, definitive treatment, death/incapacity, or random accidents are implied.

## Next development sequence

1. **Firearms Simulation-Safe Runtime v1 — REVIEW NEXT / not yet implemented.**
2. Reuse the proven Bladed component-owned represented-task pattern rather than inventing another architecture.
3. Move the historical familiar-ranged application semantics onto `firearms`, leaving hidden legacy `weapons` non-executable.
4. Add the smallest solo-usable simulation-safe target/context plus an exact represented Firearms training-resource capability.
5. Keep application evidence separate from learning evidence; no Firearms XP merely for use.
6. No hostile target, lethality, injury, casualty generation, non-consensual combat, ammunition/weapon-consumption expansion, or real-world weapon instructions.
7. Only after the safe Firearms application invariant is proven, review **Firearms Progression Producer v1**.
8. After Firearms application + progression, perform a **Skills section completion review** before moving to another Character Profile section.

## Deferred boundaries

No relationship system expansion, casualty handoff consumer, hostile/non-consensual Combat Engine, weapon lethality, broad casualty simulator, universal Hazard/Injury Engine, bleeding/wound taxonomy, definitive-treatment engine, random-accident scheduler, full Knowledge Engine, H2H hierarchy rewrite, deep weapon taxonomy, economy/jobs/quests, real-world weapon instructions, or synthetic production actors/actions solely for proof.

## Exact resume point

**Bladed Weapons Progression Producer v1 is complete through PR #154 final tested head `148884966ded63559806101cffbeb891efbe96dd`, merge `11ee97f093c7bc5a7439742f3f691f87b6b915de`, CI #908 / run `31890299802` with 518 passing tests plus fresh-DB init/status and relevant acceptance lanes green, post-merge CI #909 SUCCESS, and Deploy #222 / run `31890490349` SUCCESS. `bladed_weapons_handling_practice` is the explicit learning producer; `blade_drill` remains application-only; component score changes re-derive Weapon Mastery/legacy projection without parent XP; Firearms remains inactive. Review Firearms Simulation-Safe Runtime v1 next.**
