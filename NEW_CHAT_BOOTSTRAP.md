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

Development is currently **profile-first**: make Character Profile sections meaningfully participate in simulation before expanding relationship or broader multi-character systems.

Current section focus: **Skills**.

Relationship/casualty-handoff expansion remains deferred until additional represented-character work resumes.

## Current verified deployment

Latest runtime deployment: **Deploy #220 / run `31886986845` SUCCESS**, Weapon Mastery Skill Hierarchy Foundation v1, PR #150 merge `d2616db5cf08e496b66c3f939ae3b2dcbf1560c4`.

Final tested PR head: `d4c23e77e24d6a7f6c75146b78ecab81be34d662`.

Validation:
- **CI #894 / run `31886921670` SUCCESS**;
- **506 tests passed in 41.06s**;
- fresh DB init/status succeeded;
- schema remains v5;
- Cognition Capability Awareness, Skill Progression, Skill Evidence, Grading, Strength, Inventory, and Technology acceptance lanes green.

Production readback after Deploy #220:
- service active/healthy; production init succeeded;
- autonomy enabled, normal mode, 1x, retry `null`, pending action present;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram token/API/owner/allowed-user configuration healthy;
- sim time naturally reached `2025-05-06T10:48:00+00:00`;
- Darian was naturally eating in the Kitchen;
- no production weapon action/practice/target/harm event was fabricated for proof.

Production `init` executed hierarchy reconciliation safely. Exact hierarchy row migration/derivation and profile/cognition behavior are proven by CI/fresh-DB fixtures; the deploy workflow did not separately dump the live hierarchy rows.

## Skills checkpoint

### Weapon Mastery hierarchy — complete foundation

Canonical v1 structure:

`Weapon Mastery` — derived parent
- `Bladed Weapons` — learned component
- `Firearms` — learned component

Authority rules:
- learned components own proficiency;
- parent is equal-weight derived summary only;
- parent cannot receive direct XP or authorize a represented task;
- parent is excluded from overall Skills aggregation to prevent double-counting;
- historical `weapons = 87` initializes both components only as an explicit compatibility baseline and does not prove distinct historical specialization scores;
- existing child score/experience/learning metadata survives reinitialize;
- old `weapons` row remains temporarily hidden as a compatibility projection while historical definition paths are retired;
- profile and cognition expose the canonical hierarchy, not the hidden projection;
- no weapon runtime or progression was activated by the foundation.

Do not build a deep knife/sword/handgun/rifle taxonomy until a real simulation need appears.

### Other Skill coverage

- H2H: represented controlled striking/grapple + progression; represented sparring requires another consenting colocated character. No H2H hierarchy rewrite now.
- Survival: represented navigation/sustainment + explicit solo progression active.
- Tactical Planning: represented assessment/planning + progression active.
- Technology: represented diagnostic runtime + explicit practice progression active.
- Field Medicine: represented assessment/stabilization active but requires casualty context; progression and lifecycle-end continuation deferred.

## Preserved casualty foundation

`typed represented fall -> casualty lifecycle state -> read-only Field Medicine assessment -> optional bounded stabilization -> explicit lifecycle-end event required for clear`

Risk reaching zero never auto-clears and never asserts healing. No broad Injury/Hazard/diagnosis/treatment/death system is implied.

## Hard boundaries

- no relationship system expansion during the current Skills pass;
- no hostile/non-consensual combat engine;
- no weapon lethality/injury/casualty side effects;
- no Injury Engine or deep weapon taxonomy;
- no generic use/application => XP shortcut;
- no H2H hierarchy rewrite as a side effect;
- no fabricated production actors/actions merely for proof.

## Next canonical direction

**Bladed Weapons Simulation-Safe Runtime v1 — REVIEW NEXT / not yet implemented.**

Reconcile the historical `employ_familiar_melee_weapon` definition and make `bladed_weapons` the actual represented capability authority. Add the smallest solo-usable safe training/simulation target plus exact represented bladed-weapon resource capability. `weapon_mastery` remains non-executable. Application evidence is not learning evidence and must not award XP.

After the safe Bladed Weapons application invariant is proven, review **Bladed Weapons Progression Producer v1**. Then apply the proven pattern to **Firearms** rather than inventing another architecture.

## Exact resume point

**Weapon Mastery Skill Hierarchy Foundation v1 is complete through PR #150 final tested head `d4c23e77e24d6a7f6c75146b78ecab81be34d662`, merge `d2616db5cf08e496b66c3f939ae3b2dcbf1560c4`, CI #894 / run `31886921670` with 506 passing tests plus fresh-DB init/status and relevant acceptance lanes green, and Deploy #220 / run `31886986845` SUCCESS. Weapon Mastery is now a derived non-executable parent over learned Bladed Weapons and Firearms; legacy Weapons is only a documented compatibility baseline/projection, existing child learning state is preserved, and no weapon runtime or XP was activated. Review Bladed Weapons Simulation-Safe Runtime v1 next.**
