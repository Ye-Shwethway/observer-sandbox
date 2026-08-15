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

Latest runtime deployment: **Deploy #212 / run `31879753891` SUCCESS**, Controlled H2H Sparring Runtime v1, PR #134 merge `a4f8f8f84f71d77e87f7208bbac9546b3bdc4ca9`.

Post-deploy evidence:
- service active/healthy, schema v5;
- autonomy enabled in normal mode at 1x;
- `autonomy_retry` is `null` and a pending action exists;
- cognition binding was preserved/resolved successfully;
- Telegram API connectivity remained healthy;
- production initialization completed successfully with controlled-H2H action vocabulary seed code active;
- live state continued naturally at `train` in the Home Gym;
- no live `spar` action was forced for proof;
- no production sparring partner or represented sparring-session fixture was fabricated solely for validation.

The exact production `spar` action-definition row was not separately queried in a dedicated read-only workflow. Exact H2H contract/action/participant behavior is proven by full CI, fresh-DB `init`/`status`, and focused runtime tests; do not overstate the live evidence.

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

Recent Skill/runtime line:
- Skill Definition Refactor Batch v1 — PR #121 / Deploy #204
- Represented Skill Task Instance Resolver v1 — PR #123 / Deploy #205
- Cognition Capability Awareness v1 — PR #124 / Deploy #206
- Cognitive / Performance Modifier Contract v1 — PR #125 / Deploy #207
- Technology Represented Diagnostic Task Runtime v1 — PR #126 / Deploy #208
- sanitized autonomy-error readback — PR #127, corrected by PR #128
- Training Movement Contract Normalization v1 — PR #129 / Deploy #209
- Tactical Planning Represented Assessment Runtime v1 — PR #131 / Deploy #210
- Represented Skill Runtime Batch v1 — PR #133 / Deploy #211
- Controlled H2H Sparring Runtime v1 — PR #134 / Deploy #212.

## Represented Skill runtime state

### Low-risk represented pattern — complete and batched

Technology diagnostic and Tactical assessment established structurally different `required_resource_mode: any|none` exemplars. PR #133 then applied the proven pattern in one batch to:
- `tactical_planning.plan_tactical_maneuver`;
- `survival.navigate_field_environment`;
- `survival.establish_field_sustainment`.

The batch reuses exact represented target/context/resource resolution, cognition awareness, bounded modifiers, deterministic outcomes and immutable application evidence without movement execution, shelter mutation, represented-resource consumption or automatic XP.

### Controlled H2H consequential exemplar — complete

Task: `h2h_controlled_striking_spar_v1`
Application: `hand_to_hand_combat.engage_unarmed_striking`
Action: `spar`
Session definition: `represented_task:h2h_controlled_striking_sparring_session_v1`

The first bounded multi-actor authorization invariant is now proven:
- represented sparring session remains the exact object target;
- one opponent is carried in `Action.participants`;
- opponent must be a distinct represented character;
- opponent must be colocated;
- opponent must expose explicit `controlled_sparring_consent`;
- authorization is deterministic and separate from Skill/performance scoring;
- outcome is scored contact only;
- no injury or participant target state mutation occurs in v1;
- no hostile/non-consensual combat is authorized;
- no production test character/session was created just to prove the feature.

H2H Skill score 90/S remains learned-capability authority. Bounded performance factors are Reflexes + Agility + Focus only. IQ is not used; legacy `raps_pa.combat_skill` is excluded.

## Cognition / IQ state

Cognition receives read-only semantic capability awareness: definition scope/exclusions, application families, behavioral anchors, challenge/context/resource boundaries, and relevant performance context.

IQ is not Skill or Knowledge. It can only affect an explicit task-specific modifier contract after deterministic Skill/task feasibility is established. It cannot create consent, authorization, resources, missing context, knowledge or consequences.

Do not apply a universal IQ bonus. Tactical represented tasks may use bounded IQ when declared; Survival and controlled H2H deliberately do not.

## Evidence boundary

Runtime application completion may emit immutable `skill_application_evidence`. That is **not learning evidence** and does not automatically award XP.

Active legitimate progression remains:
- H2H — structured Training Method evidence;
- Tactical Planning — VR Tactical Drills / AI Combat Simulation;
- Technology — `systems_diagnostic_practice`.

Controlled sparring application evidence does not become H2H XP automatically. Weapons, Survival and Field Medicine definitions do not activate XP by themselves.

PR #134 also corrected the Skill Progression Foundation acceptance validator so it requires the durable historical zero-gain bootstrap to exist rather than incorrectly requiring bootstrap to remain the latest H2H settlement after legitimate later training.

## Training movement recovery contract

PR #129 remains active:
- authored training method with no movement subcatalog -> auxiliary `training_movements` canonicalizes to empty;
- explicit movement subcatalog -> strict exact movement-id validation;
- unknown/unbound target -> fail closed.

## Next canonical direction

**Controlled H2H Pattern Expansion v1** is next.

First inspect the exact live `hand_to_hand_combat.control_unarmed_grapple` application contract against the new controlled-striking interaction pattern.

If structurally equivalent, reuse the same participant channel, distinct-character + colocation + explicit-authorization checks, Skill authority, bounded task-specific modifiers, deterministic outcome and immutable application-evidence path rather than creating another parallel engine.

If grapple introduces genuinely new restraint/control, release, incapacity, injury or authorization semantics, treat that as a new bounded structural invariant instead of hiding it inside a nominal follow-on.

Do not pull Weapons or Field Medicine into the same slice for completeness. Preserve:
- Skill score as learned-capability authority;
- exact represented target/context/resource binding;
- explicit participant authorization for consequential interaction;
- bounded explicit modifiers only where task-relevant;
- application evidence != learning evidence;
- no invented child Skill scores;
- no production forcing/fabricated second character for proof.

## Exact resume point

**Represented Skill Runtime Batch v1 is complete through PR #133 / Deploy #211. Controlled H2H Sparring Runtime v1 is complete through PR #134 merge `a4f8f8f84f71d77e87f7208bbac9546b3bdc4ca9` / Deploy #212 run `31879753891` SUCCESS. Reconcile current repo/production, then inspect `control_unarmed_grapple` for structural equivalence to the proven explicit-consent/colocation/scored-contact participant pattern; reuse it if equivalent, otherwise isolate any genuinely new restraint/control/consequence invariant.**
