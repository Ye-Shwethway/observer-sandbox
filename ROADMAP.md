# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-14

## Operating principles

- Python/SQLite runtime and world state are authoritative.
- AI proposes structured cognition; deterministic engines own mutations.
- Telegram is a Creator-facing observer/control adapter, not a simulation engine.
- Preserve the composable runtime contract:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Darian is the first richly specified exemplar, not the identity embedded in reusable universe engines.
- Character-specific profile/policy/world content is data; reusable simulation/cognition/progression/query/control logic must be actor/entity-id driven.
- Schema v4 remains the current foundation; do not introduce schema v5 without a concrete missing invariant.
- Prefer minimum-runnable, reversible slices.
- Use exemplar-first only for genuinely new invariants; batch structurally equivalent follow-ons.
- For physiology/body systems, external human evidence should inform the deterministic policy before formulas are frozen; simulation approximations must be documented as policy rather than presented as biological laws.
- Default development flow:
  `test -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`.
- Keep only persistent `main` and reusable `test` branches unless a concrete exceptional need requires otherwise.
- Production-copy validation is optional and reserved for genuinely state-sensitive/migration-heavy work.
- New architecture/control surfaces must update their canonical contract plus this roadmap/bootstrap checkpoint in the same development cycle.

## Current verified production baseline

Latest runtime-affecting deployment: **Deploy #174 `31787127694` SUCCESS** from PR #68 merge `3bceda924ed0fe18ce1d1360f6e0cc2c62c55f7e`.

Deploy #174 readback verified:
- service active / healthy;
- schema v4;
- world revision `thorne-estate-v3.3-physical-attribute-training`;
- configured/default actor projection `char_darian`;
- autonomy enabled / normal, `paused=false`, `autonomy_retry=null`;
- speed **`1.0x`**;
- cognition primary Gemini `gemini-3.1-flash-lite`, preserved through normal deploy bootstrap;
- configured fallback Groq `qwen/qwen3.6-27b`, tested at `2026-08-14T07:27:42.290743+00:00`;
- Telegram API connected with owner/allowed-user configuration present;
- cognition `decision_calls=356` at the readback boundary;
- Darian was sleeping in the Master Suite with Energy 82.127, Fatigue 11.045, Hunger 50.325, Thirst 21.3, Sleepiness 31.55 and Cleanliness 99.466.

No production acceleration, direct live profile/progression mutation, validation-induced model probe or intentionally induced provider failure was used for Deploy #174 acceptance.

## Completed foundation and observer/control layers

- Foundation schema v4 — COMPLETE.
- P0 Foundation & Remote Control — COMPLETE / LIVE VERIFIED.
- P0.5 dynamic AI provider layer — COMPLETE; Gemini, Groq and generic OpenAI-compatible runtime support are deployed, with OpenAI/OpenRouter/NanoGPT provider surfaces retained.
- P1 Living Darian Minimum — CONTINUOUS AUTONOMY LIVE.
- P2 Telegram Observer MVP / browse / profile-control surfaces — COMPLETE / LIVE VERIFIED.
- Runtime speed control, action ETA, autonomy timing/observability, research/monitor semantics — DEPLOYED.
- Telegram proactive next-action cognition reason — DEPLOYED via PR #62 / Deploy #170.
- P2.3 Telegram Creator AI Control v1 — COMPLETE / CI VERIFIED / DEPLOYED / CREATOR-EXERCISED.
- Runtime Cognition Fallback v1 — COMPLETE / CI VERIFIED / DEPLOYED / CREATOR-CONFIGURED.
- Telegram Observer Home Message Lifecycle v1 — COMPLETE / CI VERIFIED / DEPLOYED.

### AI control/fallback invariant

Canonical contracts: `docs/AI_RUNTIME_FALLBACK.md`, `docs/TELEGRAM_HOME_LIFECYCLE.md`, `docs/TELEGRAM_OBSERVER_ARCHITECTURE.md`.

