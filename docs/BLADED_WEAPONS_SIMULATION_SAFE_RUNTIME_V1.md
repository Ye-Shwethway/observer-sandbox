# Bladed Weapons Simulation-Safe Runtime v1

Status: COMPLETE

## Purpose

Activate the first represented runtime application owned by the learned `bladed_weapons` component without turning the Weapon Mastery hierarchy into a combat, injury, or lethality system.

This slice proves one bounded invariant:

`learned component Skill + exact simulation-safe context + exact represented training resource + exact represented target -> deterministic application evidence`

Application evidence remains separate from learning evidence.

## Authority transfer

`employ_familiar_melee_weapon` is no longer executable through the hidden legacy `weapons` compatibility projection.

Executable authority now belongs to:

`bladed_weapons.employ_familiar_melee_weapon`

`weapon_mastery` remains a derived non-executable parent. `firearms` remains a learned component with no active represented runtime in this slice.

The active Bladed application narrows the historical melee semantics to an explicitly simulation-safe contract requiring:
- `weapon_employment_context`;
- `represented_melee_weapon`;
- `simulation_safe_training_context`;
- exact resource capability `usable_bladed_training_weapon`.

The broader historical `usable_melee_weapon` capability is not used by this first executable runtime.

## Represented task

Task:
`bladed_weapons_safe_handling_sim_v1`

Action:
`blade_drill`

Exact target definition:
`represented_task:bladed_weapons_safe_handling_simulator_v1`

Seeded target:
`obj_thorne_estate_training_bladed_weapons_safe_handling_simulator`

Location:
`loc_thorne_estate_training_hall`

Required target/resource capabilities:
- `blade_drill`;
- `usable_bladed_training_weapon`.

Task mode: `simulation_safe`
Risk class: `low`

The simulator is an abstract represented training resource. This runtime does not encode real-world weapon technique, offensive instructions, injury mechanics, weapon consumption, or hostile-target semantics.

## Deterministic outcome

The first Bladed exemplar deliberately declares no separate cognitive/Attribute modifier contract.

Therefore:
- authoritative `bladed_weapons.score` is the performance authority;
- IQ, reflexes, focus, agility, and other fields are not silently added as bonuses;
- Darian's fresh-fixture Bladed score of 87 resolves to deterministic 0.87 quality/recovery indices under supported conditions;
- the fixture outcome class is `strong`.

Outcome dimensions:
- `quality_precision`;
- `partial_failure_recovery`.

World mutation policy:
`simulation_evidence_only`

## Evidence boundary

Successful completion emits:
- `action_completed`;
- `skill_application_evidence`.

The application evidence records `bladed_weapons` as Skill authority and `employ_familiar_melee_weapon` as the application.

It explicitly records:
`learning_evidence: false`

Running the generic Skill progression settlement after this application does not change:
- Bladed Weapons score/experience;
- Firearms score/experience;
- Weapon Mastery derived score;
- legacy Weapons compatibility projection.

A future progression slice must add an explicit safe learning producer rather than treating generic application/use as XP.

## Fail-closed boundaries

The runtime rejects before completion when:
- target definition is not the exact authorized represented task;
- the target lacks required task capability `usable_bladed_training_weapon`;
- actor lacks authoritative `bladed_weapons` Skill state;
- represented application requirements are otherwise unsupported.

Existing action IDs remain exactly-once evidence identities.

## Validation evidence

Runtime PR:
- PR #152 — `add Bladed Weapons simulation-safe runtime v1`
- final tested head: `44f70f8f9768665851858a16bc198c962d9b512a`
- merge: `ce77b0a9a78684283c69daa3357df1dcd4d9aeb6`

Final PR CI:
- CI #902 / run `31889534085`: SUCCESS
- 513 tests passed in 42.24s
- fresh DB `sandboxctl init` succeeded
- fresh DB `sandboxctl status` healthy
- schema v5
- relevant Skill Definition, Application Requirements, Actor Capability, Represented Task, Cognition, Technology, and Strength acceptance lanes green.

Production deployment:
- Deploy #221 / run `31889659349`: SUCCESS
- exact deployed head: `ce77b0a9a78684283c69daa3357df1dcd4d9aeb6`
- production init succeeded;
- service active/healthy;
- schema v5;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram API/owner/allowed-user configuration healthy.

Verified deployment readback naturally showed:
- autonomy enabled, normal mode;
- speed `10.0`;
- retry null and pending action present;
- sim time `2025-05-06T14:18:00+00:00`;
- Darian naturally reading in the Living Room;
- Bladed Weapons 87/A;
- Firearms 87/A;
- Weapon Mastery 87/A;
- overall Skills A / 85.167.

No production `blade_drill` or other weapon proof action was forced. Production deployment proves safe loading and continuity only; exact application/evidence/no-XP semantics are CI/fixture evidence.

## Non-goals preserved

This slice does not add:
- hostile or non-consensual combat;
- lethality;
- injury or casualty generation;
- real-world weapon instructions;
- weapon inventory consumption;
- automatic Bladed Weapons XP;
- Firearms runtime;
- knife/sword/deeper weapon taxonomy;
- H2H hierarchy changes;
- relationship or casualty-system expansion.

## Next development direction

Review **Bladed Weapons Progression Producer v1** next.

The preferred shape is one explicit simulation-safe practice producer that creates legitimate Bladed learning evidence. It must preserve the rule that ordinary represented application/use does not automatically grant XP.

Once the Bladed application + learning invariant is complete, apply the proven structure to **Firearms** by pattern rather than inventing a parallel architecture.
