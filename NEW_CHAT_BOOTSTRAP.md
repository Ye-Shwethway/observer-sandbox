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

The previously proposed casualty handoff/lifecycle-end consumer is deferred until additional represented-character work resumes. Existing multi-character participant/consent/colocation and casualty primitives remain valid foundations but are not the current priority.

## Current verified deployment

Latest runtime deployment: **Deploy #219 / run `31885774198` SUCCESS**, Survival Skill Progression Producer v1, PR #148 merge `8e094c542d1664f09deb6492ff7dbcb357f95111`.

Final tested PR head: `159afdb3ccda6fd1745148f160954c8c1c7a71d9`.

Validation:
- **CI #888 / run `31885722183` SUCCESS**;
- **500 tests passed in 34.75s**;
- fresh DB init/status succeeded;
- schema remains v5;
- all relevant Skill progression/evidence/definition and Strength validation gates green.

Production readback after Deploy #219:
- service active/healthy; production init succeeded;
- autonomy enabled, normal mode, 1x, retry `null`, pending action present;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram token/API/owner/allowed-user configuration healthy;
- sim time naturally reached `2025-05-06T10:33:00+00:00`;
- Darian was naturally moving while located in the Kitchen;
- Survival remained `85 / A` because no live practice was forced for proof.

Exact Survival learning/progression behavior is CI/ephemeral-fixture evidence. Production deployment proves safe loading and continuity only.

## Skills checkpoint

Production parent Skill values:
- H2H 90/S
- Weapons 87/A
- Survival 85/A
- Tactical Planning 92/S
- Technology 82/A
- Field Medicine 75/A.

### Survival — application + progression loop now meaningful

Represented applications already exist for:
- field navigation;
- field sustainment.

PR #148 added explicit solo-usable learning producers using the existing config-driven `skill_practice` and generic idempotent Skill settlement path:
- `field_navigation_practice`;
- `field_sustainment_practice`.

Both have purpose-built simulation-safe `practice` targets in the Thorne Estate Training Hall and require at least 10 represented minutes.

Learning boundary:
- ordinary obstacle-course use is not Survival XP;
- generic prose/activity is not Survival XP;
- represented Survival application evidence is not automatically learning evidence;
- inspect/research/monitor are not learning evidence;
- only explicit whitelisted practice evidence may settle Survival progression in v1;
- consumed evidence cannot progress twice.

No new progression engine was created.

### Other Skill coverage

- H2H: represented controlled striking/grapple + progression, but represented sparring requires another consenting colocated character.
- Weapons: application definitions exist; represented runtime and progression producer still missing.
- Tactical Planning: represented assessment/planning + progression active.
- Technology: represented diagnostic runtime + explicit practice progression active.
- Field Medicine: represented assessment/stabilization active but requires casualty context; progression and lifecycle-end continuation deferred.

## Preserved casualty foundation

Existing bounded path remains valid:

`typed represented fall -> casualty lifecycle state -> read-only Field Medicine assessment -> optional bounded stabilization -> explicit lifecycle-end event required for clear`

Risk reaching zero never auto-clears and never asserts healing. No broad Injury/Hazard/diagnosis/treatment/death system is implied.

## Hard boundaries

- no relationship system expansion during the current Skills pass;
- no hostile/non-consensual combat engine;
- no Weapons lethality/injury/casualty side effects;
- no Injury Engine, wound/bleeding taxonomy, definitive-treatment graph, death/incapacity model, or random accidents;
- no generic use/application => XP shortcut;
- no fabricated production actors/actions merely for proof.

## Next canonical direction

**Weapons Simulation-Safe Runtime v1 — REVIEW NEXT / not yet implemented.**

Review the existing Weapons skill definitions, represented-task/runtime patterns, available represented training resources and safe targets. Implement the smallest solo-usable familiar-weapon training/simulation application without hostile use, lethality, injury, casualty generation, or automatic Weapons XP.

After represented safe Weapons application coverage is proven, review **Weapons Progression Producer v1**.

## Exact resume point

**Survival Skill Progression Producer v1 is complete through PR #148 final tested head `159afdb3ccda6fd1745148f160954c8c1c7a71d9`, merge `8e094c542d1664f09deb6492ff7dbcb357f95111`, CI #888 / run `31885722183` with 500 passing tests plus fresh-DB init/status and all relevant Skill/Strength gates green, and Deploy #219 / run `31885774198` SUCCESS. Survival now has explicit simulation-safe Field Navigation and Field Sustainment practice producers using structured `skill_practice` learning evidence and the existing idempotent settlement path; generic activity/application evidence remains non-learning evidence. No live practice was forced. Review Weapons Simulation-Safe Runtime v1 next.**
