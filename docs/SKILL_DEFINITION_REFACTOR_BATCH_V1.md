# Skill Definition Refactor Batch v1

Status: COMPLETE / DEPLOYED
Date: 2026-08-15

## Purpose

Move the five remaining current umbrella Skills from actor-score-only or progression-only state into the validator-backed gameplay definition format proven by Technology, before broad action/task integration.

Batch:
- Hand-to-Hand Combat
- Weapons
- Survival
- Tactical Planning
- Field Medicine

Technology remains the exemplar and was updated only to make its required-resource mode explicit.

## Core decision: applications before scored subskills

The current `character_skills.score` rows remain authoritative parent proficiency. This batch does **not** split any current parent score into child values.

Initial gameplay granularity is represented by bounded application families under each umbrella Skill:
- H2H: `engage_unarmed_striking`, `control_unarmed_grapple`
- Weapons: `employ_familiar_melee_weapon`, `employ_familiar_ranged_weapon`
- Survival: `navigate_field_environment`, `establish_field_sustainment`
- Tactical Planning: `assess_tactical_situation`, `plan_tactical_maneuver`
- Field Medicine: `assess_field_casualty`, `stabilize_for_evacuation`
- Technology remains `diagnose_known_system_fault`.

A true scored child Skill should be introduced only when its task family has independently distinguishable learning evidence, progression/retention ownership, and explicit parent/child aggregation plus migration semantics. Parent scores are never copied into children automatically.

## Resource requirement generalization

Technology exposed a structural assumption in the first executable application contract: every application previously required at least one external resource capability.

That is not universally true. H2H striking, tactical assessment, field navigation, and casualty assessment may be semantically valid without an external required tool.

Application requirements now declare:
- `required_resource_mode: any` — at least one listed `resource_capabilities_any` must be available;
- `required_resource_mode: none` — no external required resource capability exists and the list must be empty.

Supporting resources remain optional and can change an otherwise eligible assessment from `constrained` to `supported` without becoming a hard gate.

## Authority and compatibility

Actor state remains unchanged:
- `character_skills.score` = proficiency authority;
- `character_skills.experience` = legitimate learning evidence accumulation;
- grade = read-time `skill-proficiency-100-v1`;
- persisted tier = compatibility only.

Legacy skill-like RAPS fields remain provenance/compatibility only and are deliberately excluded from Ability/Attribute dependencies:
- `raps_pa.combat_skill`
- `raps_pa.weapons_proficiency`
- `raps_pa.survival_skill`
- `raps_ia.tactical_thinking`
- `raps_ia.technological_aptitude`
- `raps_ia.medical_knowledge`

Definitions instead reference true underlying capacities such as reflexes, agility, focus, adaptability, problem solving, endurance, and emotional stability.

## Learning-evidence preservation

This batch is semantic definition work, not a progression expansion.

Preserved active evidence paths:
- H2H: existing structured Training Method progression evidence;
- Tactical Planning: existing VR Tactical Drills / AI Combat Simulation progression evidence;
- Technology: existing `systems_diagnostic_practice` evidence.

No new evidence producer was activated for:
- Weapons
- Survival
- Field Medicine

Those definitions declare future `supervised_application` as an allowed evidence family, but generic actions, names, model prose, and the definition itself cannot award XP or mutate score.

## Risk boundaries

Weapons and Field Medicine applications are marked high-risk at the universal definition layer. Their Skill score is capability input only and never independent authorization for consequential use.

Field Medicine definitions are simulation/gameplay semantics, not medical advice. Real-world medical authority is not implied.

## Validation / deployment

PR #121: `refactor current Skill definitions for gameplay semantics`

Final tested head:
`0ca8875d35349d02975e8e80929300fbdd9b6507`

Merge:
`3eb94d408c6d207610cb17920ae16dd42172b6e4`

PR gates — all first-attempt SUCCESS:
- Skill Definition Refactor Batch v1 Acceptance #1 / run `31874524536`
- CI #826 / run `31874524531`
- Skill Application Requirements v1 Acceptance #3 / run `31874524508`
- Skill Definition Format v1 Acceptance #5 / run `31874524483`
- Technology Capability Resolution v1 Acceptance #3 / run `31874524477`
- Actor Skill Capability Adapter v1 Acceptance #3 / run `31874524491`
- Represented Skill Task Contract v1 Acceptance #3 / run `31874524496`
- Strength Live Cycle Validation v1 #39 / run `31874524516`
- Public Readiness Security Audit #78 / run `31874524485`

Post-merge:
- Skill Definition Refactor Batch v1 Acceptance #2 / run `31874569354`: SUCCESS
- CI #827 / run `31874569313`: SUCCESS
- Deploy #204 / run `31874569397`: SUCCESS

## Production readback after Deploy #204

Verified read-only deployment evidence:
- exact deployed commit `3eb94d408c6d207610cb17920ae16dd42172b6e4`;
- service active/healthy;
- schema v5;
- autonomy enabled, normal, 1.0x;
- Telegram API/config and cognition binding preserved;
- current parent Skill values remained unchanged:
  - Hand-to-Hand Combat `90.0 / S Expert`
  - Weapons `87.0 / A Advanced`
  - Survival `85.0 / A Advanced`
  - Tactical Planning `92.0 / S Expert`
  - Technology `82.0 / A Advanced`
  - Field Medicine `75.0 / A Advanced`.

No live action, learning evidence, score mutation, XP migration, or child Skill creation was forced to prove this batch.

## Acceptance invariants proven

- registry covers exactly the six current actor umbrella Skills;
- all five new definitions pass universal definition and executable application validators;
- existing parent scores remain `90 / 87 / 85 / 92 / 82 / 75`;
- no `component_skills` or child actor rows were fabricated;
- legacy skill-like RAPS fields are not Ability dependencies;
- only H2H, Tactical Planning, and Technology remain in the current progression config;
- a no-resource H2H application can resolve as supported;
- an optional navigation aid changes Survival navigation from constrained to supported;
- a required weapon capability remains a real hard gate;
- existing represented Technology task contract remains valid.

## Next

Resume **Represented Skill Task Instance Resolver v1** as the generic read-only target-instance binding seam before live action integration.
