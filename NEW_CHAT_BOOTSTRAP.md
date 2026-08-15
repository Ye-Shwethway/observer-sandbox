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

Latest runtime deployment: **Deploy #209 / run `31877214780` SUCCESS**, PR #129 merge `17dd3363467e82fb0fdf099316f619b0757ca5b5`.

Post-deploy production recovery was verified read-only after the existing backoff expired:
- service active/healthy, schema v5;
- autonomy enabled, normal mode, 1x;
- `current_retry` became `null` naturally;
- a new pending action was successfully planned;
- historical `training_movements` ValueError events did not advance at the recovery boundary;
- cognition and Telegram remained intact;
- no manual retry reset, forced live action, or synthetic production evidence was used.

Production parent Skill values remain:
- H2H 90/S
- Weapons 87/A
- Survival 85/A
- Tactical Planning 92/S
- Technology 82/A
- Field Medicine 75/A.

## Skill authority / ontology

- `character_skills.score` = authoritative learned proficiency;
- `character_skills.experience` = legitimate accumulated learning evidence;
- persisted `tier` = compatibility only;
- grade = read-time `skill-proficiency-100-v1`.

Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated reliability. No second competency score exists. Legacy RAPS skill-like fields are compatibility/provenance only.

Current application families are the subskill-like gameplay surface. **Do not create independently scored child Skills yet.**

## Completed current execution chain

Through the Skill/runtime line:
- Skill Definition Refactor Batch v1 — PR #121 / Deploy #204
- Represented Skill Task Instance Resolver v1 — PR #123 / Deploy #205
- Cognition Capability Awareness v1 — PR #124 / Deploy #206
- Cognitive / Performance Modifier Contract v1 — PR #125 / Deploy #207
- Technology Represented Diagnostic Task Runtime v1 — PR #126 / Deploy #208
- sanitized autonomy-error readback — PR #127, corrected by PR #128
- Training Movement Contract Normalization v1 — PR #129 / Deploy #209.

Core files now include the Skill definition/application/capability stack, `represented_skill_tasks.py`, `represented_skill_task_instance.py`, cognition capability awareness, bounded cognitive/performance modifier resolution, and the Technology represented diagnostic runtime.

Canonical docs to use for this line:
- `docs/SKILL_DEFINITION_REFACTOR_BATCH_V1.md`
- `docs/REPRESENTED_SKILL_TASK_CONTRACT_V1.md`
- `docs/REPRESENTED_SKILL_TASK_INSTANCE_RESOLVER_V1.md`
- `docs/COGNITION_CAPABILITY_AWARENESS_V1.md`
- `docs/COGNITIVE_PERFORMANCE_MODIFIER_CONTRACT_V1.md`
- `docs/TECHNOLOGY_DIAGNOSTIC_TASK_RUNTIME_V1.md`.

## Current six gameplay-grade umbrella Skills

Applications:
- H2H: `engage_unarmed_striking`, `control_unarmed_grapple`
- Weapons: `employ_familiar_melee_weapon`, `employ_familiar_ranged_weapon`
- Survival: `navigate_field_environment`, `establish_field_sustainment`
- Tactical Planning: `assess_tactical_situation`, `plan_tactical_maneuver`
- Technology: `diagnose_known_system_fault`
- Field Medicine: `assess_field_casualty`, `stabilize_for_evacuation`.

Application resource requirements use `required_resource_mode: any|none`; supporting resources can produce constrained vs supported without bypassing hard gates.

## Cognition / IQ state

Cognition now receives read-only semantic capability awareness rather than raw Skill numbers alone:
- definition scope and exclusions;
- application families;
- current behavioral anchor;
- challenge/context/resource boundaries;
- relevant supporting Attributes and general reasoning context.

IQ is not Skill or Knowledge. It may affect only explicit task-specific modifier dimensions. It cannot create missing proficiency, Knowledge, target/resource access, or action authority.

The first modifier contract uses bounded reasoning/precision/adaptation effects for the Technology diagnostic exemplar. Deterministic represented-task outcome remains authority.

## Technology represented runtime — complete

Task:
`technology_known_system_fault_diagnostic_sim_v1`

Action:
`diagnose`

Purpose-built target:
`obj_thorne_estate_intel_known_fault_diagnostic_simulator`

Exact definition:
`represented_task:technology_known_fault_diagnostic_simulator_v1`

Flow:
`cognition awareness -> legal action option -> exact represented target binding -> authoritative Skill feasibility -> bounded cognitive modifiers -> deterministic outcome -> immutable application evidence`

Application evidence is explicitly separate from learning evidence and does not auto-award XP. The existing Systems Diagnostic Practice Console remains practice-only.

## Training movement recovery contract

Production exposed a pre-existing autonomy loop when cognition supplied a semantic movement label such as `sparring` for an authored training method that has no movement/anatomy subcatalog.

PR #129 behavior:
- authored method with no movement subcatalog -> auxiliary `training_movements` canonicalizes to empty;
- explicit movement subcatalog -> strict exact movement-id validation;
- unknown/unbound target -> fail closed.

This does not change the chosen action, target, method, duration, progression formula, or evidence authority.

## Learning evidence

Active progression remains only where legitimate evidence exists:
- H2H — structured Training Method evidence;
- Tactical Planning — VR Tactical Drills / AI Combat Simulation;
- Technology — `systems_diagnostic_practice`.

Weapons, Survival and Field Medicine definitions do not activate XP by themselves. Generic actions, application evidence, object names, and model prose are not learning evidence.

## Next canonical slice

**Tactical Planning Represented Assessment Runtime v1** using:
`tactical_planning.assess_tactical_situation`.

Required direction:
- seed a distinct represented tactical simulator/scenario; do not reuse Tactical training/practice targets;
- low-risk `simulation_safe` exemplar;
- expose a concrete legal action through ordinary cognition/action options when contextually available;
- exact target binding and actor-backed Tactical Skill feasibility remain deterministic authority;
- use only explicitly declared task-relevant cognitive factors such as IQ/problem solving/focus/adaptability/tactical reasoning;
- bounded deterministic outcome dimensions, no `Skill score = success percent` shortcut;
- immutable application evidence on completion;
- application evidence remains separate from existing Tactical learning evidence;
- no child Skill creation and no automatic XP from application evidence;
- do not force a production tactical action for proof.

The purpose of this second exemplar is to test whether the Technology runtime pattern generalizes cleanly to a cognitively heavy, non-tool-centric Skill. If structurally proven, batch equivalent follow-ons rather than repeating one bespoke PR per Skill.

## Exact resume point

**Skill/cognition/represented-task gameplay is complete through PR #129 / Deploy #209, and the production autonomy movement-mismatch retry loop has naturally recovered. Next implement one distinct Tactical Planning `assess_tactical_situation` represented runtime exemplar under the existing deterministic Skill/cognition/evidence boundaries.**
