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

Latest deployed checkpoint before BC-1: **Deploy #175 `31788257885` SUCCESS**, PR #69 merge `e407533eff098f5803cc17469e8b9da8c24c21b8`.

Deploy #175 readback:
- service active / healthy;
- schema v4;
- world revision `thorne-estate-v3.3-physical-attribute-training`;
- default actor projection `char_darian`;
- autonomy enabled / normal, `paused=false`, `autonomy_retry=null`;
- speed `1.0x`;
- primary cognition Gemini `gemini-3.1-flash-lite` preserved by ordinary bootstrap;
- fallback Groq `qwen/qwen3.6-27b` preserved;
- Telegram API connected with owner/allowed-user config present;
- cognition `decision_calls=356` at readback;
- Darian remained sleeping in the Master Suite with Energy 82.127, Fatigue 11.045, Hunger 50.325, Thirst 21.3, Sleepiness 31.55 and Cleanliness 99.466.

No model probe/provider failure/live-state mutation was induced for Deploy #175 acceptance.

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

PR #68 final head `5ebe50d0752790c1abea7ee6d653be8ebd5a1c2e`; merge `3bceda924ed0fe18ce1d1360f6e0cc2c62c55f7e`; CI #608/post-merge #609 and all targeted acceptances succeeded; Deploy #174 succeeded.

## Body Composition Progression — CURRENT ACTIVE PROGRAM

Canonical research contract: `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`.
Canonical BC-1 evidence contract: `docs/NUTRITION_ENERGY_EVIDENCE.md`.

Creator requires realistic human-body behavior with age, sex and genetic potential considered before formulas are frozen. External physiology evidence was reconciled first.

Evidence-led decisions:
- do not use a static `3500 kcal = 1 lb` rule as the body-composition engine;
- model coupled fat mass (FM) and fat-free mass (FFM) over bounded settlement intervals;
- Hall/Forbes-style partitioning is only a first-order deterministic approximation with audit evidence;
- sex affects baseline/reference physiology but is not a crude universal male-vs-female hypertrophy multiplier;
- age is a physiological/context input, not a hard response cliff;
- genetic potential is character-specific canonical/config data; population FFMI/FMI is plausibility context only;
- body-fat/weight progression requires persisted nutrition/energy-balance evidence and cannot infer kcal from `needs.hunger` or `needs.energy`;
- protein/energy availability constrains later lean-mass adaptation;
- action expenditure is actor-scaled and uses authored Compendium-informed intensity policy rather than a single kcal/min constant.

Current profile already declares `body.weight_lb`, `body.body_fat_pct`, derived `body.lean_mass_lb`, `body.fat_mass_lb`, `body.bmi`, plus Darian's canonical lean-condition weight range and sustainable body-fat floor. No schema v5 is required for the first body-composition engine.

### BC-0 — Simulated Profile Re-seed Safety

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

PR #69:
- tested head `2a23ff48207867a6684832b8fefdd260053eac78`;
- CI #610 SUCCESS;
- merge `e407533eff098f5803cc17469e8b9da8c24c21b8`;
- post-merge CI #611 SUCCESS;
- Deploy #175 SUCCESS.

Invariant:
- canonical seed initializes inactive fields;
- an existing `mode=simulated` profile value remains authoritative across ordinary re-init/deploy;
- non-simulated canonical/static fields can still receive intentional seed-revision updates;
- explicit migrations/control operations remain separate from ordinary seed import.

### BC-1 — Minimum Nutrition & Energy Balance Evidence

Status: **IMPLEMENTED / CI VERIFIED / PRODUCTION-COPY VALIDATED ON PR #70; MERGE/DEPLOY PENDING**.

Current PR #70 head: `06cb2dddb34367cc1218cccd9341125a73693b7a`.

Validation:
- full CI #613 SUCCESS;
- Nutrition & Energy Evidence v1 Acceptance #1 / run `31788917813` SUCCESS on a disposable copy of production;
- copied-production Darian resting reference was about `2073.388 kcal/day` using Mifflin-St Jeor with his own age/sex/height/weight;
- a disposable 25-minute prepared-meal action persisted `800 kcal`, `50 g protein`, `90 g carbohydrate`, `27 g fat` intake evidence;
- that action's actor-scaled expenditure estimate was about `53.994 kcal` at activity multiplier `1.5`;
- `body.weight_lb` and `body.body_fat_pct` remained unchanged;
- model calls 0, Telegram calls 0, live production DB unchanged.

BC-1 implementation:
- `config/nutrition_profiles.v1.json` supplies authored food-content policy for current edible resources;
- `config/energy_expenditure.v1.json` supplies Mifflin-St Jeor resting reference plus Compendium-informed action/training intensity anchors;
- completed action events snapshot immutable nutrition/expenditure evidence;
- `energy_balance_window()` aggregates persisted evidence over bounded simulated-time windows with coverage and missing-evidence guards;
- pre-BC-1 history is not retroactively recomputed from current catalogs;
- a partially observed day cannot silently become a calorie deficit;
- BC-1 itself never changes body weight/body fat.

### BC-2 readiness gate — REQUIRED BEFORE MUTATION

Do **not** activate weight/BF progression merely because BC-1 code passes tests.

After PR #70 deploys, inspect natural production evidence without accelerating or mutating production. Before BC-2, establish that:
- ordinary action history supplies near-complete daily expenditure coverage;
- all naturally used edible targets carry nutrition profiles;
- natural meal cadence and total intake are plausible for the exemplar rather than artifacts of the old abstract hunger loop;
- REE/action-energy magnitudes stay plausible in natural runtime use.

If meal cadence is structurally too sparse/dense, fix the behavioral/needs-to-meal bridge before body-composition mutation. Do not compensate by assigning implausibly large/small calories to generic meals.

### BC-2 — Body Composition Progression Exemplar

Only after the readiness gate passes:
- activate coupled `body.weight_lb` + `body.body_fat_pct` through one universal actor-generic engine;
- derive FM/FFM and BMI consistently;
- combine bounded energy-balance evidence with FM/FFM partitioning;
- model resistance-training lean adaptation separately, constrained by training evidence, protein/energy availability, current training state and personalized genetic headroom;
- no crude sex hypertrophy multiplier;
- age/sex enter only where supported by evidence/policy;
- bootstrap at activation without retroactive gains;
- write coupled fields atomically with profile history + audit event;
- hard-clamp/reject implausible single-window changes;
- no Darian-specific branch and no extra model calls.

### BC-3 — Body Measurement Progression Batch

Only after BC-2 is live/validated. Circumferences must not be derived from weight alone; measurement changes need body composition plus regional training/anatomical policy.

## Exact resume point

Finish PR #70: canonical docs sync -> merge -> automatic deploy/readback -> synchronize `test` to `main`.

Then perform **read-only natural BC-1 evidence observation / meal-cadence readiness check**. If the evidence is plausible, proceed to BC-2; otherwise calibrate the minimum behavioral/needs-to-meal bridge first.

Do not add full Character Memory, multi-fallback/circuit-breaker architecture, forced equipment rotation, Telegram secret editing/model tuning, a second production character merely for testing, endocrine/micronutrient simulation, or schema v5 as side effects.
