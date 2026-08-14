# Observer Sandbox Roadmap

Status: ACTIVE
Roadmap synchronized: 2026-08-14

## Operating principles

- Python/SQLite runtime and world state are authoritative.
- AI proposes structured cognition; deterministic engines own mutation.
- Telegram is a Creator-facing observer/control adapter, not a simulation engine.
- Preserve the composable runtime contract:
  `Actor(s) + Action + Place + Simulation Time + Conditions/Modifiers + Resources/Targets -> Validation -> State Changes + Events`.
- Darian is the first richly specified exemplar, never reusable-engine identity.
- Character-specific facts/policy/world content are data; reusable simulation/cognition/progression/query/control logic is actor/entity-id driven.
- Schema v4 remains authoritative; no schema v5 without a concrete missing invariant.
- Prefer minimum-runnable reversible slices.
- Use exemplar-first for genuinely new invariants, then batch structurally equivalent follow-ons.
- For physiology/body systems, reconcile human evidence before freezing formulas; simulation approximations must be documented as policy rather than biological law.
- Default development: `test -> focused tests + CI -> merge main -> deploy if runtime-affecting -> read-only production check -> sync test`.
- Never accelerate or directly mutate production merely to manufacture acceptance evidence.

## Current verified production baseline

Latest deployed checkpoint before BC-1: **Deploy #175 `31788257885` SUCCESS** from PR #69 merge `e407533eff098f5803cc17469e8b9da8c24c21b8`.

Readback:
- service active / healthy;
- schema v4;
- world revision `thorne-estate-v3.3-physical-attribute-training`;
- default actor `char_darian`;
- autonomy enabled / normal, `paused=false`, `autonomy_retry=null`;
- speed `1.0x`;
- primary Gemini `gemini-3.1-flash-lite` preserved by ordinary bootstrap;
- fallback Groq `qwen/qwen3.6-27b` preserved;
- Telegram connected;
- `decision_calls=356` at readback;
- Darian sleeping in Master Suite with Energy 82.127, Fatigue 11.045, Hunger 50.325, Thirst 21.3, Sleepiness 31.55, Cleanliness 99.466.

## Completed platform/runtime layers

- Foundation schema v4 — COMPLETE.
- P0 Foundation & Remote Control — COMPLETE / LIVE VERIFIED.
- P0.5 dynamic AI provider/runtime layer — COMPLETE.
- P1 continuous autonomy — LIVE.
- P2 Telegram Observer/Profile/Control — COMPLETE / LIVE VERIFIED.
- P2.3 Telegram Creator AI Control v1 — COMPLETE / DEPLOYED / CREATOR-EXERCISED.
- Runtime Cognition Fallback v1 — COMPLETE / DEPLOYED / CREATOR-CONFIGURED.
- Telegram Home lifecycle — COMPLETE / DEPLOYED.
- Universal Character Engine Contract — COMPLETE / CI VERIFIED / DEPLOYED.
- Dynamic Resource Awareness / Choice Breadth — DEPLOYED.
- Object Familiarity / Inspect Utility Guard — DEPLOYED.
- P3.1 systemic fatigue/recovery — COMPLETE / LIVE VERIFIED.
- P3.2 targeted training — COMPLETE.
- P3.3 readiness — COMPLETE / DEPLOYED.
- P3.4 effectiveness — COMPLETE / DEPLOYED.
- P3.5 effective training load — COMPLETE / DEPLOYED.
- Minimum Training Stimulus v1 — COMPLETE / DEPLOYED.
- Training Session Load & Recovery Guard v1 — COMPLETE / DEPLOYED.
- Causal living needs + sleep pressure/circadian behavior — DEPLOYED.
- Training Method Semantics v1 — COMPLETE / DEPLOYED.

## Universal Character Engine

Canonical contract: `docs/UNIVERSAL_CHARACTER_ENGINE_CONTRACT.md`.

Invariant:
- explicit actor -> configured valid default actor -> sole actor resolution;
- ambiguous multi-character implicit selection fails closed;
- another actor cannot inherit Darian cognition policy silently;
- missing location is invalid state, not implicit Master Suite;
- global resume wakes every eligible actor;
- Darian/Thorne named data remains exemplar content only;
- synthetic non-Darian regression guards identity leakage.

