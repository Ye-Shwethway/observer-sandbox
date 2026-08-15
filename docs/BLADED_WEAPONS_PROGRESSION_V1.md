# Bladed Weapons Progression Producer v1

Status: COMPLETE

## Canonical checkpoint

- Runtime PR: #154 — `add Bladed Weapons progression producer v1`
- Final tested head: `148884966ded63559806101cffbeb891efbe96dd`
- Runtime merge: `11ee97f093c7bc5a7439742f3f691f87b6b915de`
- PR CI: #908 / run `31890299802` — SUCCESS, 518 passed in 191.64s, fresh DB init/status healthy, schema v5
- Production deploy: #222 / run `31890490349` — SUCCESS
- Post-merge CI: #909 / run `31890490342` — SUCCESS

## Runtime contract

Bladed Weapons learning is explicit and separate from ordinary represented application.

Learning producer:
- method `bladed_weapons_handling_practice`;
- action `practice`;
- minimum duration 10 minutes;
- relevance `{ "bladed_weapons": 1.0 }`;
- `simulation_safe` evidence tag;
- dedicated target `obj_thorne_estate_training_bladed_weapons_practice_simulator` in the Training Hall.

The existing `blade_drill` represented application remains application evidence only. It does not grant Bladed Weapons XP merely because it succeeds.

## Hierarchy settlement

`Bladed Weapons` remains the learned component authority. When explicit Bladed progression changes its score, the existing hierarchy reconciler immediately refreshes:
- derived `Weapon Mastery` = mean of current Bladed Weapons and Firearms scores;
- hidden legacy `weapons` compatibility projection = current Weapon Mastery score.

Neither `Weapon Mastery` nor the legacy projection receives direct experience. Firearms is not modified by Bladed learning.

## Production evidence boundary

Deploy #222 safely loaded the producer and ran initialization against production. Production remained healthy and no Bladed practice or `blade_drill` was forced for proof.

Verified readback after deployment:
- service active/healthy; schema v5;
- autonomy enabled, normal mode, speed 10x, retry null, pending action present;
- Gemini `gemini-3.1-flash-lite` primary cognition preserved;
- Groq `qwen/qwen3.6-27b` fallback healthy;
- Telegram bot/API/owner/allowed-user configuration healthy;
- sim time `2025-05-06T17:18:00+00:00`;
- Darian naturally resting in Darian's Master Suite;
- Bladed Weapons 87/A, Firearms 87/A, Weapon Mastery 87/A, overall Skills A / 85.167.

The unchanged production scores are expected: activation/bootstrap is zero-gain until new eligible explicit practice evidence occurs. Score gain, exactly-once settlement, hierarchy re-derivation, application-not-learning separation, and reinitialize preservation are CI/fresh-fixture evidence.

## Boundaries

This slice does not add Firearms runtime/progression, hostile or non-consensual combat, lethality, injury, casualty generation, weapon consumption, real-world weapon instructions, deep weapon taxonomy, or a generic use/application-to-XP shortcut.

## Next review

Review **Firearms Simulation-Safe Runtime v1** next. Reuse the proven component-owned application/resource/target pattern rather than creating a second bespoke architecture. Progression for Firearms remains a later explicit learning slice after its safe represented application invariant is proven.
