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

Latest runtime deployment: **Deploy #210 / run `31878236282` SUCCESS**, Tactical Planning Represented Assessment Runtime v1, PR #131 merge `aef123dc7840b69091c7264988b744c69d955396`.

Post-deploy evidence:
- service active/healthy, schema v5;
- autonomy enabled in normal mode at 1x;
- `autonomy_retry` is `null` and a pending action exists;
- cognition binding was preserved and resolved successfully;
- Telegram API connectivity remained healthy;
- production initialization completed successfully with the Tactical runtime seed code active;
- no live Tactical action was forced for proof.

The exact Tactical production seed row was not separately queried in a dedicated read-only workflow during this checkpoint. Exact seed/action behavior is proven by full CI, fresh-DB `init`/`status`, and Tactical runtime tests; do not overstate the live evidence.

`main` and `test` are synchronized at `aef123dc7840b69091c7264988b744c69d955396` before this documentation checkpoint.

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
- Training Movement Contract Normalization v1 — PR #129 / Deploy #209
- Tactical Planning Represented Assessment Runtime v1 — PR #131 / Deploy #210.

Canonical docs for this line include:
- `docs/SKILL_DEFINITION_REFACTOR_BATCH_V1.md`
- `docs/REPRESENTED_SKILL_TASK_CONTRACT_V1.md`
- `docs/REPRESENTED_SKILL_TASK_INSTANCE_RESOLVER_V1.md`
- `docs/COGNITION_CAPABILITY_AWARENESS_V1.md`
- `docs/COGNITIVE_PERFORMANCE_MODIFIER_CONTRACT_V1.md`
- `docs/TECHNOLOGY_DIAGNOSTIC_TASK_RUNTIME_V1.md`
- `docs/TACTICAL_ASSESSMENT_TASK_RUNTIME_V1.md`.

## Represented Skill runtime state

### Technology exemplar — complete

Task: `technology_known_system_fault_diagnostic_sim_v1`
Action: `diagnose`
Target: `obj_thorne_estate_intel_known_fault_diagnostic_simulator`
Definition: `represented_task:technology_known_fault_diagnostic_simulator_v1`

### Tactical Planning second exemplar — complete

Task: `tactical_situation_assessment_sim_v1`
Application: `tactical_planning.assess_tactical_situation`
Action: `assess`
Target: `obj_thorne_estate_intel_tactical_situation_assessment_simulator`
Definition: `represented_task:tactical_situation_assessment_simulator_v1`

The Tactical exemplar is deliberately distinct from Tactical training/practice targets. It proved the represented-task pattern can generalize beyond a tool-heavy Technology task to a cognitively heavy task with no hard external resource requirement.

Represented-task resource contracts now explicitly support `required_resource_mode: any|none` while preserving the underlying Skill application's mode. Supporting resources may make an otherwise eligible result constrained vs supported but cannot bypass hard requirements.

## Cognition / IQ state

Cognition receives read-only semantic capability awareness: definition scope/exclusions, application families, behavioral anchors, challenge/context/resource boundaries, and relevant reasoning context.

IQ is not Skill or Knowledge. It can only affect an explicit task-specific modifier contract after deterministic Skill/task feasibility is established.

Current Tactical assessment modifiers use bounded:
- IQ;
- Problem Solving;
- Focus;
- Adaptability.

Legacy `raps_ia.tactical_thinking` is intentionally excluded from Tactical modifiers so the authoritative Tactical Planning Skill is not double-counted.

## Evidence boundary

Runtime application completion may emit immutable `skill_application_evidence`. That is **not learning evidence** and does not automatically award XP.

Active legitimate progression remains:
- H2H — structured Training Method evidence;
- Tactical Planning — VR Tactical Drills / AI Combat Simulation;
- Technology — `systems_diagnostic_practice`.

Weapons, Survival and Field Medicine definitions do not activate XP by themselves. Generic actions, represented application evidence, object names, and model prose are not learning evidence.

## Training movement recovery contract

PR #129 remains active:
- authored training method with no movement subcatalog -> auxiliary `training_movements` canonicalizes to empty;
- explicit movement subcatalog -> strict exact movement-id validation;
- unknown/unbound target -> fail closed.

Production recovered naturally after the previous retry backoff; no manual retry reset was used.

## Next canonical direction

The Technology and Tactical exemplars have now proven the core represented-Skill runtime pattern across two structurally different cases. **Do not create a third bespoke exemplar by default. Move to batch-by-pattern.**

Next work should first inspect the remaining Skill applications and form one bounded batch of structurally equivalent **low-risk / simulation-safe** represented runtimes. Prefer applications whose target/context/resource/outcome contracts fit the proven pattern without introducing a genuinely new safety or consequence invariant.

Likely candidates should be evaluated from live canonical definitions rather than hard-coded from chat memory. Higher-risk H2H/Weapons consequential use should not be smuggled into this batch merely for completeness. Weapons/Survival/Field Medicine progression remains separate and requires legitimate learning evidence before XP activation.

Preserve:
- Skill score as learned-capability authority;
- exact represented target/context/resource binding;
- bounded explicit modifiers only where task-relevant;
- application evidence != learning evidence;
- no invented child Skill scores;
- no production forcing for proof.

## Exact resume point

**Represented-Skill gameplay is complete through Tactical Planning Represented Assessment Runtime v1, PR #131 / Deploy #210. The two-exemplar pattern is proven. Reconcile live repo/production, then design and implement the next minimum-runnable batch of structurally equivalent low-risk represented Skill applications under the existing deterministic Skill/cognition/evidence contracts.**