- Provider catalogs can be fetched without changing bindings.
- A selected provider/model must pass one explicit real `Test Model` structured inference before save.
- Browse/refresh/select/test-failure/cancel do not mutate active configuration.
- Credential values are never displayed.
- Normal deploy/bootstrap preserves every existing explicit Creator-selected primary binding.
- One provider/model invocation failure may use the configured single fallback once.
- Fallback use never permanently rewrites primary cognition.
- Deterministic action/target/duration/runtime validation failure never triggers provider fallback.
- If primary and fallback both fail, existing autonomy retry/backoff remains authoritative.
- CI/deploy acceptance does not consume a model probe.

Explicitly deferred: multi-fallback chains, circuit breakers, provider-health scoring, automatic permanent rebinding, Telegram secret editing and model-parameter tuning.

## Universal Character Engine Contract

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

Canonical contract: `docs/UNIVERSAL_CHARACTER_ENGINE_CONTRACT.md`.

Current invariant:
- `config/characters/registry.json` resolves character-specific canonical/runtime-policy files as content, not engine identity;
- reusable actor selection is explicit actor -> configured valid `default_actor_id` -> sole existing character;
- ambiguous multi-character implicit selection fails closed;
- cognition loads the selected character's registered policy; another actor cannot silently inherit Darian's policy;
- reusable runtime/control/query/AI/simulation paths do not require a literal `char_darian` default;
- missing character location is invalid runtime state rather than an implicit Thorne Estate Master Suite;
- movement uses generic dynamic-location semantics;
- universe resume wakes every enabled idle actor at a decision boundary;
- synthetic non-Darian regression coverage catches identity leakage;
- Darian profile/config, Thorne Estate content and clearly named presentation aliases such as `/darian` remain valid exemplar content;
- no schema v5.

## Training and physiology foundation

- P3.1 Systemic Training Fatigue / Recovery — COMPLETE / LIVE VERIFIED.
- P3.2 Targeted Training Session — COMPLETE.
- P3.3 Training Readiness Modifier — COMPLETE / DEPLOYED.
- P3.4 Training Effectiveness Outcome — COMPLETE / DEPLOYED.
- P3.5 Effective Training Load — COMPLETE / DEPLOYED.
- Minimum Training Stimulus v1 — COMPLETE / DEPLOYED.
- Training Session Load & Recovery Guard v1 — COMPLETE / CI VERIFIED / DEPLOYED.
- Causal hunger, thirst, energy, sleepiness, cleanliness and fatigue resolution — DEPLOYED.
- Sleep Pressure & Circadian Need v1 — COMPLETE / DEPLOYED.

Training Load Guard v1 budgets remain:
- current session: 90 effective minutes;
- session break: >120 simulated minutes without training;
- rolling 6 hours: 120 effective minutes;
- rolling 24 hours: 180 effective minutes.

Short fatigue recovery does not erase recent training dose. The model sees the derived remaining budget; deterministic validation remains final authority.

## Training environment and method semantics

Current production world: `thorne-estate-v3.3-physical-attribute-training`.

Training Hall and Top-Class Home Gym provide the bounded authored training-resource surface. The Home Gym now includes a Mobility & Stretching Area for causal Flexibility evidence. Exterior estate grounds/private lake/outdoor tactical course/Tahoe traversal remain deferred.

`config/training_methods.v1.json` is the canonical Training Method Semantics v1 catalog. Equipment/method metadata describes causal workload/planning evidence; it does not own progression formulas or directly mutate attributes.

Object Familiarity / Inspect Utility Guard v1 and Dynamic Resource Awareness & Choice Breadth v1 are deployed. Familiar functional resources do not remain generic low-value inspect fallbacks; cognition can choose normal downtime instead of manufactured activity.

## Physical progression state

### Strength

Status: **ACTIVE / DEPLOYED / LIVE-CYCLE VALIDATED**.

Free Weights remains the deliberate Strength stimulus source. Strength retains its proven level difficulty, saturation, recovery realization, detraining, idempotent settlement and completed-action activation semantics.

### Stamina

Status: **ACTIVE / DEPLOYED**.

Pure-conditioning evidence sources remain High-Speed Treadmill / `steady_state_cardio`, Rowing Ergometer / `rowing_conditioning`, and Altitude Training Chamber / `altitude_conditioning`. Mixed movement/combat methods are not silently credited to Stamina.

### Agility

Status: **ACTIVE / DEPLOYED**.

Agility uses `speed_agility_drills` from the Speed & Agility Station with its proven recovery/saturation/detraining semantics and automatic completed-action activation.

