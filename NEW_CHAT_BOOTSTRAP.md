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

Development is currently **profile-first**. Current Character Profile focus: **Skills**.

Relationship/casualty-handoff expansion remains deferred until additional represented-character work resumes.

## Current verified deployment

Latest runtime deployment: **Deploy #221 / run `31889659349` SUCCESS**, Bladed Weapons Simulation-Safe Runtime v1, PR #152 merge `ce77b0a9a78684283c69daa3357df1dcd4d9aeb6`.

Final tested PR head: `44f70f8f9768665851858a16bc198c962d9b512a`.

Validation:
- **CI #902 / run `31889534085` SUCCESS**;
- **513 tests passed in 42.24s**;
- fresh DB init/status succeeded;
- schema remains v5;
- relevant Skill Definition/Application/Capability/Represented Task/Cognition/Technology/Strength gates green.

Production readback after Deploy #221:
- service active/healthy; production init succeeded;
- autonomy enabled, normal mode, **10x**, retry `null`, pending action present;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram token/API/owner/allowed-user configuration healthy;
- sim time naturally reached `2025-05-06T14:18:00+00:00`;
- Darian was naturally reading in the Living Room;
- Bladed Weapons 87/A, Firearms 87/A, Weapon Mastery 87/A, overall Skills A / 85.167;
- no production `blade_drill` or other weapon action was fabricated for proof.

Exact application/evidence/no-XP behavior is CI/fixture evidence. Production deployment proves safe loading and continuity only.

## Weapon Mastery checkpoint

Canonical hierarchy:

`Weapon Mastery` — derived parent
- `Bladed Weapons` — learned component
- `Firearms` — learned component

Authority rules:
- learned components own proficiency;
- parent is equal-weight derived summary only;
- parent cannot receive direct XP or authorize a represented task;
- historical `weapons = 87` was only a compatibility baseline, not proof of distinct specialization measurements;
- old `weapons` remains temporarily as hidden compatibility projection while historical paths are retired.

### Bladed Weapons — represented runtime active

Executable melee application authority is now:
`bladed_weapons.employ_familiar_melee_weapon`

The hidden legacy `weapons` projection no longer executes that application.

Represented task:
- `bladed_weapons_safe_handling_sim_v1`;
- action `blade_drill`;
- exact target definition `represented_task:bladed_weapons_safe_handling_simulator_v1`;
- exact resource/target capability `usable_bladed_training_weapon`;
- Training Hall, solo-compatible, simulation-safe, low risk.

Deterministic behavior:
- Bladed learned score is the performance authority;
- no extra cognitive/Attribute modifier contract was invented;
- completion emits application evidence only;
- `learning_evidence=false`;
- no automatic XP, injury, casualty, hostile-use, weapon-consumption, or real-world technique semantics.

### Firearms

Firearms remains a learned component with no active represented runtime or progression producer yet.

## Other Skill coverage

- H2H: represented controlled striking/grapple + progression; sparring requires another consenting colocated character. No hierarchy rewrite now.
- Survival: represented navigation/sustainment + explicit solo progression active.
- Tactical Planning: represented assessment/planning + progression active.
- Technology: represented diagnostic runtime + explicit practice progression active.
- Field Medicine: represented assessment/stabilization active but requires casualty context; progression/lifecycle continuation deferred.

## Preserved casualty foundation

`typed represented fall -> casualty lifecycle state -> read-only Field Medicine assessment -> optional bounded stabilization -> explicit lifecycle-end event required for clear`

Risk reaching zero never auto-clears and never asserts healing. No broad Injury/Hazard/diagnosis/treatment/death system is implied.

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

**Bladed Weapons Progression Producer v1 — REVIEW NEXT / not yet implemented.**

Add one explicit simulation-safe Bladed learning producer using the existing progression machinery where possible. Ordinary `blade_drill` represented application evidence must remain non-learning evidence. Component learning may re-derive Weapon Mastery, but the parent never receives direct XP.

After Bladed application + progression is complete, apply the proven pattern to **Firearms Simulation-Safe Runtime v1** rather than inventing another architecture.

## Exact resume point

**Bladed Weapons Simulation-Safe Runtime v1 is complete through PR #152 final tested head `44f70f8f9768665851858a16bc198c962d9b512a`, merge `ce77b0a9a78684283c69daa3357df1dcd4d9aeb6`, CI #902 / run `31889534085` with 513 passing tests plus fresh-DB init/status and all relevant gates green, and Deploy #221 / run `31889659349` SUCCESS. Bladed Weapons now owns executable simulation-safe melee application authority through `blade_drill` plus exact `usable_bladed_training_weapon`; Weapon Mastery remains derived/non-executable, Firearms remains inactive, application evidence does not award XP, and no production proof action was forced. Review Bladed Weapons Progression Producer v1 next.**
