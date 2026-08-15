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

## Workflow

Default:
`branch -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`

Use **exemplar-first, then batch-by-pattern**. Never manipulate production merely to manufacture evidence. Darian/Thorne Estate are exemplars only.

## Current verified deployment

Latest runtime deployment: **Deploy #204 / run `31874569397` SUCCESS**, Skill Definition Refactor Batch v1, PR #121 merge `3eb94d408c6d207610cb17920ae16dd42172b6e4`.

Verified:
- PR Skill Definition Refactor Batch Acceptance #1 / `31874524536`: SUCCESS;
- PR CI #826 / `31874524531`: SUCCESS;
- downstream Skill/Application/Capability/Represented-Task regressions: SUCCESS;
- Strength Live Cycle #39 / `31874524516`: SUCCESS;
- Public Security #78 / `31874524485`: SUCCESS;
- post-merge Skill Definition Refactor Batch Acceptance #2 / `31874569354`: SUCCESS;
- post-merge CI #827 / `31874569313`: SUCCESS;
- Deploy #204 / `31874569397`: SUCCESS;
- service active/healthy, schema v5, autonomy normal 1x, Telegram/cognition intact.

Production parent Skill values remained unchanged: H2H 90/S, Weapons 87/A, Survival 85/A, Tactical Planning 92/S, Technology 82/A, Field Medicine 75/A. No live action or migration was forced for proof.

## Skill authority / ontology

- `character_skills.score` = authoritative learned proficiency;
- `character_skills.experience` = legitimate accumulated learning evidence;
- persisted `tier` = compatibility only;
- grade = read-time `skill-proficiency-100-v1`.

Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated reliability. No second competency score exists. Legacy RAPS skill-like fields remain compatibility/provenance only.

## Current Skill execution stack

- `config/skill_definitions.v1.json`
- `src/observer_sandbox/skill_definitions.py`
- `src/observer_sandbox/skill_application_requirements.py`
- `src/observer_sandbox/skill_capability.py`
- `src/observer_sandbox/actor_skill_capability.py`
- `config/represented_skill_tasks.v1.json`
- `src/observer_sandbox/represented_skill_tasks.py`

Canonical docs include the Skill framework/creation/application/capability/actor-adapter docs plus `docs/REPRESENTED_SKILL_TASK_CONTRACT_V1.md`, `docs/SKILL_DEFINITION_REFACTOR_BATCH_V1.md`, and progression/evidence docs referenced by ROADMAP.

## Current six gameplay-grade umbrella Skills

All six actor Skills now have universal definitions, E/D/C/B/A/S anchors, bounded applications, executable context/resource requirements, risk/consequence boundaries, and explicit learning-evidence policies.

Applications:
- H2H: `engage_unarmed_striking`, `control_unarmed_grapple`
- Weapons: `employ_familiar_melee_weapon`, `employ_familiar_ranged_weapon`
- Survival: `navigate_field_environment`, `establish_field_sustainment`
- Tactical Planning: `assess_tactical_situation`, `plan_tactical_maneuver`
- Technology: `diagnose_known_system_fault`
- Field Medicine: `assess_field_casualty`, `stabilize_for_evacuation`.

Application resources use `required_resource_mode: any|none`. Supporting resources remain optional and can create `constrained` rather than unsupported results.

## Subskill policy

These applications are the current subskill-like gameplay surface. **Do not create independently scored child Skills yet.** Parent `character_skills.score` remains authoritative.

A true child Skill requires independently distinguishable learning evidence, independent progression/retention ownership, and explicit parent/child aggregation plus migration semantics. Never split parent scores into invented child values. Current `component_skills` remains empty.

## Learning evidence

Active progression remains only where legitimate evidence already exists:
- H2H — structured Training Method evidence;
- Tactical Planning — VR Tactical Drills / AI Combat Simulation;
- Technology — `systems_diagnostic_practice`.

Weapons, Survival and Field Medicine definitions do not activate XP by themselves. Generic actions, object names and model prose remain invalid learning evidence.

## Represented Skill Task Contract v1

First task: `technology_known_system_fault_diagnostic_sim_v1`.

It binds Technology `diagnose_known_system_fault` to exact target definition `represented_task:technology_known_fault_diagnostic_simulator_v1`, challenge `standard`, explicit context/resource semantics and bounded low-risk simulation outcomes.

No task entity is seeded yet. The Systems Diagnostic Practice Console remains practice/learning evidence only.

## Next canonical slice

**Represented Skill Task Instance Resolver v1 — read-only.**

Invariant:
`actor + task_id + target_entity_id + explicit available resource capabilities -> validate exact target type/definition/capabilities -> derive task challenge/context -> actor-backed Skill assessment -> read-only represented-task assessment`

Constraints:
- exact `definition_id`; no name/prose matching;
- fail closed on target mismatch;
- never reuse the practice console;
- prove with synthetic entities; no production simulator seed needed;
- resources remain explicit caller/task inputs until represented resource ownership is separately proven;
- no writes, action authorization, events/evidence, XP, autonomy or Telegram integration.

Expected Technology exemplar behavior:
- missing required diagnostic capability -> unsupported;
- required diagnostic capability present but documentation absent -> constrained;
- required + supporting capabilities present -> supported, subject to proficiency/challenge support.

## Exact resume point

**Skill Definition Refactor Batch v1 is complete/deployed through PR #121 / Deploy #204. All six current umbrella Skills are gameplay-definition complete while parent scores remain authoritative. Next implement the read-only Represented Skill Task Instance Resolver v1; do not seed a production simulator or wire live actions yet.**
