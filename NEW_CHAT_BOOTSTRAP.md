# Observer Sandbox — New Chat Bootstrap

Status: **ACTIVE DEVELOPMENT**
Last synchronized: 2026-08-14

## Startup / authority

Read and reconcile in this order:
1. `AGENTS.md`
2. this file
3. `ROADMAP.md`
4. task-relevant canonical contracts/source files
5. current live production evidence before implementation decisions

Current Creator instruction and newer repository/CI/deploy/live-runtime evidence override older chat memory.

## Development workflow

Default flow:

`test -> focused tests + CI -> merge main -> automatic deploy when runtime-affecting -> read-only production check`

Keep only persistent `main` and reusable `test` branches unless an exceptional need is concrete. After merge/deploy, fast-forward `test` back to current `main` before the next slice.

Production-copy validation is optional. Use it when a stateful/migration risk needs production-shaped data; otherwise prefer focused regression + full CI. Never accelerate production or mutate live profile/world/progression merely to manufacture acceptance evidence.

Whenever a slice introduces a new architecture/control invariant, update its canonical contract plus `ROADMAP.md` and this bootstrap in the same development cycle.

## Current verified production baseline

Latest runtime-affecting deployment: **Deploy #174 `31787127694` SUCCESS**, PR #68 merge `3bceda924ed0fe18ce1d1360f6e0cc2c62c55f7e`.

Deploy #174 readback:
- service active / healthy;
- schema v4;
- world revision `thorne-estate-v3.3-physical-attribute-training`;
- default actor projection `char_darian`;
- autonomy enabled / normal, `paused=false`, `autonomy_retry=null`;
- speed **`1.0x`**;
- primary cognition Gemini `gemini-3.1-flash-lite`;
- normal Groq bootstrap preserved that explicit Creator-selected primary (`existing_binding_preserved`);
- fallback Groq `qwen/qwen3.6-27b`, configured/tested through Telegram;
- Telegram API connected; owner and allowed-user config present;
- cognition `decision_calls=356` at readback;
- Darian was sleeping in the Master Suite; Energy 82.127, Fatigue 11.045, Hunger 50.325, Thirst 21.3, Sleepiness 31.55, Cleanliness 99.466.

No model probe/provider failure/live-state mutation was induced for Deploy #174 acceptance.

## Universal Character Engine Contract

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.
Canonical contract: `docs/UNIVERSAL_CHARACTER_ENGINE_CONTRACT.md`.

Invariant:
- Darian is exemplar content, not reusable engine identity;
- character config registry owns character-specific canonical/runtime/autonomy-policy files;
- actor selection is explicit actor -> valid configured `default_actor_id` -> sole actor;
- multi-character ambiguity fails closed;
- another actor cannot silently inherit Darian cognition policy;
- reusable runtime/autonomy/query/AI/simulation APIs do not rely on literal `char_darian` defaults;
- missing actor location is invalid state, not implicit Master Suite;
- global resume wakes all enabled idle actors;
- synthetic non-Darian regression guards identity leakage;
- no schema v5.

Named Darian/Thorne content and `/darian` convenience presentation remain valid exemplar surfaces.

## AI / Telegram control state

P2.3 Telegram Creator AI Control v1, Runtime Cognition Fallback v1 and Telegram Observer Home Message Lifecycle v1 are deployed.

Key invariants:
- catalog fetch does not mutate cognition binding;
- selected model requires explicit real `Test Model` before save;
- test failure/cancel/navigation do not mutate config;
- credential values never display;
- CI/deploy never performs a model probe;
- one eligible provider-layer failure may try one configured fallback;
- fallback never rewrites primary;
- deterministic action/target/duration/runtime validation never triggers fallback;
- both provider calls failing returns to ordinary autonomy retry/backoff;
- `/start` Home has manual Close plus bounded 5-minute default auto-delete lifecycle.

Do not deliberately fail Gemini or spend inference simply to prove fallback monitoring.

## Training / physiology state

Deployed:
- systemic fatigue/recovery;
- targeted training sessions;
- readiness/effectiveness/effective training load;
- minimum Strength stimulus;
- training-session load/recovery guard;
- causal needs and sleep-pressure/circadian behavior;
- Training Method Semantics v1;
- Dynamic Resource Awareness / Choice Breadth;
- Object Familiarity / Inspect Utility Guard.

## Physical Attribute Progression Framework v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.
Canonical contract: `docs/PHYSICAL_ATTRIBUTE_PROGRESSION_FRAMEWORK.md`.

All seven core RAPS-PA attributes now have active progression paths:
- Strength;
- Stamina;
- Agility;
- Speed;
- Reflexes;
- Endurance;
- Flexibility.

