# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-15

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

During implementation use the smallest task-relevant tests/gates. Do not repeatedly run the full suite. Code/runtime PRs get one final full CI checkpoint by default; docs-only changes skip the full Python suite; do not deliberately repeat a full suite after merge when the already-tested PR is sufficient.

Use **exemplar-first, then batch-by-pattern**. Never manipulate production merely to manufacture evidence.

## Active direction

Development is **profile-first**. Current Character Profile focus: **Skills**.

Relationship/casualty-handoff expansion remains deferred until additional represented-character work resumes.

## Current verified deployment

Latest runtime deployment: **Deploy #225 / run `31892433699` SUCCESS**, Firearms Progression Producer v1, PR #159 merge `d759ef7903f889517e76a48b803fba83bba09ba0`.

Final tested head: `1553621a93e52cb52e948a856dec99a49bd4fc23`.

Validation:
- final **CI #918 / run `31892374935` SUCCESS**;
- Skill Progression Foundation, Skill Evidence Semantics, Skill Definition Format/Refactor, Tactical progression, and Strength Live Cycle gates all green;
- the immediately prior CI #917 had only one stale global revision assertion after 531 passing tests; that assertion alone was aligned;
- no manual repeated full-suite rerun was requested;
- production init/status healthy; schema v5.

Production readback after Deploy #225:
- service active/healthy; autonomy enabled, normal mode, retry null, pending action preserved;
- speed **30x** at readback;
- Gemini `gemini-3.1-flash-lite` primary preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram token/API/owner/allowed-user configuration healthy;
- sim time `2025-05-06T18:56:00+00:00`;
- Darian still naturally sleeping in Darian's Master Suite because the sleep action had already been pending before the circadian fix;
- Bladed Weapons 87/A, Firearms 87/A, Weapon Mastery 87/A, overall Skills A / 85.167;
- no production firearm practice/application was fabricated for proof.

## Circadian stabilization

**Circadian Sleep Rhythm Stabilization v1** is complete through PR #158, merge `f63786c5f0f3d4c4b2098a0c6dc37d9ced9180db`, Deploy #224.

The prior sleep-pressure logic incorrectly made ordinary 16-hour wakefulness a strong sleep need at any clock time, allowing an early wake to phase-lock an early bedtime. Current behavior treats 07:00–22:00 as the normal wake window for ordinary accumulated wakefulness and applies the stronger circadian sleep pull in the 22:00–07:00 night window. Severe >=20h wakefulness or critical raw sleepiness still overrides daytime timing. The already-pending early sleep was deliberately not cancelled or rewritten.

## Weapon Mastery checkpoint

`Weapon Mastery` — derived/non-executable parent
- `Bladed Weapons` — learned component
- `Firearms` — learned component

Parent rules:
- equal-weight mean of components;
- no direct application or XP;
- excluded from overall Skills aggregation;
- hidden legacy `weapons` remains only a compatibility projection;
- component progression re-derives parent/legacy score without granting parent experience.

### Bladed Weapons — application + progression complete

Application runtime:
- `bladed_weapons.employ_familiar_melee_weapon`;
- action `blade_drill`;
- exact simulation-safe capability `usable_bladed_training_weapon`;
- low risk, solo-compatible;
- application evidence only; no automatic XP/harm.

Learning producer:
- `bladed_weapons_handling_practice`;
- action `practice`, minimum 10 minutes;
- dedicated Training Hall practice simulator distinct from `blade_drill`;
- only explicit whitelisted practice evidence progresses Bladed Weapons.

### Firearms — application + progression complete

Application runtime:
- `firearms.employ_familiar_ranged_weapon`;
- action `firearm_drill`;
- exact simulation-safe capability `usable_firearms_training_weapon`;
- low risk, solo-compatible;
- application evidence only; `learning_evidence=false`;
- no automatic XP, ammunition consumption, injury, casualty, hostile-use, lethality, or real-world technique semantics.

Learning producer:
- `firearms_handling_practice`;
- action `practice`, minimum 10 minutes;
- relevance `{ "firearms": 1.0 }`;
- dedicated Training Hall Firearms Practice Simulator distinct from `firearm_drill`;
- only explicit whitelisted `skill_practice` evidence progresses Firearms;
- Bladed Weapons remains an independent sibling;
- legitimate Firearms learning re-derives Weapon Mastery/legacy projection while neither parent receives direct XP;
- ordinary `firearm_drill` remains non-learning.

See `docs/FIREARMS_SIMULATION_SAFE_RUNTIME_V1.md` and `docs/FIREARMS_PROGRESSION_V1.md`.

## Other Skill coverage

- H2H: controlled striking/grapple + progression; sparring needs another consenting colocated character.
- Survival: represented navigation/sustainment + explicit solo progression.
- Tactical Planning: represented assessment/planning + progression.
- Technology: represented diagnostic + explicit practice progression.
- Field Medicine: represented assessment/stabilization; casualty context required; progression/lifecycle continuation deferred.

## Hard boundaries

- no relationship system expansion during the current Skills pass;
- no hostile/non-consensual combat engine;
- no weapon lethality/injury/casualty side effects;
- no real-world weapon instructions;
- no Injury Engine or deep weapon taxonomy;
- no generic use/application => XP shortcut;
- no H2H hierarchy rewrite as a side effect;
- no fabricated production actors/actions merely for proof.

## Next canonical direction

**Skills Section Completion Review — REVIEW NEXT.**

Audit the current Skills section against the profile-first goal. Confirm which Skills have authoritative learned/derived semantics, safe represented application, legitimate progression producers, cognition awareness, and correct profile rendering. Do not create fake producers just to make every row symmetrical: document intentional deferred constraints such as Field Medicine progression and H2H's second-character sparring requirement.

Then decide whether Skills is meaningfully simulation-unlocked under the current scope and choose the next Character Profile section only after that review.

## Exact resume point

**Firearms Progression Producer v1 is complete through PR #159 final tested head `1553621a93e52cb52e948a856dec99a49bd4fc23`, merge `d759ef7903f889517e76a48b803fba83bba09ba0`, final CI #918 with all relevant Skill/Strength acceptance gates green, and Deploy #225 / run `31892433699` SUCCESS. `firearms_handling_practice` is now explicit Firearms learning authority; `firearm_drill` remains application-only/non-learning; Bladed and Firearms progress independently; Weapon Mastery/legacy projection re-derive without direct XP; production stayed healthy and unchanged at 87/A without fabricated practice. Perform the Skills Section Completion Review next.**