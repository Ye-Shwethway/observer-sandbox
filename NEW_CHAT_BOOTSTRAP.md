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

During implementation use the smallest task-relevant tests/gates. Do not repeatedly run the full suite. Code/runtime PRs get one final full CI checkpoint by default; docs-only changes skip the full Python suite; merge-to-main does not need a duplicate full-suite run.

Use **exemplar-first, then batch-by-pattern**. Never manipulate production merely to manufacture evidence.

## Active direction

Development is **profile-first**. Current Character Profile focus: **Skills**.

Relationship/casualty-handoff expansion remains deferred until additional represented-character work resumes.

## Current verified deployment

Latest runtime deployment: **Deploy #223 / run `31891128059` SUCCESS**, Firearms Simulation-Safe Runtime v1, PR #156 merge `ea5dad4fb49180e37eaff5435bd82c8f0c4a487e`.

Final tested head: `33c52000595f00f36687afef670ebf105dd5f9c2`.

Validation:
- **CI #912 / run `31891065742` SUCCESS — 525 passed in 31.20s**;
- fresh DB init/status healthy; schema v5;
- Strength Live Cycle Validation #67 / run `31891065783` succeeded;
- no iterative full-suite rerun was needed.

Production readback after Deploy #223:
- service active/healthy; production init succeeded;
- autonomy enabled, normal mode, **5x**, retry null, pending action present;
- Gemini `gemini-3.1-flash-lite` primary preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram token/API/owner/allowed-user configuration healthy;
- sim time `2025-05-06T18:56:00+00:00`;
- Darian naturally sleeping in Darian's Master Suite;
- Bladed Weapons 87/A, Firearms 87/A, Weapon Mastery 87/A, overall Skills A / 85.167;
- no production firearm practice/action was fabricated for proof.

Exact Firearms application/no-XP behavior is CI/fresh-fixture evidence. Deployment proves safe loading and continuity only.

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

### Firearms — represented runtime active

Executable ranged authority is now:
`firearms.employ_familiar_ranged_weapon`

The hidden legacy `weapons` projection no longer executes the ranged application.

Represented task:
- `firearms_safe_handling_sim_v1`;
- action `firearm_drill`;
- exact target `represented_task:firearms_safe_handling_simulator_v1`;
- exact resource/target capability `usable_firearms_training_weapon`;
- Training Hall, solo-compatible, simulation-safe, low risk.

Deterministic behavior:
- Firearms learned score is the performance authority;
- no cognitive/Attribute modifier contract is invented;
- completion emits application evidence only;
- `learning_evidence=false`;
- no automatic XP, ammunition consumption, injury, casualty, hostile-use, lethality, or real-world technique semantics.

Firearms progression remains inactive.

See `docs/FIREARMS_SIMULATION_SAFE_RUNTIME_V1.md`.

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

**Firearms Progression Producer v1 — REVIEW NEXT / not yet implemented.**

Reuse the proven Bladed explicit-practice pattern. Add one dedicated simulation-safe Firearms practice producer whose whitelisted learning evidence progresses only `firearms`. Ordinary `firearm_drill` must remain application-only/non-learning. Legitimate Firearms component learning may re-derive Weapon Mastery/legacy projection but neither parent receives direct XP.

After Firearms application + progression are complete, perform the **Skills section completion review** before choosing the next Character Profile section.

## Exact resume point

**Firearms Simulation-Safe Runtime v1 is complete through PR #156 final tested head `33c52000595f00f36687afef670ebf105dd5f9c2`, merge `ea5dad4fb49180e37eaff5435bd82c8f0c4a487e`, CI #912 / run `31891065742` with 525 passing tests plus fresh-DB init/status, Strength Live Cycle Validation #67 green, and Deploy #223 / run `31891128059` SUCCESS. Firearms now owns executable simulation-safe ranged application authority through `firearm_drill` plus exact `usable_firearms_training_weapon`; Weapon Mastery remains derived/non-executable; application evidence does not award XP; production remained healthy at 5x and no proof action was forced. Review Firearms Progression Producer v1 next.**