## Physical Attribute Progression Framework v1

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.
Canonical contract: `docs/PHYSICAL_ATTRIBUTE_PROGRESSION_FRAMEWORK.md`.

PR #68 final head `5ebe50d0752790c1abea7ee6d653be8ebd5a1c2e`; merge `3bceda924ed0fe18ce1d1360f6e0cc2c62c55f7e`; CI #608/post-merge #609 plus targeted acceptances green; Deploy #174 success.

All seven core RAPS-PA fields have live progression:
- Strength;
- Stamina;
- Agility;
- Speed;
- Reflexes;
- Endurance;
- Flexibility.

Speed/Reflexes/Endurance/Flexibility use the actor-generic policy-driven framework. Existing Strength/Stamina/Agility implementations remain stable. Flexibility has a real Mobility & Stretching Area and `mobility_stretching` evidence method. Activation never retroactively awards historical gain.

## Grading state

- Strength grading exemplar — COMPLETE / DEPLOYED.
- Attribute Grading Batch 1 — COMPLETE / DEPLOYED for compatible 0..100 fields.
- IQ remains a separate scale.
- Skills grading/progression remains separate.
- Body composition/measurements are a distinct physiology family.

## Body Composition Progression Program — CURRENT ACTIVE PROGRAM

Canonical research contract: `docs/BODY_COMPOSITION_RESEARCH_FOUNDATION.md`.
Canonical BC-1 contract: `docs/NUTRITION_ENERGY_EVIDENCE.md`.

Creator requirement: realistic human body behavior must consider age, sex, individual genetic potential, nutrition/energy balance and plausible body proportions before formulas are frozen.

### Evidence-led decisions

Research reconciled from NIH/NIDDK Hall/Forbes dynamic body-weight work, resistance-training sex/age response evidence, genetic/inter-individual variability, protein/energy-deficit literature, body-composition references and the 2024 Compendium of Physical Activities.

Locked direction:
- no universal static `3500 kcal = 1 lb` law;
- model weight, FM, FFM and BF% as a coupled system over bounded settlement intervals;
- Hall/Forbes-style partitioning is a documented first-order approximation, not a full human metabolic model;
- sex affects baseline/reference physiology but is not a crude hypertrophy multiplier;
- age is context/modifier, not a hard response cliff;
- genetic potential is character-specific canonical/config data; population FFMI/FMI is plausibility context only;
- kcal/protein cannot be inferred from abstract hunger/energy scores;
- protein/energy availability constrains later lean adaptation;
- action expenditure is actor-scaled using a resting-energy reference plus authored Compendium-informed intensity anchors;
- no schema v5 required for the first body-composition engine.

Current profile already declares `body.weight_lb`, `body.body_fat_pct`, derived `body.lean_mass_lb`, `body.fat_mass_lb`, `body.bmi`, canonical DOB/sex/height, and genetic lean-condition weight range/body-fat floor.

### BC-0 — Simulated Profile Re-seed Safety

Status: **COMPLETE / CI VERIFIED / DEPLOYED**.

PR #69:
- tested head `2a23ff48207867a6684832b8fefdd260053eac78`;
- CI #610 SUCCESS;
- merge `e407533eff098f5803cc17469e8b9da8c24c21b8`;
- post-merge CI #611 SUCCESS;
- Deploy #175 SUCCESS.

Invariant: ordinary canonical seed import initializes inactive fields but preserves existing `mode=simulated` value/mode/authority/source. Non-simulated canonical/static fields remain intentionally seed-updatable.

### BC-1 — Minimum Nutrition & Energy Balance Evidence

Status: **IMPLEMENTED / CI VERIFIED / PRODUCTION-COPY VALIDATED ON PR #70; MERGE/DEPLOY PENDING**.

Current PR #70 head: `06cb2dddb34367cc1218cccd9341125a73693b7a` plus canonical-doc synchronization commits on `test`.

