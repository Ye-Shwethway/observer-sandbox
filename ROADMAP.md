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

Latest runtime deployment: **Deploy #209 / run `31877214780` SUCCESS**, Training Movement Contract Normalization v1, PR #129 merge `17dd3363467e82fb0fdf099316f619b0757ca5b5`.

Verified production state after natural retry recovery:
- service active/healthy; schema v5;
- autonomy enabled in normal mode at 1x;
- the pre-existing `training_movements` ValueError retry loop recovered naturally without a manual retry reset;
- read-only post-deploy check showed `current_retry: null` and a newly planned pending action;
- no newer autonomy error replaced the historical movement-mismatch events at that recovery boundary;
- cognition binding and Telegram connectivity remained intact;
- Technology diagnostic simulator/action seed remained present;
- no live diagnostic/tactical action was forced for proof.

Production parent Skill state remains authoritative:
- H2H `90 / S`
- Weapons `87 / A`
- Survival `85 / A`
- Tactical Planning `92 / S`
- Technology `82 / A`
- Field Medicine `75 / A`.

Relevant reasoning context remains present, including IQ 140, problem solving 88, focus 92, and adaptability 85. These values are not replacement Skill scores.

## Skill authority / ontology

- `character_skills.score` = authoritative learned proficiency;
- `character_skills.experience` = legitimate accumulated learning evidence;
- persisted `tier` = compatibility only;
- grade = read-time `skill-proficiency-100-v1`.

Ability/Attribute != Knowledge != Skill != Task/Application != demonstrated reliability. No second competency score exists. Legacy RAPS skill-like fields remain compatibility/provenance only and are not independent Skill truth.

## Completed Skill / cognition / represented-task chain

1. H2H Skill Progression v1 — PR #104 / Deploy #196
2. Tactical Planning Skill Progression — PR #106 / Deploy #197
3. Skill Evidence Semantics / Technology practice — PR #108 / Deploy #198
4. Skill Definition & Capability Framework — PR #110
5. Skill Creation Format / Technology definition — PR #111 / Deploy #199
6. Skill Application Requirements — PR #113 / Deploy #200
7. Technology Capability Resolution — PR #115 / Deploy #201
8. Actor-backed Skill Capability Adapter — PR #117 / Deploy #202
9. Represented Skill Task Contract v1 — PR #119 / Deploy #203
10. Skill Definition Refactor Batch v1 — PR #121 / Deploy #204
11. Represented Skill Task Instance Resolver v1 — PR #123 / Deploy #205
12. Cognition Capability Awareness v1 — PR #124 / Deploy #206
13. Cognitive / Performance Modifier Contract v1 — PR #125 / Deploy #207
14. Technology Represented Diagnostic Task Runtime v1 — PR #126 / Deploy #208
15. Sanitized Autonomy Error Readback — PR #127, corrected by PR #128
16. Training Movement Contract Normalization v1 — PR #129 / Deploy #209

Canonical execution stack now includes:
- `config/skill_definitions.v1.json`
- `src/observer_sandbox/skill_definitions.py`
- `src/observer_sandbox/skill_application_requirements.py`
- `src/observer_sandbox/skill_capability.py`
- `src/observer_sandbox/actor_skill_capability.py`
- `config/represented_skill_tasks.v1.json`
- `src/observer_sandbox/represented_skill_tasks.py`
- `src/observer_sandbox/represented_skill_task_instance.py`
- cognition capability-awareness projection;
- bounded cognitive/performance modifier resolver;
- Technology represented diagnostic runtime/application-evidence path.

Canonical docs include:
- `docs/SKILL_DEFINITION_CAPABILITY_FRAMEWORK_V1.md`
- `docs/SKILL_CREATION_FORMAT_V1.md`
- `docs/SKILL_APPLICATION_REQUIREMENTS_V1.md`
- `docs/SKILL_CAPABILITY_RESOLUTION_V1.md`
- `docs/ACTOR_SKILL_CAPABILITY_ADAPTER_V1.md`
- `docs/REPRESENTED_SKILL_TASK_CONTRACT_V1.md`
- `docs/REPRESENTED_SKILL_TASK_INSTANCE_RESOLVER_V1.md`
- `docs/SKILL_DEFINITION_REFACTOR_BATCH_V1.md`
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

Application resource requirements support `required_resource_mode: any|none`; supporting resources may change an eligible result from constrained to supported without becoming hidden hard gates.

