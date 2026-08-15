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

Latest runtime deployment: **Deploy #225 / run `31892433699` SUCCESS**, Firearms Progression Producer v1, PR #159 merge `d759ef7903f889517e76a48b803fba83bba09ba0`.

Final tested PR head: `1553621a93e52cb52e948a856dec99a49bd4fc23`.

Validation:
- final PR **CI #918 / run `31892374935` SUCCESS**;
- task-relevant Skill Progression, Skill Evidence, Skill Definition, Skill Definition Refactor, Tactical Planning progression, and Strength Live Cycle gates all succeeded;
- the prior CI #917 had exactly one stale global progression-revision assertion after 531 passing tests; only that assertion was corrected;
- no manual repeated full-suite rerun was requested;
- production init/status succeeded; schema remains v5.

Verified production readback after Deploy #225:
- service active/healthy; production init succeeded; schema v5;
- autonomy enabled, normal mode, retry null, pending action preserved;
- runtime speed was **30x** at readback;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram bot/API/owner/allowed-user configuration healthy;
- live sim time remained `2025-05-06T18:56:00+00:00` because the pre-existing overnight sleep action was still pending;
- Darian remained naturally sleeping in Darian's Master Suite;
- Bladed Weapons remained 87/A, Firearms 87/A, Weapon Mastery 87/A, overall Skills A / 85.167;
- no production firearm practice/application was fabricated for proof.

The unchanged production scores are expected: initialization activates the Firearms learning producer with zero gain. Exact learning, sibling isolation, hierarchy re-derivation, idempotency, and application-vs-learning separation are fixture/CI evidence; deployment proves safe loading and continuity.

### Circadian stabilization checkpoint

Before Firearms progression, **Circadian Sleep Rhythm Stabilization v1** shipped through PR #158, merge `f63786c5f0f3d4c4b2098a0c6dc37d9ced9180db`, Deploy #224.

The sleep-pressure model no longer treats ordinary 16-hour wakefulness as a strong sleep signal at any clock time. Ordinary accumulated wakefulness becomes strongly sleep-promoting in the authored 22:00–07:00 night window, while severe >=20h wakefulness or critical raw sleepiness can still override the daytime wake window. This prevents the observed `02:56 wake -> 18:56 sleep -> 02:56 wake` wrong-phase lock without introducing a heavy scheduler. The sleep action already pending before that deploy was deliberately not cancelled or rewritten.

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
- legitimate component learning re-derives the parent and legacy projection without granting either direct XP;
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

### Firearms — application + progression complete

Represented application:
- executable authority `firearms.employ_familiar_ranged_weapon`;
- task `firearms_safe_handling_sim_v1`;
- action `firearm_drill`;
- exact target `represented_task:firearms_safe_handling_simulator_v1`;
- exact capability `usable_firearms_training_weapon`;
- simulation-safe, low risk, solo-compatible;
- completion emits application evidence with `learning_evidence=false`;
- no ammunition consumption, hostile target, injury, casualty, lethality, or real-world technique semantics.

Explicit learning producer:
- `firearms_handling_practice`;
- action `practice`;
- minimum 10 minutes;
- relevance `{ "firearms": 1.0 }`;
- dedicated Training Hall Firearms Practice Simulator distinct from the `firearm_drill` application simulator;
- only whitelisted `skill_practice` evidence can progress Firearms;
- Firearms learning does not mutate Bladed Weapons;
- legitimate Firearms score changes re-derive Weapon Mastery and the hidden legacy projection while both remain XP-free;
- ordinary `firearm_drill` remains application-only/non-learning.

See `docs/FIREARMS_SIMULATION_SAFE_RUNTIME_V1.md` and `docs/FIREARMS_PROGRESSION_V1.md`.

## Current Skills coverage

### Hand-to-Hand Combat
- represented controlled striking/grapple applications + progression active;
- sparring requires a distinct consenting colocated character;
- no controlled-H2H injury/casualty production.

### Weapon Mastery / Bladed / Firearms
- hierarchy foundation complete;
- Bladed represented safe application + explicit progression complete;
- Firearms represented safe application + explicit progression complete;
- Weapon Mastery parent remains derived/non-executable and has no direct XP;
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

1. **Skills Section Completion Review — REVIEW NEXT.**
2. Audit each currently represented Skill against the profile-first completion standard: authoritative score/grade semantics, meaningful application where safely runnable, legitimate progression where an explicit producer exists, cognition awareness, profile rendering, and separation of application evidence from learning evidence.
3. Do not invent runtime producers merely to make the checklist uniformly green; document intentional deferred cases such as Field Medicine progression and H2H's second-character sparring requirement.
4. Decide whether the Skills profile section is meaningfully simulation-unlocked under current scope.
5. Only after that review choose the next Character Profile section; do not expand relationships or deep weapon taxonomy as a side effect.

## CI cadence

The canonical CI loop is designed to avoid redundant full-suite runs:
- focused task-relevant tests/gates during implementation;
- one final full CI checkpoint for code/runtime PRs by default;
- no deliberate second full-suite run merely because an already-tested PR merged to `main`;
- docs-only pull requests skip the full Python suite;
- manual full reruns only when broader risk actually warrants one.

Some specialized acceptance workflows may still run automatically on matching pushes; do not mistake those for manually requested full-suite loops.

## Deferred boundaries

No relationship system expansion, casualty handoff consumer, hostile/non-consensual Combat Engine, weapon lethality, broad casualty simulator, universal Hazard/Injury Engine, bleeding/wound taxonomy, definitive-treatment engine, random-accident scheduler, full Knowledge Engine, H2H hierarchy rewrite, deep weapon taxonomy, economy/jobs/quests, real-world weapon instructions, or synthetic production actors/actions solely for proof.

## Exact resume point

**Firearms Progression Producer v1 is complete through PR #159 final tested head `1553621a93e52cb52e948a856dec99a49bd4fc23`, merge `d759ef7903f889517e76a48b803fba83bba09ba0`, final CI #918 plus all task-relevant Skill/Strength acceptance gates green, and Deploy #225 / run `31892433699` SUCCESS. `firearms_handling_practice` is now the explicit simulation-safe Firearms learning producer; ordinary `firearm_drill` remains application-only/non-learning; Bladed and Firearms progress independently; Weapon Mastery/legacy projection re-derive without direct XP. Production stayed healthy, scores remained 87/A without fabricated practice, and the pre-existing sleep action remained untouched. Review the Skills section for meaningful simulation completion next.**