### Physical Attribute Progression Framework v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

Canonical contract: `docs/PHYSICAL_ATTRIBUTE_PROGRESSION_FRAMEWORK.md`.

Delivery:
- PR #68 final tested head `5ebe50d0752790c1abea7ee6d653be8ebd5a1c2e`;
- primary CI #608 SUCCESS;
- Strength Live Cycle #16 SUCCESS;
- Strength Progression Activation #8 SUCCESS;
- Minimum Training Stimulus #9 SUCCESS;
- Stamina Progression Activation #9 SUCCESS;
- Training Environment #3 SUCCESS;
- merge `3bceda924ed0fe18ce1d1360f6e0cc2c62c55f7e`;
- post-merge CI #609 SUCCESS;
- Deploy #174 SUCCESS.

All seven core RAPS-PA fields now have active progression paths:
- Strength;
- Stamina;
- Agility;
- Speed;
- Reflexes;
- Endurance;
- Flexibility.

The shared lifecycle remains:

`evidence scan -> consumed-event cursor -> recovery gate -> level/saturation gain -> detraining integration -> profile/history write -> settlement event`

Speed/Reflexes/Endurance/Flexibility use one actor-generic policy-driven framework. Existing Strength/Stamina/Agility implementations remain intact to avoid unnecessary migration risk.

No forced live training is used for acceptance; natural completed actions bootstrap/newly mature progression evidence.

## Grading state

- Strength grading exemplar — COMPLETE / DEPLOYED.
- Attribute Grading Batch 1 — COMPLETE / DEPLOYED for compatible 0..100 attribute fields.
- IQ remains a separate scale.
- Skills grading/progression remains a separate family.
- Body composition/measurements remain a separate architecture family.

## Body Composition Progression Program — CURRENT ACTIVE PROGRAM

Canonical research contract: `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`.

Creator requirement: body-composition progression must respect realistic human physiology, including age/sex context, individual genetic potential, nutrition/energy balance and plausible human ratios. Formula design therefore begins from external physiological evidence rather than convenience constants.

### Evidence-led architecture decisions

Research reconciled from NIH/NIDDK dynamic body-weight modeling, Hall/Forbes FM-FFM partition work, resistance-training hypertrophy studies/meta-analyses, protein/energy-deficit evidence, body-composition reference data and the 2024 Compendium of Physical Activities.

Current decisions:
- do not use `3500 kcal = 1 lb` as a universal runtime law;
- represent at minimum weight, fat mass (FM), fat-free mass (FFM) and body-fat percentage as a coupled system;
- use small bounded settlement intervals rather than large instantaneous changes;
- Hall/Forbes-style FM/FFM partitioning may be used as a first-order deterministic approximation, with its assumptions and settlement inputs audited;
- sex-specific population body-composition differences are real, but same-program relative hypertrophy is sufficiently similar that a crude universal male-vs-female hypertrophy multiplier is rejected;
- age affects body composition/metabolism and can attenuate some older-adult hypertrophy responses, but large individual variability means age is a context/modifier rather than a response cliff;
- genetic potential is character-specific profile/config data; population FFMI/FMI ranges are plausibility references, not universal hard caps;
- `genetics.weight_lean_min_lb` / `genetics.weight_lean_max_lb` are interpreted as a canonical **lean-condition body-weight envelope**, not raw FFM; a body engine may derive potential FFM from that envelope plus sustainable body-fat condition without rewriting the canonical semantic;
- body composition must not infer calories/protein from abstract `needs.hunger` or `needs.energy`;
- protein and energy availability constrain resistance-training lean-mass adaptation;
- action energy expenditure should be actor-scaled using resting physiology plus authored action/method intensity rather than a global kcal/min constant;
- no schema v5 is required for the first body-composition engine.

Current profile schema already declares:
- `body.weight_lb`;
- `body.body_fat_pct`;
- derived `body.lean_mass_lb`;
- derived `body.fat_mass_lb`;
- derived `body.bmi`;
- canonical sex/DOB/height;
- genetic lean-condition weight range and sustainable body-fat floor.

### BC-0 — Simulated Profile Re-seed Safety

Status: **IMPLEMENTED ON `test` / VALIDATION PENDING**.

