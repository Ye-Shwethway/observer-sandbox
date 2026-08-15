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

Latest runtime deployment: **Deploy #212 / run `31879753891` SUCCESS**, Controlled H2H Sparring Runtime v1, PR #134 merge `a4f8f8f84f71d77e87f7208bbac9546b3bdc4ca9`.

Verified post-deploy production evidence:
- service active/healthy; schema v5;
- autonomy enabled, normal mode, 1x, retry `null`;
- a pending autonomous action exists;
- cognition binding was preserved/resolved;
- Telegram API connectivity remained healthy;
- production `sandboxctl init` succeeded with the controlled-H2H action vocabulary seed path present in deployed code;
- live state continued naturally at `train` in the Home Gym;
- no live `spar` action was forced for validation;
- no production sparring partner or represented sparring-session fixture was fabricated solely for proof.

The exact production `spar` action-definition row was not separately queried in a dedicated read-only workflow. Full CI/fresh-DB tests prove exact action/task/participant behavior; production deployment/init proves that the candidate code path deployed successfully. Keep those evidence claims distinct.

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
17. Tactical Planning Represented Assessment Runtime v1 — PR #131 / Deploy #210
18. Represented Skill Runtime Batch v1 — PR #133 / Deploy #211
19. Controlled H2H Sparring Runtime v1 — PR #134 / Deploy #212.

Canonical execution stack now includes:
- Skill definition/application/capability + actor adapter;
- represented Skill task registry + exact instance resolver;
- cognition capability-awareness projection;
- bounded cognitive/performance modifier resolver;
- Technology diagnostic runtime;
- Tactical situation-assessment runtime;
- generic low-risk represented-Skill batch runtime;
- first bounded multi-actor controlled-H2H authorization/runtime exemplar;
- immutable application-evidence path separate from learning evidence.

## Current six gameplay-grade umbrella Skills

Applications:
- H2H: `engage_unarmed_striking`, `control_unarmed_grapple`
- Weapons: `employ_familiar_melee_weapon`, `employ_familiar_ranged_weapon`
- Survival: `navigate_field_environment`, `establish_field_sustainment`
- Tactical Planning: `assess_tactical_situation`, `plan_tactical_maneuver`
- Technology: `diagnose_known_system_fault`
- Field Medicine: `assess_field_casualty`, `stabilize_for_evacuation`.

## Represented Skill runtime state

### Technology exemplar — complete

Task: `technology_known_system_fault_diagnostic_sim_v1`
Application: `technology.diagnose_known_system_fault`
Action: `diagnose`
Target definition: `represented_task:technology_known_fault_diagnostic_simulator_v1`

This proved a tool/resource-centric represented runtime with `required_resource_mode: any` plus supporting documentation.

### Tactical Planning second exemplar — complete

Task: `tactical_situation_assessment_sim_v1`
Application: `tactical_planning.assess_tactical_situation`
Action: `assess`
Target definition: `represented_task:tactical_situation_assessment_simulator_v1`

This proved a cognitively heavy represented runtime with `required_resource_mode: none` plus supporting `situational_intelligence`.

### Represented Skill Runtime Batch v1 — complete

PR #133 / Deploy #211 proved batch-by-pattern reuse for:
- Tactical Planning `plan_tactical_maneuver`;
- Survival `navigate_field_environment`;
- Survival `establish_field_sustainment`.

The batch reused the task registry, exact instance resolver, action lifecycle, cognition awareness, bounded modifier resolver, deterministic outcome path and immutable application evidence. It added no movement execution, shelter mutation, resource consumption, combat consequence or automatic XP.

Represented-task resource contracts support `required_resource_mode: any|none` and preserve the underlying Skill application's mode. Supporting resources may distinguish constrained vs supported but never become hidden hard gates.

## Controlled H2H consequential exemplar — complete

Task: `h2h_controlled_striking_spar_v1`
Application: `hand_to_hand_combat.engage_unarmed_striking`
Action: `spar`
Session definition: `represented_task:h2h_controlled_striking_sparring_session_v1`

