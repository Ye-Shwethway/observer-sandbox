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
`branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`

Use **exemplar-first, then batch-by-pattern**. Never manipulate production merely to manufacture evidence.

## Active direction

Development is **profile-first**. Current Character Profile focus: **Skills**.

Relationship/casualty-handoff expansion remains deferred until additional represented-character work resumes.

## Current verified deployment

Latest runtime deployment: **Deploy #222 / run `31890490349` SUCCESS**, Bladed Weapons Progression Producer v1, PR #154 merge `11ee97f093c7bc5a7439742f3f691f87b6b915de`.

Final tested head: `148884966ded63559806101cffbeb891efbe96dd`.

Validation:
- **CI #908 / run `31890299802` SUCCESS — 518 passed in 191.64s**;
- fresh DB init/status healthy; schema v5;
- relevant Skill Progression/Evidence/Definition/Tactical/Strength gates green;
- post-merge **CI #909 / run `31890490342` SUCCESS**.

Production readback after Deploy #222:
- service active/healthy; production init succeeded;
- autonomy enabled, normal mode, **10x**, retry null, pending action present;
- Gemini `gemini-3.1-flash-lite` primary preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram token/API/owner/allowed-user configuration healthy;
- sim time `2025-05-06T17:18:00+00:00`;
- Darian naturally resting in Darian's Master Suite;
- Bladed Weapons 87/A, Firearms 87/A, Weapon Mastery 87/A, overall Skills A / 85.167;
- no production practice or weapon action was fabricated for proof.

The unchanged scores are expected: initialization uses a zero-gain progression bootstrap. Learning behavior is CI/fixture evidence.

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
- exact simulation-safe target/resource capability `usable_bladed_training_weapon`;
- low risk, solo-compatible;
- application evidence only; no automatic XP/harm.

Learning producer:
- `bladed_weapons_handling_practice`;
- action `practice`, minimum 10 minutes;
- exact relevance `{ "bladed_weapons": 1.0 }`;
- dedicated Training Hall practice simulator distinct from `blade_drill`;
- only explicit whitelisted practice evidence progresses Bladed Weapons.

See `docs/BLADED_WEAPONS_PROGRESSION_V1.md`.

### Firearms

Firearms remains a learned component with no represented runtime or progression producer yet.

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

**Firearms Simulation-Safe Runtime v1 — REVIEW NEXT / not yet implemented.**

Reuse the proven Bladed pattern: component-owned represented application, exact safe target/context, exact represented training resource capability, deterministic application evidence, and no automatic XP. Keep hidden legacy Weapons and Weapon Mastery parent non-executable. No hostile/lethal/casualty semantics or real-world technique instructions.

After the safe Firearms application invariant is proven, review **Firearms Progression Producer v1**. After Firearms application + progression, perform the **Skills section completion review** before choosing the next Character Profile section.

## Exact resume point

**Bladed Weapons Progression Producer v1 is complete through PR #154 final tested head `148884966ded63559806101cffbeb891efbe96dd`, merge `11ee97f093c7bc5a7439742f3f691f87b6b915de`, CI #908 / run `31890299802` with 518 passing tests plus fresh-DB init/status and relevant gates green, post-merge CI #909 SUCCESS, and Deploy #222 / run `31890490349` SUCCESS. Explicit `bladed_weapons_handling_practice` now provides learning evidence; ordinary `blade_drill` remains non-learning application evidence; Weapon Mastery stays derived/non-executable; Firearms remains inactive. Review Firearms Simulation-Safe Runtime v1 next.**
