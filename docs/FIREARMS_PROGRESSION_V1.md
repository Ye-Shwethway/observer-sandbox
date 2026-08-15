# Firearms Progression Producer v1

Status: COMPLETE

## Purpose

Add legitimate learned progression for the `firearms` Weapon Mastery component without converting ordinary Firearms application into automatic XP and without granting direct progression to the derived `weapon_mastery` parent.

## Runtime contract

Learning authority:
- Skill: `firearms`
- method: `firearms_handling_practice`
- action: `practice`
- minimum duration: 10 sim minutes
- relevance: `{ "firearms": 1.0 }`
- dedicated target: `obj_thorne_estate_training_firearms_practice_simulator`
- location: Thorne Estate Training Hall
- evidence family: explicit whitelisted `skill_practice`

The practice target is intentionally distinct from the represented `firearm_drill` application simulator.

## Separation of application and learning

`firearm_drill` remains a simulation-safe represented application of `firearms.employ_familiar_ranged_weapon`. Successful application emits application evidence with `learning_evidence=false` and does not by itself progress Firearms.

Only eligible explicit practice evidence is progression authority for this producer.

## Hierarchy behavior

When legitimate Firearms learning changes the component score:
- `firearms` score/experience may advance;
- sibling `bladed_weapons` is not mutated;
- derived `weapon_mastery` score is recomputed from the current components;
- hidden legacy `weapons` compatibility projection follows the derived parent score;
- `weapon_mastery` and legacy `weapons` receive no direct experience/XP.

Initialization/redeployment is idempotent and does not overwrite existing component learning.

## Safety boundaries

This slice does not add:
- ammunition accounting or consumption;
- hostile or non-consensual target use;
- injury, casualty, incapacity, or lethality;
- real-world firearm technique/instruction;
- handgun/rifle or deeper weapon taxonomy;
- generic application=>XP behavior.

## Verification

Runtime PR: #159

Final tested head: `1553621a93e52cb52e948a856dec99a49bd4fc23`

Merge: `d759ef7903f889517e76a48b803fba83bba09ba0`

Final PR validation:
- CI #918 / run `31892374935`: SUCCESS;
- Skill Progression Foundation #40: SUCCESS;
- Skill Evidence Semantics #33: SUCCESS;
- Skill Definition Format #15: SUCCESS;
- Skill Definition Refactor Batch #16: SUCCESS;
- Skill Progression Tactical Planning #15: SUCCESS;
- Strength Live Cycle Validation #71: SUCCESS.

The immediately prior CI #917 reported 531 passing tests and one stale global progression-revision assertion. Only that assertion was updated; no runtime logic was relaxed.

Deployment:
- Deploy #225 / run `31892433699`: SUCCESS;
- deployed merge `d759ef7903f889517e76a48b803fba83bba09ba0`;
- production service/init/status healthy, schema v5;
- Gemini primary, Groq fallback, and Telegram configuration healthy;
- no Firearms practice or application was forced for production proof;
- production Bladed Weapons, Firearms, and Weapon Mastery remained 87/A as expected from zero-gain activation.

## Continuation

Firearms now has both simulation-safe application and explicit legitimate progression. The next canonical task is the **Skills Section Completion Review** before selecting another Character Profile section.