Problem discovered during body-composition audit:
ordinary `profile_seed.import_seed()` previously upserted seed values on every initialize/deploy. Once a progression engine has changed a profile field to `mode=simulated`, ordinary re-seeding must not reset it to the canonical/static starting seed.

Invariant:
- canonical seed initializes inactive fields;
- an existing `mode=simulated` profile value remains authoritative across ordinary re-init/deploy;
- non-simulated canonical/static fields can still receive intentional seed-revision updates;
- explicit migrations/control operations remain separate from ordinary seed import.

Current implementation on `test`:
- `profile_seed.import_seed()` preserves existing simulated value/mode/authority/source;
- regression proves an engine-owned simulated Strength value survives `initialize()`;
- regression separately proves a non-simulated canonical field remains seed-updatable.

This is a universal reliability fix for already-live progression and a hard prerequisite before weight/body-fat become simulated.

### BC-1 — Minimum Nutrition & Energy Balance Evidence

Status: **NEXT minimum-runnable slice after BC-0 is green/deployed**.

Current runtime gap:
`eat` presently changes abstract hunger/energy needs but does not provide kcal/protein/macronutrient evidence. Those need scores cannot be treated as calorie intake.

Minimum substrate:
- authored nutrition profile catalog for edible targets/meals;
- kcal/protein evidence associated with completed eating actions or immutable settlement evidence;
- actor-specific resting expenditure estimate from current body/demographic evidence;
- action/method intensity mapping informed by the 2024 Compendium of Physical Activities;
- bounded evidence aggregation window and coverage/idempotence rules;
- no body-composition mutation if evidence coverage is not causally adequate;
- no body-composition mutation directly from hunger/energy need scores.

This is part of the body-composition program, not an unrelated nutrition-system detour.

### BC-2 — Body Composition Progression Exemplar

After BC-1 is proven, activate coupled `body.weight_lb` + `body.body_fat_pct` through one actor-generic engine:
- derive starting FM/FFM consistently;
- aggregate nutrition, expenditure and resistance-training evidence over bounded intervals;
- use bounded FM/FFM energy partitioning rather than one fixed tissue ratio;
- model resistance-training lean adaptation separately, constrained by training evidence, protein/energy availability, current training state and personalized genetic headroom;
- no crude sex hypertrophy multiplier;
- age/sex enter only where supported by evidence/policy;
- first activation bootstraps at current sim boundary without retroactive gain;
- write the coupled fields atomically with profile history and an audit event;
- hard-clamp/reject implausible single-window changes;
- no Darian-specific branch and no extra model calls.

### BC-3 — Body Measurement Progression Batch

Only after BC-2 is live/validated.

Circumference changes (waist/chest/arms/thighs/etc.) must not be derived from body weight alone. The measurement family will combine body composition, regional training evidence, anatomy/sex/age context where relevant and character-specific structural/genetic envelopes.

## Planned profile-unlock sequence after body composition

1. BC-0 re-seed safety;
2. BC-1 nutrition/energy evidence;
3. BC-2 body composition exemplar;
4. BC-3 compatible body-measurement batch;
5. skill progression exemplar;
6. compatible skill batch;
7. intellectual attribute exemplar/batch;
8. mental/emotion dynamics.

## Deferred boundaries

Not authorized as side effects of the current work:
- full Character Memory Engine;
- multi-fallback chains/circuit breakers/provider-health scoring;
- Telegram API-key editing/model tuning;
- second production character solely for universalization testing;
- forced equipment rotation;
- generalized inventory/resource depletion;
- detailed endocrine simulation;
- menstrual-cycle/hormone-state engine;
- micronutrient engine;
- organ-by-organ metabolic model;
- exact fluid/glycogen fluctuation model;
- richer relationship engine;
- estate exterior/Tahoe traversal;
- schema v5.

## Exact resume point

Finish **BC-0 Simulated Profile Re-seed Safety** on `test`: full CI -> merge -> automatic deploy/readback -> synchronize `test` to `main`.

Then immediately implement **BC-1 Minimum Nutrition & Energy Balance Evidence** as the next minimum-runnable body-composition prerequisite. Do not jump directly to weight/body-fat mutation until the nutrition/expenditure evidence is causally adequate.
