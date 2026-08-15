# Survival Skill Progression Producer v1

Status: COMPLETE

## Purpose

Activate legitimate solo-usable learning for the existing `survival` parent Skill without treating generic activity or represented application evidence as XP.

## Runtime contract

Survival progression reuses the existing config-driven `skill_practice` evidence family and generic Skill progression settlement. No new progression engine was added.

Explicit eligible practice methods:
- `field_navigation_practice`
- `field_sustainment_practice`

Purpose-built represented practice targets in the Thorne Estate Training Hall:
- `obj_thorne_estate_training_field_navigation_practice_simulator`
- `obj_thorne_estate_training_field_sustainment_practice_station`

Both methods require the generic `practice` action and at least 10 represented minutes. Their learning relevance is exactly `survival: 1.0`.

## Evidence boundary

Only explicit configured practice evidence is eligible for Survival progression in v1.

The following are not automatically Survival learning evidence:
- ordinary obstacle-course use;
- generic exercise/training prose;
- represented Survival navigation application evidence;
- represented Survival sustainment application evidence;
- inspect/research/monitor actions;
- target names or LLM prose.

Application evidence and learning evidence remain separate.

## Settlement behavior

Survival now uses the existing `skill-progression-structured-evidence` settlement model:
- score cap: 100;
- base score points per learning unit: 0.12;
- recent evidence window: 24 simulated hours;
- saturation half-units: 2.0;
- eligible methods: navigation and sustainment practice only.

Settlement is idempotent. Already-consumed evidence cannot grant progression twice. Re-initialization preserves accumulated score/experience.

## Validation

Runtime PR: #148
Final tested head: `159afdb3ccda6fd1745148f160954c8c1c7a71d9`
Merge: `8e094c542d1664f09deb6492ff7dbcb357f95111`
CI: #888 / run `31885722183` SUCCESS
- 500 tests passed in 34.75s;
- fresh DB init/status healthy;
- schema v5;
- Skill Progression Foundation, Skill Evidence Semantics, Skill Definition, Tactical Planning progression, and Strength validation gates green.

Deployment: #219 / run `31885774198` SUCCESS.

Production readback after deployment:
- service active/healthy;
- schema v5;
- autonomy remained enabled in normal mode at 1x;
- Gemini `gemini-3.1-flash-lite` primary cognition binding preserved;
- Groq `qwen/qwen3.6-27b` fallback preserved;
- Telegram connectivity/configuration healthy;
- Darian's live Survival score remained `85 / A` because no production practice was forced for proof.

Exact learning/progression semantics are proven by CI fixtures. Deployment proves safe production loading and continuity, not that Darian performed Survival practice live.

## Profile-first direction

This slice supports the current Character Profile completion strategy: make profile sections causally meaningful before expanding relationship/multi-character systems.

Casualty handoff/lifecycle-end work remains valid but deferred until multi-character development resumes.

Next review direction: **Weapons Simulation-Safe Runtime v1**. Keep weapon use bounded to safe training/simulation; do not introduce lethality, hostile use, casualty generation, or automatic Weapons XP as side effects.
