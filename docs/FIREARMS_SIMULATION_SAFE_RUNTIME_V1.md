# Firearms Simulation-Safe Runtime v1

Status: COMPLETE
Date: 2026-08-15

## Purpose

Activate the first executable Firearms application as a bounded simulation-safe follow-on to the proven Bladed Weapons pattern, without introducing hostile combat, lethality, injury, ammunition economy, or real-world firearm technique semantics.

## Canonical authority

`Weapon Mastery` remains a derived, non-executable parent.

Executable familiar-ranged authority moved from the hidden legacy `weapons` compatibility projection to:

`firearms.employ_familiar_ranged_weapon`

The Firearms component owns learned proficiency. The legacy umbrella cannot independently execute the ranged application.

## Represented task

- task: `firearms_safe_handling_sim_v1`
- action: `firearm_drill`
- room: Thorne Estate Training Hall
- exact target definition: `represented_task:firearms_safe_handling_simulator_v1`
- exact required training capability: `usable_firearms_training_weapon`
- task mode: `simulation_safe`
- challenge: `standard`
- risk: `low`
- outcome dimensions: `quality_precision`, `partial_failure_recovery`

The target is a represented training/simulation object. This slice does not model a real firearm, ammunition, projectile behavior, hostile targets, wounds, or operational firing procedures.

## Performance authority

The Firearms component score is the sole performance authority for this exemplar.

No cognitive or Attribute modifier contract was added merely because such fields exist. This avoids hidden bonuses and preserves the project rule that Attributes influence a task only when an exact task contract declares them.

## Evidence semantics

Successful completion emits deterministic Skill application evidence:

- Skill: `firearms`
- application: `employ_familiar_ranged_weapon`
- represented task and exact target identity retained
- `learning_evidence=false`

Ordinary `firearm_drill` therefore does not grant Firearms XP. A separate explicit practice producer is required for progression.

## Validation boundaries

Focused regressions prove that the runtime:

- resolves executable authority to `firearms`, not legacy `weapons`;
- requires the exact represented simulator definition;
- requires `usable_firearms_training_weapon`;
- fails closed when the target, resource capability, or authoritative Firearms Skill state is missing;
- exposes the action to cognition only through the represented target/action option path;
- uses the authoritative Firearms score for deterministic outcome indices;
- emits application evidence without learning evidence;
- is idempotent for repeated action IDs;
- does not mutate Weapon Mastery, Bladed Weapons, Firearms XP, or unrelated world state merely from application completion.

Final PR validation:
- PR #156 final tested head `33c52000595f00f36687afef670ebf105dd5f9c2`;
- CI #912 / run `31891065742`: SUCCESS;
- 525 tests passed in 31.20s;
- fresh DB init/status healthy; schema v5;
- Strength Live Cycle Validation #67 / run `31891065783`: SUCCESS;
- merge `ea5dad4fb49180e37eaff5435bd82c8f0c4a487e`.

## Production evidence

Deploy #223 / run `31891128059`: SUCCESS.

Verified readback after deployment:
- service healthy; schema v5;
- autonomy enabled in normal mode;
- speed 5x;
- sim time `2025-05-06T18:56:00+00:00`;
- Darian naturally sleeping in Darian's Master Suite;
- Gemini primary, Groq fallback, and Telegram connectivity healthy;
- Bladed Weapons 87/A;
- Firearms 87/A;
- Weapon Mastery 87/A;
- overall Skills A / 85.167.

No production `firearm_drill` was forced for proof. Unchanged Skill scores are expected; deployment proves safe loading and continuity, while application/no-XP semantics are fixture/CI evidence.

## Deferred boundaries

Not part of this slice:
- Firearms progression;
- ammunition consumption or inventory depletion;
- hostile/non-consensual combat;
- weapon lethality;
- injury/casualty generation;
- projectile/ballistics simulation;
- real-world firearm technique instructions;
- handgun/rifle/shotgun sub-skill taxonomy.

## Next review

**Firearms Progression Producer v1**.

Use a dedicated simulation-safe practice producer and explicit whitelisted learning evidence. Do not reinterpret `firearm_drill` application evidence as XP. Component progression may re-derive Weapon Mastery and the hidden legacy projection, but neither parent receives direct experience.
