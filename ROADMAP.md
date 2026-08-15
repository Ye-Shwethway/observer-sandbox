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
- Development verification is focused-first: use task-relevant tests/gates while iterating and reserve the full suite for the final code/runtime PR checkpoint unless broader risk justifies another run. Docs-only changes do not need the full Python suite.

## Current development direction

The active roadmap is **profile-first**. Current Character Profile focus: **Skills**.

Relationship-oriented expansion and casualty handoff/lifecycle-end work remain deferred until additional represented-character work resumes.

## Current verified deployment

Latest runtime deployment: **Deploy #223 / run `31891128059` SUCCESS**, Firearms Simulation-Safe Runtime v1, PR #156 merge `ea5dad4fb49180e37eaff5435bd82c8f0c4a487e`.

Final tested PR head: `33c52000595f00f36687afef670ebf105dd5f9c2`.

Validation:
- **CI #912 / run `31891065742` SUCCESS**;
- final full-suite checkpoint: **525 passed in 31.20s**;
- fresh DB init/status succeeded; schema remains v5;
- Strength Live Cycle Validation #67 / run `31891065783` succeeded on a disposable production copy;
- no iterative full-suite reruns were used for this slice.

Verified production readback after Deploy #223:
- service active/healthy; production init succeeded; schema v5;
- autonomy enabled, normal mode, **5x**, retry null, pending action present;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram bot/API/owner/allowed-user configuration healthy;
- live sim time was `2025-05-06T18:56:00+00:00`;
- Darian was naturally sleeping in Darian's Master Suite;
- Bladed Weapons remained 87/A, Firearms 87/A, Weapon Mastery 87/A, overall Skills A / 85.167;
- no production `firearm_drill`, practice, or other weapon proof action was fabricated.

The unchanged production scores are expected. Exact Firearms application, evidence, fail-closed, idempotency, and no-XP behavior are CI/fresh-fixture evidence; deployment proves safe loading and runtime continuity only.

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
- component learning re-derives the parent and legacy projection without granting either direct XP;
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

See `docs/BLADED_WEAPONS_PROGRESSION_V1.md`.

### Firearms — represented application active

Represented application:
- executable authority `firearms.employ_familiar_ranged_weapon`;
- hidden legacy `weapons` no longer executes the ranged application;
- task `firearms_safe_handling_sim_v1`;
- action `firearm_drill`;
- exact target `represented_task:firearms_safe_handling_simulator_v1`;
- exact capability `usable_firearms_training_weapon`;
- context includes `weapon_employment_context`, `represented_ranged_weapon`, and `simulation_safe_training_context`;
- simulation-safe, low risk, solo-compatible;
- Firearms learned score is the sole performance authority for this exemplar; no cognitive/Attribute bonus contract was invented;
- completion emits application evidence with `learning_evidence=false`;
- no ammunition consumption, hostile target, injury, casualty, lethality, or real-world technique semantics.

Firearms progression remains inactive pending the next slice.

See `docs/FIREARMS_SIMULATION_SAFE_RUNTIME_V1.md`.

## Current Skills coverage

### Hand-to-Hand Combat
- represented controlled striking/grapple applications + progression active;
- sparring requires a distinct consenting colocated character;
- no controlled-H2H injury/casualty production.

### Weapon Mastery / Bladed / Firearms
- hierarchy foundation complete;
- Bladed represented safe application + explicit progression complete;
- Firearms represented safe application complete;
- Firearms progression remains missing;
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

1. **Firearms Progression Producer v1 — REVIEW NEXT / not yet implemented.**
2. Reuse the proven Bladed explicit-practice progression pattern rather than treating `firearm_drill` application evidence as learning.
3. Add one dedicated simulation-safe Firearms practice method/target with explicit whitelisted learning evidence.
4. Progress only the `firearms` component; do not mutate Bladed Weapons as a sibling side effect.
5. Re-derive Weapon Mastery and the hidden legacy projection after legitimate Firearms component learning, while granting neither parent direct XP.
6. Preserve exact safe resource/target semantics and no ammunition/harm side effects.
7. After Firearms application + progression are complete, perform a **Skills section completion review** before moving to another Character Profile section.

## CI cadence

The canonical CI loop is now designed to avoid redundant full-suite runs:
- focused task-relevant tests/gates during implementation;
- one full CI suite on code/runtime pull requests as the final checkpoint;
- no automatic second full-suite run merely because the already-tested PR merged to `main`;
- docs-only pull requests skip the full Python suite;
- manual `workflow_dispatch` remains available when a deliberate full rerun is warranted.

## Deferred boundaries

No relationship system expansion, casualty handoff consumer, hostile/non-consensual Combat Engine, weapon lethality, broad casualty simulator, universal Hazard/Injury Engine, bleeding/wound taxonomy, definitive-treatment engine, random-accident scheduler, full Knowledge Engine, H2H hierarchy rewrite, deep weapon taxonomy, economy/jobs/quests, real-world weapon instructions, or synthetic production actors/actions solely for proof.

## Exact resume point

**Firearms Simulation-Safe Runtime v1 is complete through PR #156 final tested head `33c52000595f00f36687afef670ebf105dd5f9c2`, merge `ea5dad4fb49180e37eaff5435bd82c8f0c4a487e`, CI #912 / run `31891065742` with 525 passing tests plus fresh-DB init/status, Strength Live Cycle Validation #67 green, and Deploy #223 / run `31891128059` SUCCESS. `firearms.employ_familiar_ranged_weapon` now owns the simulation-safe `firearm_drill` application requiring exact `usable_firearms_training_weapon`; Weapon Mastery remains derived/non-executable; application evidence remains non-learning; production stayed healthy at 5x with Darian naturally sleeping and no proof action forced. Review Firearms Progression Producer v1 next.**