PR #68:
- final tested head `5ebe50d0752790c1abea7ee6d653be8ebd5a1c2e`;
- CI #608 SUCCESS;
- Strength Live Cycle #16 SUCCESS;
- Strength Progression Activation #8 SUCCESS;
- Minimum Training Stimulus #9 SUCCESS;
- Stamina Progression Activation #9 SUCCESS;
- Training Environment #3 SUCCESS;
- merge `3bceda924ed0fe18ce1d1360f6e0cc2c62c55f7e`;
- post-merge CI #609 SUCCESS;
- Deploy #174 SUCCESS.

Key semantics:
- shared actor-generic policy-driven framework handles Speed/Reflexes/Endurance/Flexibility;
- Stamina remains cardiovascular/work-capacity reserve and does not silently duplicate Endurance;
- Flexibility has a real Mobility & Stretching Area and `mobility_stretching` method;
- first activation bootstraps without retroactive gain;
- existing Strength/Stamina/Agility implementations remain intact;
- no schema v5 and no extra model calls.

## Body Composition Progression — CURRENT ACTIVE PROGRAM

Canonical research contract: `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`.

Creator explicitly requires realistic human-body behavior with age, sex and genetic potential considered before formulas are frozen. Online evidence was therefore reconciled before implementation.

Evidence-led decisions:
- do not use a static `3500 kcal = 1 lb` rule as the body-composition engine;
- model coupled fat mass (FM) and fat-free mass (FFM) over bounded settlement intervals;
- use Hall/Forbes-style partitioning only as a first-order deterministic approximation, with explicit audit evidence;
- sex affects typical baseline composition/reference physiology but is **not** a crude universal male-vs-female hypertrophy multiplier;
- age is a physiological/context input, not a hard response cliff;
- genetic potential is character-specific canonical/config data with population FFMI/FMI used only as plausibility context, never as a universal hard ceiling;
- body-fat/weight progression requires real nutrition/energy-balance evidence and must not infer kcal from `needs.hunger` or `needs.energy`;
- protein/energy availability constrains lean-mass adaptation;
- action energy expenditure should be actor-scaled and based on authored intensity/MET policy rather than one global kcal/min constant.

Current profile already declares `body.weight_lb`, `body.body_fat_pct`, derived `body.lean_mass_lb`, `body.fat_mass_lb`, `body.bmi`, plus Darian's canonical lean-condition weight range and sustainable body-fat floor. No schema v5 is needed for the first body-composition engine.

### BC-0 — Simulated profile re-seed safety

Status: **IMPLEMENTED ON `test`, VALIDATION PENDING**.

Ordinary canonical re-seeding must initialize inactive profile fields without clobbering a field already activated by a simulation engine (`mode=simulated`). This is a universal reliability prerequisite for body composition and protects already-live attribute progression across deploy/re-init.

Implementation:
- `profile_seed.import_seed()` preserves existing simulated values/authority/source;
- non-simulated canonical/static fields can still receive intentional seed revision updates;
- regression coverage proves re-initialization preserves an engine-owned simulated Strength value while a canonical field remains seed-updatable.

### BC-1 — Minimum Nutrition & Energy Balance Evidence

**NEXT minimum-runnable slice after BC-0 is green/deployed.**

Required substrate:
- authored nutrition profile catalog for edible targets/meals;
- kcal/protein evidence associated with completed eating actions or immutable composition settlements;
- actor-specific resting expenditure estimate using body/demographic evidence;
- action/training intensity mapping informed by the 2024 Compendium of Physical Activities;
- bounded aggregation window with evidence coverage checks;
- no body-composition mutation from abstract hunger/energy scores.

This is part of the body-composition program, not a separate product detour.

### BC-2 — Body Composition Progression Exemplar

After BC-1 is proven:
- activate coupled `body.weight_lb` + `body.body_fat_pct` through one universal actor-generic engine;
- derive FM/FFM and BMI consistently;
- combine energy balance with bounded FM/FFM partitioning;
- model resistance-training lean adaptation separately, constrained by training evidence, protein/energy availability, current training state and personalized genetic headroom;
- write both coupled fields atomically with profile history + audit event;
- bootstrap at activation without retroactive gains;
- no Darian-specific branch.

### BC-3 — Body Measurement Progression Batch

Only after BC-2 is live/validated. Circumferences must not be derived from weight alone; measurement changes need body composition plus regional training/anatomical policy.

## Exact resume point

Finish **BC-0** now: run full CI, merge/deploy/readback if green, sync `test` to `main`, then immediately implement **BC-1 Minimum Nutrition & Energy Balance Evidence**.

Do not jump directly to weight/BF mutation until nutrition/energy evidence is causal enough to support it.

Do not add full Character Memory, multi-fallback/circuit-breaker architecture, forced equipment rotation, Telegram secret editing/model tuning, a second production character merely for testing, endocrine/micronutrient simulation, or schema v5 as side effects.