## Cognition and IQ boundary

Cognition now receives a read-only semantic projection of actor Skill state plus canonical Skill definitions/applications, current behavioral anchors, supported challenges, context/resource expectations, and explicit limits.

IQ and supporting Attributes are task-specific reasoning/performance context only when a declared modifier contract names them. They must not:
- create Knowledge;
- create or increase learned Skill proficiency;
- satisfy missing target/context/resource requirements;
- upgrade an unsupported task to supported;
- become a universal unrelated-task bonus.

The first Technology modifier contract uses bounded reasoning/precision/adaptation dimensions. V1 modifier effects are explicit and capped; deterministic task outcome remains final authority.

## Represented Skill runtime state

### Technology exemplar — complete

`technology_known_system_fault_diagnostic_sim_v1`

Runtime flow:
`cognition awareness -> legal diagnose action option -> exact represented target binding -> Technology capability -> bounded cognitive modifiers -> deterministic outcome -> action completion -> immutable skill_application_evidence`

Purpose-built production target:
`obj_thorne_estate_intel_known_fault_diagnostic_simulator`

Exact definition:
`represented_task:technology_known_fault_diagnostic_simulator_v1`

The existing Systems Diagnostic Practice Console remains practice/learning evidence only and is not application authority.

Application evidence is separate from learning evidence. The Technology runtime does not grant XP merely because an application completed.

## Training movement operational correction

Production exposed a pre-existing cognition retry loop when a valid authored training method with no movement/anatomy subcatalog received a human-semantic auxiliary label such as `sparring`.

PR #129 established the contract:
- authored method + no movement subcatalog -> auxiliary `training_movements` canonicalizes to empty;
- explicit movement subcatalog -> strict exact movement-id validation;
- unknown/unbound training target -> fail closed.

This changes no action target, method, duration, progression formula, or evidence authority. Production naturally recovered after the previous retry backoff expired.

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

Weapons, Survival, and Field Medicine have semantic definitions but no active progression producer. Generic actions, names, model prose, or application evidence must not silently become XP.

## Next development sequence

1. **Tactical Planning Represented Assessment Runtime v1 — NEXT**;
2. use `tactical_planning.assess_tactical_situation` as the second represented gameplay exemplar;
3. seed a distinct low-risk represented tactical assessment simulator/scenario rather than reusing Tactical training/practice targets;
4. reuse proven represented-task/action/application-evidence structure where structurally equivalent;
5. declare only task-relevant cognitive factors (likely IQ/problem solving/focus/adaptability/tactical reasoning) with bounded modifier effects;
6. emit immutable application evidence separate from existing Tactical learning evidence;
7. do not auto-award XP from application evidence;
8. after the second exemplar, decide which equivalent Skill runtimes can be batched rather than creating one bespoke PR per Skill;
9. add Weapons/Survival/Field Medicine progression only when legitimate represented learning evidence exists;
10. later address retention/reacquisition and justified true subskill promotion.

## Tactical Planning Represented Assessment Runtime v1 — NEXT

Target application:
`tactical_planning.assess_tactical_situation`

Required invariants:
- purpose-built represented target with exact definition binding;
- simulation-safe / low-risk first exemplar;
- cognition sees both semantic Tactical capability and a concrete legal action only when physically/contextually available;
- deterministic Skill capability remains feasibility authority;
- IQ and supporting Attributes shape only explicitly declared performance dimensions;
- no random `Skill score = success percent` shortcut;
- immutable application evidence on actual completion;
- application evidence != learning evidence;
- no child Skill creation;
- no production action forced for validation.

The second exemplar is intended to prove that the runtime pattern is generic beyond a tool-heavy Technology task before broader batch-by-pattern integration.

## Deferred boundaries

No full Knowledge Engine, second competency score, giant Skill tree, economy/jobs/quests, broad Mind/Behavior rewrite, deep crafting, detailed endocrine expansion, second production character solely for testing, or Tahoe exterior traversal as side effects of this Skill-runtime line.

## Exact resume point

**Technology represented gameplay, cognition capability awareness, bounded IQ/supporting-factor performance modifiers, and production autonomy recovery are complete through PR #129 / Deploy #209. Next implement one distinct Tactical Planning `assess_tactical_situation` represented runtime exemplar; do not reuse Tactical training targets, do not create child scores, and do not turn application evidence into XP.**