PR #134 / Deploy #212 introduced the first bounded represented-consequential interaction invariant:
- the exact represented session remains the object target;
- exactly one opponent is supplied through `Action.participants`;
- opponent must be a distinct represented character;
- opponent must be colocated with the actor;
- opponent must explicitly expose `controlled_sparring_consent`;
- authorization is deterministic and cannot be created by Skill score, model prose, IQ or a modifier;
- outcome is deterministic **scored contact only** in v1;
- no injury state or participant target state is mutated;
- no hostile/non-consensual combat behavior is authorized;
- no production partner/session was seeded solely for validation.

H2H performance modifiers use bounded Reflexes + Agility + Focus only after Skill/task/participant feasibility. IQ is intentionally absent, and legacy `raps_pa.combat_skill` is excluded so H2H Skill is not double-counted.

## Cognition and IQ boundary

Cognition receives a read-only semantic projection of actor Skill state plus canonical Skill definitions/applications, behavioral anchors, supported challenges, context/resource expectations, and explicit limits.

IQ/supporting Attributes are task-specific performance context only when a declared modifier contract names them. They cannot create Knowledge, proficiency, missing resources/context, consent, authorization, supported challenge capability or consequences.

Tactical represented tasks may use bounded IQ where explicitly declared. Survival and controlled H2H deliberately do not use IQ because their canonical task-relevant factors name other Attributes.

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

Represented task application evidence, including controlled sparring application evidence, remains immutable application evidence only and does not automatically become XP.

Weapons, Survival and Field Medicine have semantic definitions but no active progression producer. Do not invent progression merely because represented gameplay is added.

PR #134 also made the Skill Progression Foundation acceptance validator history-safe: the durable invariant is that the original zero-gain progression bootstrap exists, not that it must remain the latest H2H settlement after legitimate future training settlements occur.

## Training movement operational correction

PR #129 remains the production contract:
- authored method + no movement subcatalog -> auxiliary movement labels canonicalize to empty;
- explicit movement subcatalog -> strict exact movement-id validation;
- unknown/unbound target -> fail closed.

Do not regress this boundary while expanding Skill gameplay.

## Next development sequence

1. **Controlled H2H Pattern Expansion v1 — NEXT**.
2. Re-read the exact live `hand_to_hand_combat.control_unarmed_grapple` contract against the newly proven controlled-striking interaction invariant.
3. Reuse the participant channel, distinct-character requirement, colocation, explicit authorization, Skill authority, bounded modifiers, deterministic outcome and immutable application-evidence path wherever structurally equivalent.
4. If grapple introduces genuinely new restraint/control, injury, release, incapacity or authorization semantics, isolate that new invariant in one bounded exemplar rather than hiding it inside a nominal follow-on.
5. Do not pull Weapons or Field Medicine into the same slice merely for completeness; their weapon-resource/lethality and casualty/treatment consequences remain separate structural questions.
6. Keep application evidence separate from learning evidence and do not auto-award XP.
7. Do not add independently scored child Skills.
8. Continue to avoid synthetic production characters/actions solely to manufacture validation evidence.

## Deferred boundaries

No hostile/non-consensual combat engine, full injury engine, Weapons lethality system, Field Medicine casualty-state mutation, full Knowledge Engine, second competency score, giant Skill tree, economy/jobs/quests, broad Mind/Behavior rewrite, deep crafting, detailed endocrine expansion, second production character solely for testing, or Tahoe exterior traversal as side effects of this slice.

## Exact resume point

**Represented Skill Runtime Batch v1 is complete through PR #133 / Deploy #211. Controlled H2H Sparring Runtime v1 is complete through PR #134 merge `a4f8f8f84f71d77e87f7208bbac9546b3bdc4ca9` / Deploy #212 run `31879753891` SUCCESS. The first multi-actor explicit-authorization/scored-contact invariant is now proven without injury mutation or automatic XP. Next inspect `control_unarmed_grapple` for structural equivalence; reuse the pattern if equivalent, otherwise isolate any genuinely new restraint/control/consequence invariant.**