Implementation:
- `config/nutrition_profiles.v1.json` supplies authored kcal/protein/carbohydrate/fat profiles for current edible resources;
- `config/energy_expenditure.v1.json` supplies Mifflin-St Jeor resting-energy reference plus Compendium-informed action/training intensity anchors;
- completed action events snapshot immutable `nutrition_intake` and `energy_expenditure` evidence;
- `energy_balance_window()` aggregates persisted evidence over bounded sim-time windows;
- coverage/missing-evidence guards prevent partially observed history from becoming an artificial deficit;
- historical pre-BC-1 actions are not silently recomputed from current policy;
- BC-1 never mutates weight or body fat.

Validation:
- CI #613 SUCCESS on head `06cb2ddd...`;
- Nutrition & Energy Evidence Acceptance #1 / run `31788917813` SUCCESS on a disposable production copy;
- copied-production Darian REE estimate: about `2073.388 kcal/day` from his own age/sex/height/weight;
- disposable 25-minute prepared-meal action: `800 kcal`, `50 g protein`, `90 g carbohydrate`, `27 g fat` intake evidence;
- estimated action expenditure: about `53.994 kcal`, multiplier `1.5`;
- body weight/BF remained unchanged;
- model calls 0; Telegram calls 0; live production DB unchanged.

### BC-2 readiness gate — REQUIRED

Do not activate body-weight/BF mutation merely because BC-1 tests pass.

After PR #70 deploys, use read-only natural production evidence to establish:
- near-complete ordinary action-time expenditure coverage;
- naturally used edible targets all have nutrition evidence;
- natural meal cadence and total intake are physiologically plausible rather than artifacts of the older abstract hunger loop;
- resting/action expenditure magnitudes remain plausible in ordinary runtime.

If meal cadence is too sparse/dense, calibrate the minimum needs-to-meal behavioral bridge before BC-2. Never hide a cadence defect by assigning implausibly huge/tiny calories to a generic meal.

### BC-2 — Body Composition Progression Exemplar

Only after readiness passes:
- activate coupled `body.weight_lb` + `body.body_fat_pct` through one actor-generic deterministic engine;
- derive FM/FFM/BMI consistently;
- aggregate causal nutrition/expenditure/training evidence over bounded windows;
- use bounded FM/FFM partitioning rather than one fixed tissue ratio;
- model resistance-training lean adaptation separately, constrained by training evidence, protein/energy availability, training state and personalized genetic headroom;
- no crude sex hypertrophy multiplier;
- age/sex enter only where evidence supports them;
- bootstrap at the activation boundary without retroactive gain/loss;
- write coupled fields atomically with profile history/audit event;
- clamp/reject implausible single-window changes;
- no Darian-specific branch and no extra model calls.

### BC-3 — Body Measurement Progression Batch

Only after BC-2 is live/validated. Circumferences must combine composition, regional training/anatomy and character-specific structural/genetic envelopes; do not derive every circumference from body weight alone.

## Planned profile unlock after body composition

1. BC-1 deploy + natural evidence readiness gate;
2. BC-2 body composition exemplar;
3. BC-3 body measurement batch;
4. skill progression exemplar;
5. compatible skill batch;
6. intellectual attribute exemplar/batch;
7. mental/emotion dynamics;
8. later social/relationship/sexual physiology families as their causal prerequisites exist.

## Deferred boundaries

Do not add as side effects:
- full Character Memory Engine;
- multi-fallback/circuit-breaker/provider-health systems;
- Telegram secret/model-parameter editing;
- second production character solely for testing;
- forced equipment rotation;
- generalized inventory depletion;
- detailed endocrine or menstrual-cycle/hormone engine;
- micronutrient or organ-by-organ metabolic simulation;
- exact fluid/glycogen fluctuation model;
- richer relationship engine;
- estate exterior/Tahoe traversal;
- schema v5.

## Exact resume point

Finish PR #70: docs sync -> full CI/acceptance on final head -> merge -> Deploy/readback -> sync `test` to `main`.

Then inspect **natural BC-1 evidence read-only**. If cadence/coverage/magnitudes are plausible, authorize the already-planned BC-2 exemplar implementation under this evidence contract; otherwise make the smallest causal meal-behavior calibration first.
