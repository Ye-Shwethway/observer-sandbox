# Skills Closure v1

Status: **CLOSED — MINIMUM UNLOCK COMPLETE**

## Purpose

Skills v1 closes the Character Profile Skills section under the Minimum Profile Unlock Policy. The goal is vertical completeness, not exhaustive Skill depth.

A learned Skill is considered minimum-unlocked when it has authoritative score/grade semantics, profile/cognition visibility, at least one meaningful represented application where safely runnable, and a legitimate learning path with explicit separation between application evidence and learning evidence.

## Frozen v1 learned Skill surface

- Hand-to-Hand Combat
- Bladed Weapons
- Firearms
- Survival
- Tactical Planning
- Technology
- Field Medicine

`Weapon Mastery` remains a derived, non-executable parent over Bladed Weapons and Firearms. The hidden legacy `weapons` row remains a compatibility projection. Neither receives direct progression XP.

Skill-like compatibility/Attribute fields such as combat skill, weapons proficiency, survival skill, powerlifting capacity, focus/precision, practical skills, technological aptitude, and medical knowledge are not independent Skills in this minimum pass.

## Field Medicine closure

Skills Closure Batch v1 adds the final missing learning path:

- method: `field_medicine_scenario_practice`
- action: `practice`
- minimum duration: 10 minutes
- relevance: `{ "field_medicine": 1.0 }`
- target: `obj_thorne_estate_training_field_medicine_practice_simulator`
- location: Training Hall
- tags include `simulation_safe`

The practice target is an abstract scenario simulator, not a live casualty. It does not create casualty state, diagnose a patient, perform treatment, or imply a broader Injury Engine.

Real Field Medicine assessment and bounded stabilization remain casualty-context-bound represented applications. Their application evidence is not automatically learning evidence.

## Validation

Runtime PR: **#161 — `close Skills v1 minimum unlock`**

Final tested head:
`f502e7e0e0f438b2dfac9ffab01c547ef1b255b9`

Merge:
`7cbc92a38ee8b3f5d8220c6e33ff0c4d00f157b4`

Final validation:
- CI #923 / run `31893520852`: SUCCESS
- fresh DB init/status: SUCCESS
- Skill Progression Foundation: SUCCESS
- Skill Evidence Semantics: SUCCESS
- Skill Definition Format/Refactor: SUCCESS
- Tactical Planning progression regression: SUCCESS
- Strength Live Cycle Validation: SUCCESS
- Public Readiness Security Audit: SUCCESS

The first full CI attempt exposed four stale contract assertions after 531 passing tests. They were limited to prior global progression-revision/set expectations and were updated narrowly. No runtime architecture change was required.

## Production

Deploy #226 / run `31893586685`: **SUCCESS**

Verified readback after deployment:
- service healthy; schema v5;
- autonomy enabled, normal mode, retry null;
- speed 10x at readback;
- sim time `2025-05-07T06:24:00+00:00`;
- Darian was naturally training in the Top-Class Home Gym;
- Field Medicine remained 75/A;
- Bladed Weapons 87/A;
- Firearms 87/A;
- Weapon Mastery 87/A;
- overall Skills 85.167/A;
- Gemini primary, Groq fallback, and Telegram observer configuration healthy.

Initialization only activated the Field Medicine learning producer with zero gain. No production practice or casualty was fabricated for proof.

The live morning training state also demonstrates that the earlier circadian stabilization has progressed beyond the previously pending early-evening sleep lock.

## Definition metadata note

The active Field Medicine learning authority for this slice is the explicit Skill Progression + Skill Practice registries. The older universal Skill Definition `learning_evidence` description was not comprehensively refactored in this closure batch. It remains definition-era metadata and must not be interpreted as implicit application-to-XP authority.

This is acceptable minimum-pass debt and can be normalized later if the Skill Definition framework is revisited. It is not a blocker for Skills v1 closure because runtime progression is explicit, whitelisted, tested, and application evidence remains non-learning.

## Deferred depth

Skills v1 closure does not add:
- deeper H2H, blade, firearm, medicine, survival, tactical, or technology trees;
- Injury Engine, diagnosis taxonomy, treatment graph, death/incapacity, or random casualty generation;
- hostile/non-consensual combat or weapon lethality;
- retention/decay/reacquisition depth;
- automatic application => XP;
- a second production actor solely for proof.

Add deeper Skill structure only when a future represented task requires distinct authority or progression.

## Next

Leave Skills closed and proceed to the **Remaining Profile Minimum Unlock Sweep**. Existing mature sections should receive closure review rather than rewrites; canonical/contextual sections should receive only the smallest real runtime influence required by the minimum-unlock policy.
