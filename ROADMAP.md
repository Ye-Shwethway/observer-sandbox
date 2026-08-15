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

Latest runtime deployment: **Deploy #210 / run `31878236282` SUCCESS**, Tactical Planning Represented Assessment Runtime v1, PR #131 merge `aef123dc7840b69091c7264988b744c69d955396`.

Verified post-deploy production evidence:
- service active/healthy; schema v5;
- autonomy enabled, normal mode, 1x, retry `null`;
- a pending autonomous action exists;
- cognition binding was preserved/resolved;
- Telegram API connectivity remained healthy;
- production `sandboxctl init` succeeded with the Tactical seed path present in deployed code;
- no live Tactical action was forced for validation.

The exact Tactical seed row was not separately queried read-only in this checkpoint. Full CI/fresh-DB tests prove exact seed/action behavior; production deployment/init proves the code path deployed successfully. Keep those evidence claims distinct.

Production parent Skill state remains authoritative:
- H2H `90 / S`
- Weapons `87 / A`
- Survival `85 / A`
- Tactical Planning `92 / S`
- Technology `82 / A`
- Field Medicine `75 / A`.

Relevant general reasoning context remains IQ 140, Problem Solving 88, Focus 92, Adaptability 85. These are supporting context, not replacement Skill scores.

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
17. Tactical Planning Represented Assessment Runtime v1 — PR #131 / Deploy #210.

Canonical execution stack includes:
- Skill definition/application/capability + actor adapter;
- represented Skill task registry + instance resolver;
- cognition capability-awareness projection;
- bounded cognitive/performance modifier resolver;
- Technology diagnostic runtime;
- Tactical situation-assessment runtime;
- immutable application-evidence path separate from learning evidence.

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
- `docs/TECHNOLOGY_DIAGNOSTIC_TASK_RUNTIME_V1.md`
- `docs/TACTICAL_ASSESSMENT_TASK_RUNTIME_V1.md`.

## Current six gameplay-grade umbrella Skills

Applications:
- H2H: `engage_unarmed_striking`, `control_unarmed_grapple`
- Weapons: `employ_familiar_melee_weapon`, `employ_familiar_ranged_weapon`
- Survival: `navigate_field_environment`, `establish_field_sustainment`
- Tactical Planning: `assess_tactical_situation`, `plan_tactical_maneuver`
- Technology: `diagnose_known_system_fault`
- Field Medicine: `assess_field_casualty`, `stabilize_for_evacuation`.

## Represented-task foundation after second exemplar

Represented-task resource contracts now support `required_resource_mode: any|none` and must preserve the underlying Skill application's resource mode.

Supporting resources may distinguish constrained from supported outcomes but do not become hidden hard gates. Exact target definition/capability, context, actor Skill state and challenge support remain deterministic authority.

### Technology exemplar — complete

Task: `technology_known_system_fault_diagnostic_sim_v1`
Application: `technology.diagnose_known_system_fault`
Action: `diagnose`
Target definition: `represented_task:technology_known_fault_diagnostic_simulator_v1`

This proved a tool/resource-centric represented runtime with one hard resource-any requirement plus supporting documentation.

### Tactical Planning second exemplar — complete

Task: `tactical_situation_assessment_sim_v1`
Application: `tactical_planning.assess_tactical_situation`
Action: `assess`
Target definition: `represented_task:tactical_situation_assessment_simulator_v1`

This proved a cognitively heavy represented runtime with `required_resource_mode: none` plus supporting `situational_intelligence`. The simulator is distinct from Tactical learning/practice targets.

The second exemplar demonstrates that the core runtime structure generalizes across materially different resource shapes. Under the expansion policy, the next structurally equivalent follow-ons should therefore be batched rather than implemented as one bespoke exemplar per Skill.

## Cognition and IQ boundary

Cognition receives a read-only semantic projection of actor Skill state plus canonical Skill definitions/applications, behavioral anchors, supported challenges, context/resource expectations, and explicit limits.

IQ/supporting Attributes are task-specific performance context only when a declared modifier contract names them. They cannot create Knowledge, proficiency, missing resources/context, authorization, or supported challenge capability.

Tactical assessment uses bounded IQ + Problem Solving + Focus + Adaptability modifiers. Legacy `raps_ia.tactical_thinking` is intentionally excluded so Tactical Planning Skill is not double-counted.

## Subskill policy

Current application families are the initial subskill-like gameplay surface, not independently scored child Skills.

Do not split parent scores into invented child values. Promote a true child Skill only when:
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

Represented task application evidence remains immutable application evidence only and does not automatically become XP.

Weapons, Survival and Field Medicine have semantic definitions but no active progression producer. Do not invent progression merely because represented gameplay is added.

## Training movement operational correction

PR #129 remains the production contract:
- authored method + no movement subcatalog -> auxiliary movement labels canonicalize to empty;
- explicit movement subcatalog -> strict exact movement-id validation;
- unknown/unbound target -> fail closed.

Production recovered naturally after its previous retry backoff. Do not regress this boundary while expanding Skill gameplay.

## Next development sequence

1. **Represented Skill Runtime Batch v1 — NEXT**.
2. Re-read remaining current Skill applications and group only structurally equivalent low-risk / simulation-safe candidates that fit the now-proven task/action/evidence pattern.
3. Prefer one branch / PR / focused regression set / merge / deploy-readback for the batch.
4. Reuse the represented-task registry, exact instance resolver, action lifecycle, cognition awareness, bounded modifier contracts and immutable application-evidence path rather than creating domain-specific parallel engines.
5. Add task-specific cognitive/physical factors only where canonical Skill definitions justify them; do not apply a universal IQ bonus.
6. Keep application evidence separate from learning evidence and do not auto-award XP.
7. Do not add independently scored child Skills.
8. Do not include higher-risk consequential H2H/Weapons use merely to complete a checklist; new safety/consequence invariants require their own bounded exemplar if genuinely novel.
9. Survival / Field Medicine / remaining Tactical applications may be candidates only after checking their exact live contracts and whether they introduce new structural invariants.
10. Later: add Weapons/Survival/Field Medicine progression only when legitimate represented learning evidence exists; address retention/reacquisition and justified true subskill promotion separately.

## Deferred boundaries

No full Knowledge Engine, second competency score, giant Skill tree, economy/jobs/quests, broad Mind/Behavior rewrite, deep crafting, detailed endocrine expansion, second production character solely for testing, or Tahoe exterior traversal as side effects of this Skill-runtime line.

## Exact resume point

**Technology diagnostic and Tactical assessment represented runtimes are complete through PR #131 / Deploy #210. The two-exemplar pattern is proven across `required_resource_mode: any` and `none`. Next reconcile live definitions and implement one bounded batch of structurally equivalent low-risk represented Skill applications; keep Skill authority, exact task binding, bounded modifiers, application-vs-learning evidence separation, and no-child-score invariants intact.**
