# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-15

## Operating principles

- Runtime/code/config plus verified live production are authoritative over remembered chat.
- AI proposes structured cognition; deterministic engines validate and mutate.
- Telegram is observer/control, never simulation authority.
- Preserve: `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Darian/Thorne Estate are exemplars, never reusable-engine identity.
- Use minimum-runnable reversible slices and **exemplar-first, then batch-by-pattern**.
- Never manipulate production merely to manufacture evidence.

## Current verified deployment

Latest runtime deployment: **Deploy #204 / run `31874569397` SUCCESS**, Skill Definition Refactor Batch v1, PR #121 merge `3eb94d408c6d207610cb17920ae16dd42172b6e4`.

Verified:
- PR Skill Definition Refactor Batch Acceptance #1 / `31874524536`: SUCCESS;
- PR CI #826 / `31874524531`: SUCCESS;
- all downstream Skill/Application/Capability/Represented-Task regressions: SUCCESS;
- Strength Live Cycle #39 / `31874524516`: SUCCESS;
- Public Security #78 / `31874524485`: SUCCESS;
- post-merge Skill Definition Refactor Batch Acceptance #2 / `31874569354`: SUCCESS;
- post-merge CI #827 / `31874569313`: SUCCESS;
- Deploy #204 / `31874569397`: SUCCESS;
- service healthy/active, schema v5, autonomy normal 1.0x, Telegram/cognition intact.

Production readback preserved current parent Skill state:
- H2H `90.0 / S`
- Weapons `87.0 / A`
- Survival `85.0 / A`
- Tactical Planning `92.0 / S`
- Technology `82.0 / A`
- Field Medicine `75.0 / A`.

No live action, XP migration, child Skill creation, or synthetic production evidence was forced.

## Skill authority / ontology

- `character_skills.score` = authoritative learned proficiency;
- `character_skills.experience` = legitimate accumulated learning evidence;
- persisted `tier` = compatibility only;
- grade = read-time `skill-proficiency-100-v1`.

Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated reliability. No second competency score exists. Legacy RAPS skill-like fields remain compatibility/provenance only and are not independent Skill truth.

## Completed Skill execution chain

1. H2H Skill Progression v1 — PR #104 / Deploy #196
2. Tactical Planning Skill Progression — PR #106 / Deploy #197
3. Skill Evidence Semantics / Technology practice — PR #108 / Deploy #198
4. Skill Definition & Capability Framework — PR #110
5. Skill Creation Format / Technology definition — PR #111 / Deploy #199
6. Skill Application Requirements — PR #113 / Deploy #200
7. Technology Capability Resolution — PR #115 / Deploy #201
8. Actor-backed Skill Capability Adapter — PR #117 / Deploy #202
9. Represented Skill Task Contract v1 — PR #119 / Deploy #203
10. **Skill Definition Refactor Batch v1 — PR #121 / Deploy #204**

Canonical stack:
- `config/skill_definitions.v1.json`
- `src/observer_sandbox/skill_definitions.py`
- `src/observer_sandbox/skill_application_requirements.py`
- `src/observer_sandbox/skill_capability.py`
- `src/observer_sandbox/actor_skill_capability.py`
- `config/represented_skill_tasks.v1.json`
- `src/observer_sandbox/represented_skill_tasks.py`

Canonical docs include:
- `docs/SKILL_DEFINITION_CAPABILITY_FRAMEWORK_V1.md`
- `docs/SKILL_CREATION_FORMAT_V1.md`
- `docs/SKILL_APPLICATION_REQUIREMENTS_V1.md`
- `docs/SKILL_CAPABILITY_RESOLUTION_V1.md`
- `docs/ACTOR_SKILL_CAPABILITY_ADAPTER_V1.md`
- `docs/REPRESENTED_SKILL_TASK_CONTRACT_V1.md`
- `docs/SKILL_DEFINITION_REFACTOR_BATCH_V1.md`.

## Current six gameplay-grade umbrella Skills

All current actor Skills now have validator-backed universal meaning, behavioral anchors, bounded applications, executable requirements, risk boundaries, and explicit learning-evidence policy.

Applications:
- H2H: `engage_unarmed_striking`, `control_unarmed_grapple`
- Weapons: `employ_familiar_melee_weapon`, `employ_familiar_ranged_weapon`
- Survival: `navigate_field_environment`, `establish_field_sustainment`
- Tactical Planning: `assess_tactical_situation`, `plan_tactical_maneuver`
- Technology: `diagnose_known_system_fault`
- Field Medicine: `assess_field_casualty`, `stabilize_for_evacuation`.

Application resource requirements support:
- `required_resource_mode: any` for genuinely required external resources;
- `required_resource_mode: none` for applications that do not require an external tool/resource.

Supporting resources remain optional and may change an otherwise eligible assessment from `constrained` to `supported` without becoming a hard gate.

## Subskill policy

Current application families are the initial **subskill-like gameplay surface**, not independently scored child Skills.

Do not split current parent scores into invented child values. Promote a true child Skill only when:
1. the task family is meaningfully separable;
2. legitimate learning evidence can distinguish it;
3. progression/retention can be independently owned;
4. parent/child aggregation and migration semantics are explicit.

`component_skills` remains empty for the current six definitions.

## Learning-evidence state

Active legitimate progression remains:
- H2H — structured Training Method evidence;
- Tactical Planning — VR Tactical Drills / AI Combat Simulation evidence;
- Technology — `systems_diagnostic_practice`.

Weapons, Survival, and Field Medicine now have semantic definitions but **no active progression producer**. Their definitions must not create XP from generic actions, names, model prose, or semantic similarity. Add progression only after legitimate represented evidence exists.

## Represented Skill Task Contract v1

First represented task:
`technology_known_system_fault_diagnostic_sim_v1`

It binds Technology `diagnose_known_system_fault` to exact target definition `represented_task:technology_known_fault_diagnostic_simulator_v1`, challenge `standard`, explicit context/resource semantics, low simulation-safe risk, and bounded outcomes.

No target entity is seeded yet. Existing Systems Diagnostic Practice Console remains practice/learning evidence only and cannot be promoted into application authority.

## Next development sequence

1. **Represented Skill Task Instance Resolver v1 — NEXT**;
2. prove exact target-entity binding and read-only actor assessment on synthetic entities;
3. add one distinct Technology simulator entity plus bounded action/application-evidence integration;
4. apply represented-task/action patterns to other Skills by structural equivalence, not one PR per Skill;
5. add missing Weapons/Survival/Field Medicine learning evidence/progression only when legitimate represented practice/task evidence exists;
6. later Skill retention/reacquisition and justified true subskill promotion;
7. later intellectual attributes, mental/emotion dynamics and broader social/relationship systems.

## Represented Skill Task Instance Resolver v1 — NEXT

Invariant:
`actor + task_id + target_entity_id + explicit available resource capabilities -> exact target type/definition/capability validation -> task challenge/context derivation -> actor-backed Skill capability assessment -> read-only represented-task assessment`

Constraints:
- exact `definition_id`; no name/model-prose matching;
- fail closed on missing/mismatched target, entity type, definition, or required target capability;
- do not reuse the practice console;
- synthetic target/entity tests are sufficient; no production seed for proof;
- available resource capabilities remain explicit until represented resource ownership is separately proven;
- no writes, action authorization, events/evidence, XP, autonomy or Telegram integration.

Expected assessment behavior for the Technology exemplar:
- required diagnostic capability absent -> unsupported;
- required capability present but supporting documentation absent -> constrained;
- required + supporting capabilities present -> supported, subject to actor proficiency/challenge support.

## Deferred boundaries

No full Knowledge Engine, second competency score, giant Skill tree, economy/jobs/quests, broad Mind/Behavior, deep crafting, partnered sexual behavior, detailed endocrine simulation, second production character solely for testing, or Tahoe exterior traversal as side effects.

## Exact resume point

**Skill Definition Refactor Batch v1 is complete/deployed through PR #121 / Deploy #204. All six current umbrella Skills now have gameplay-grade definitions while existing parent scores remain authoritative. Next implement Represented Skill Task Instance Resolver v1 as a read-only exact target-instance binding seam; do not seed the production simulator or wire live actions yet.**
